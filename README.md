
# Czech Names Gender Classification

This repository contains a Python code for scraping and classifying Czech names based on gender.
The tool leverages web scraping, machine learning models, and a names datasets to estimate
the gender.

## Features

- **Web Scraping**: Scrape Czech male and female names from the [krestnijmeno.prijmeni.cz](https://krestnijmeno.prijmeni.cz) website.
- **Data Storage**: Save the scraped names into CSV files for later use.
- **Gender Classification** (see [workflow diagram](https://app.diagrams.net/?tags=%7B%7D&title=Gender%20estimation%20based%20on%20the%20Czech%20facebook%20user%20name.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1ae-bg7SJjikO_j0Vp39UWUarm2ZwIytC%26export%3Ddownload)):
  - **Corpus-Based**: Match names against a pre-collected corpus of male and female first names.
  - **Suffix Analysis**: Determine gender based on typical male or female name suffixes.
  - **Leaked Data Matching**: Compare names with leaked Czech Facebook users' data.
  - **Zero-Shot Classification**: Use a pre-trained BERT-based model for gender prediction when other methods are inconclusive.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/freeczuk/czech-names-gender-classification.git
   cd czech-names-gender-classification
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Data Setup

To function properly, the following CSV files need to be added to the `data` folder:
1. `fb_users_leak_CZ.csv`
2. `female_names.csv`
3. `male_names.csv`

Since the data may be considered sensitive, it is not provided in this repository. Refer to the `data/info.md` file for 
the instructions on how to obtain and prepare these files.

## Usage

1. **Scrape and Store Names**:
   ```python
   from src.names import CzechNamesCorpus, GenderType

   corpus_handle = CzechNamesCorpus()   
   data = corpus_handle.scrape_first_names(max_pages=300, genders=[GenderType.male, GenderType.female])
   ```
   
2. **Load from storage** (*only once scrapped*):
   ```python
   from src.names import CzechNamesCorpus

   corpus_handle = CzechNamesCorpus()   
   data = corpus_handle.load_from_storage()
   ```

3. **Classify Names**:
   ```python
   from src.classifier import NameClassifier
   from src.names import CzechNamesCorpus
   
   corpus_handle = CzechNamesCorpus()
   data = corpus_handle.load_from_storage()
   
   classifier = NameClassifier(corpus=data)
   result = classifier.classify_commenters(["Jan Novak", "Petra Svobodova"])
   print(result)
   ```

## Structure

- **data**: Scrapped names and leaked names data
- **src**
  - **names.py**: Handles web scraping and data storage.
  - **classifier.py**: Provides means for estimating the gender


## Possible TODOs

- **Error Handling**: Implement better error handling for HTTP requests in `_get_page`.
- **File Path Configuration**: Remove hardcoded file paths; allow users to specify paths or use a configuration object.
- **Performance Optimization**: Improve the efficiency of `check_name_against_first_names_corpus`.
- **Logging**: Replace `print` statements with logging for better output control.
- **Documentation**: Add detailed docstrings to methods for better clarity.

