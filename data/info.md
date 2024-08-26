
### 3 csv files are required:

- `fb_users_leak_CZ.csv`
   1. See the [name-dataset](https://github.com/philipperemy/name-dataset) Github project.
   2. Download the [name_dataset.zip](https://drive.google.com/file/d/1QDbtPWGQypYxiS4pC_hHBBtbRHk9gEtr/view) from Google Drive (3.3 GB).
   3. Use a zip file manager to unzip only `name_dataset/data/CZ.csv`.
   4. Rename `CZ.csv` to `fb_users_leak_CZ.csv` and place it under the `data` folder.
- `female_names.csv` & `male_names.csv`
   1. Run `scrape_first_names.py`. This script will automatically extract and save the data
   from the web into the `data` folder.
