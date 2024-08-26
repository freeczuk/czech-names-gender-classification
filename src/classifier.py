from transformers import pipeline


class NameClassifier:
    def __init__(self, corpus: dict):
        self.corpus = corpus
        self.zero_shot_classifier = pipeline(
            task="zero-shot-classification",
            model="facebook/bart-large-mnli",
        )

    def check_name_against_first_names_corpus(
        self, corpus_gender: str, name_parts: list[str]
    ) -> bool:
        gender_names = self.corpus.get(corpus_gender)
        matches = [name_part for name_part in name_parts if name_part in gender_names]
        return bool(matches)

    @staticmethod
    def check_name_against_surnames(name_parts: str):
        surname = name_parts[-1]
        male_suffixes = ["ák", "ač", "ek", "ej", "ík", "ý", "čka", "il"]
        female_suffixes = ["ová", "ská", "á"]

        matches = {}
        for gender, suffixes in zip(["Male", "Female"], [male_suffixes, female_suffixes]):
            for suffix in suffixes:
                suffix_match = surname.endswith(suffix)
                if suffix_match:
                    matches[gender] = suffix_match
                    break

        if len(matches) == 1:
            gender_identification_result = "Male" if "Male" in matches else "Female"
        else:
            gender_identification_result = None

        return gender_identification_result

    def classify_commenters(self, commenter_names: list[str]) -> dict[str, str]:
        commenter_gender_map = {}
        for i, commenter_name in enumerate(commenter_names):
            gender_identification_result = self.estimate_gender(commenter_name)
            commenter_gender_map[commenter_name] = gender_identification_result
            print(f"{i:04d} | {commenter_name:<30}{gender_identification_result}")

        return commenter_gender_map

    def zero_shot_classify(self, name_parts: list[str]):
        labels = ["Female name", "Male name"]
        name = " ".join(name_parts)
        classification_result = self.zero_shot_classifier(name, labels)
        if classification_result["scores"][0] > 0.7:
            gender_identification_result = (
                "Female" if "Female" in classification_result["labels"][0] else "Male"
            )
        else:
            gender_identification_result = "Unknown"
        return gender_identification_result

    def estimate_gender(self, commenter_full_name: str) -> str:
        commenter_name_small = commenter_full_name.lower()
        name_parts = commenter_name_small.split(" ")

        identified_as_female = self.check_name_against_first_names_corpus(
            corpus_gender="female_first_names", name_parts=name_parts
        )
        identified_as_male = self.check_name_against_first_names_corpus(
            corpus_gender="male_first_names", name_parts=name_parts
        )

        if identified_as_male ^ identified_as_female:
            gender_identification_result = "Male" if identified_as_male else "Female"
        else:
            gender_identification_result = self.run_deeper_name_checks(name_parts)

        return gender_identification_result

    def check_name_against_fb_leaked_users(self, name_parts):
        fb_leak_df = self.corpus["facebook_leak"]
        first_name_matches = fb_leak_df["First name"] == name_parts[0]
        surname_matches = fb_leak_df["Surname"] == " ".join(name_parts[1:])

        full_name_matches = first_name_matches & surname_matches
        name_component_matches = first_name_matches | surname_matches

        if full_name_matches.any():
            gender_dict = fb_leak_df[full_name_matches]["Gender"].value_counts()
        elif name_component_matches.any():
            gender_dict = fb_leak_df[name_component_matches]["Gender"].value_counts()
        else:
            return None

        occurrence = sorted(gender_dict.items(), key=lambda x: x[1], reverse=True)
        occurrence_map = {"M": "Male", "F": "Female"}
        if len(occurrence):
            gender_identification_result = occurrence_map.get(occurrence[0][0], None)
        elif len(occurrence) > 1:
            if occurrence[0][1] == occurrence[1][1]:
                gender_identification_result = None
            else:
                gender_identification_result = occurrence_map.get(occurrence[0][0], None)
        else:
            gender_identification_result = None

        return gender_identification_result

    def run_deeper_name_checks(self, name_parts):
        gender_identification_result = self.check_name_against_surnames(name_parts)
        if gender_identification_result:
            return gender_identification_result

        gender_identification_result = self.check_name_against_fb_leaked_users(name_parts)
        if gender_identification_result:
            return gender_identification_result

        gender_identification_result = self.zero_shot_classify(name_parts)

        return gender_identification_result
