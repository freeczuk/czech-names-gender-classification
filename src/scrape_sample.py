from src.names import CzechNamesCorpus, GenderType

if __name__ == "__main__":
    # May take about 15 minutes
    corpus_handle = CzechNamesCorpus()
    first_names = corpus_handle.scrape_first_names(
        max_pages=300, genders=[GenderType.male, GenderType.female]
    )
