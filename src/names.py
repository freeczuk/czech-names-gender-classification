from enum import Enum
from io import StringIO

import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


class GenderType(Enum):
    male = "Male name"
    female = "Female name"


class CzechNamesCorpus:
    url_base = "https://krestnijmeno.prijmeni.cz"
    endpoint = "oblast/3000-ceska_republika"

    def scrape_first_names(self, genders: list[GenderType], max_pages=300):
        for gender in genders:
            names = self._get_names(gender=gender, max_pages=max_pages)
            names.to_csv(f"data/{gender.name}_names.csv")
        return self.load_from_storage()

    def _get_names(self, gender: GenderType, max_pages: int = 300) -> pd.DataFrame:
        subpage = "zenska_jmena" if GenderType.female == gender else "muzska_jmena"
        url = f"{self.url_base}/{self.endpoint}/{subpage}"

        pages = []
        for page_number in tqdm(range(1, max_pages), desc=f"Scrapping {gender.name} first names"):
            page_names = self._get_page(url, page_number)
            pages.append(page_names)

        df = pd.concat(pages)
        return df

    @staticmethod
    def _get_page(url, page_number: int) -> pd.DataFrame:
        response = requests.get(url, params={"page": page_number})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="lxml")
        names_table_str = soup.find("table").parent.encode_contents().decode()
        names_table = pd.read_html(StringIO(names_table_str))[0]
        return names_table

    @staticmethod
    def load_fb_leaked_users() -> pd.DataFrame:
        """Except of ~1.4 M names from leaked Czech FB users data

        See: https://github.com/philipperemy/name-dataset
        """
        filename = "data/fb_users_leak_CZ.csv"
        users_df = pd.read_csv(filename, header=None)
        users_df.columns = ["First name", "Surname", "Gender", "Location"]
        users_df["First name"] = users_df["First name"].str.lower()
        users_df["Surname"] = users_df["Surname"].str.lower()
        return users_df

    def load_from_storage(self) -> dict[str, set | pd.DataFrame]:
        female_first_names = pd.read_csv("data/female_names.csv")
        male_first_names = pd.read_csv("data/male_names.csv")

        corpus = {
            "female_first_names": set(female_first_names["Jméno"].str.lower()),
            "male_first_names": set(male_first_names["Jméno"].str.lower()),
            "facebook_leak": self.load_fb_leaked_users(),
        }

        return corpus
