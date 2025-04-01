# **Financial Text Sentiment Analysis**

## **Project Overview**
This Python script performs **Sentiment Analysis** and **Readability Analysis** on financial texts. It calculates various linguistic metrics such as **polarity score, subjectivity score, fog index, average word length**, and more. Using requests to extract URLs, using BeautifulSoup to extract text and title of each article from every URL, and finally using nltk and re to clean up, and extract words and sentences from the text of each article to perform sentiment analysis and readability analysis on the given list of articles. Uploading all the relevant scores into the Output_Data_Structure.xlsx file.

The analysis follows these steps:
1. **Preprocessing**: Cleaning text by removing stopwords, special characters, and unwanted symbols.
2. **Sentiment Analysis**: Using predefined **positive and negative word dictionaries** to calculate sentiment scores.
3. **Readability Metrics**: Computing text complexity using formulas like **Gunning Fog Index**.
4. **Exporting Results**: The analysis results are saved in **CSV/Excel format**.

---

## **Installation & Dependencies**
Before running the script, install the required Python libraries using:

```sh
pip install nltk pandas openpyxl requests beautifulsoup4
```

Ensure that the **NLTK Punkt tokenizer** is available:

```python
import nltk
nltk.download('punkt-tab')
```

---

## **How to Run the Script**
1. In a folder, place the relevantfiles
2. Place Input.xlsx in the same folder
2. Ensure the required **stopword lists** .txt files and **positive/negative dictionaries** .txt files are available in the same directory as the script.
3. Run the script:

   ```sh
   python assignment.py
   ```

4. The results will be saved as `Output_Data_Structure.xlsx`.
NOTE: the code will show error/warnings in the end, ignore
---

## **Output Structure**
Each row in the output file contains:
| FILENAME | POSITIVE SCORE | NEGATIVE SCORE | POLARITY SCORE | SUBJECTIVITY SCORE | AVG SENTENCE LENGTH | FOG INDEX | COMPLEX WORD COUNT | WORD COUNT | SYLLABLE PER WORD | PERSONAL PRONOUNS | AVG WORD LENGTH |
|----------|---------------|---------------|---------------|----------------|-------------------|----------|------------------|-----------|----------------|-----------------|----------------|

---

## **Troubleshooting**
- If `nltk.tokenize` is not found, install NLTK and download `punkt-tab`:
  ```sh
  pip install nltk
  python -c "import nltk; nltk.download('punkt-tab')"
  ```
- If file encoding issues occur, ensure all text files use **UTF-8** encoding.

---

## **Future Improvements**
- Implement **machine learning-based sentiment classification**.

---
