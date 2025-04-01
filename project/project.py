import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
import os
import requests
import pandas as pd

nltk.download('punkt_tab')

df = pd.read_excel("Input.xlsx")

output_dir = "extract_articles"
os.makedirs(output_dir, exist_ok=True)

def extract(url):
  response = requests.get(url, timeout=10)
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'html.parser')
  title = soup.find("title").get_text(strip=True)
  content = soup.find_all(attrs = {'class':'td-post-content'})#extracting only text part
  content = content[0].text if len(content) > 0 else ''
  return title, content

for index, row in df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]

    title, article_text = extract(url)

    output_path = os.path.join(output_dir, f"{url_id}.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(f"{title}\n\n{article_text}")

stopwords_files = [
    "StopWords_Names.txt",
    "StopWords_Geographic.txt",
    "StopWords_GenericLong.txt",
    "StopWords_Generic.txt",
    "StopWords_DatesandNumbers.txt",
    "StopWords_Currencies.txt",
    "StopWords_Auditor.txt",
]

def load_stopwords(stopwords_files):
    stopwords = set()
    for file_path in stopwords_files:
        with open(file_path, "r", encoding="ISO-8859-1") as f:
            stopwords.update(f.read().splitlines())
    return stopwords

stopwords = load_stopwords(stopwords_files)

def load_words(file_path):
    with open(file_path, "r", encoding="ISO-8859-1") as f:
        return set(f.read().splitlines()) - stopwords

positive_words = load_words("positive-words.txt")
negative_words = load_words("negative-words.txt")

output_data = pd.read_excel('Input.xlsx')

def calculate_metrics(text):
    text = re.sub(r'[^A-Za-z ]+', '', text)
    text = text.lower()
    sentences = sent_tokenize(text)
    tokens = word_tokenize(text)
    word_count = len(tokens)
    sentence_count = len(sentences)

    positive_score = 0
    negative_score = 0

    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)

    avg_sentence_length = word_count / sentence_count if sentence_count else 0
    complex_words = [word for word in tokens if sum(1 for char in word if char in 'aeiou') > 2]
    percentage_complex_words = len(complex_words) / word_count if word_count else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = word_count / sentence_count if sentence_count else 0
    complex_word_count = len(complex_words)

    syllable_per_word = sum(sum(1 for char in word if char in 'aeiou') for word in tokens) / word_count if word_count else 0
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in tokens) / word_count if word_count else 0

    return positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, syllable_per_word, personal_pronouns, avg_word_length

res =[]
for index, row in output_data.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]
    file_path = os.path.join(output_dir, f"{url_id}.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, syllable_per_word, personal_pronouns, avg_word_length = calculate_metrics(text)
    #print(positive_score)
    #print(negative_score)
    res.append({
                "URL_ID": url_id,
                "URL": url,
                "Positive_Score": positive_score,
                "Negative_Score": negative_score,
                "Polarity_Score": polarity_score,
                "Subjectivity_Score": subjectivity_score,
                "Avg_Sentence_Length": avg_sentence_length,
                "Percentage_Complex_Words": percentage_complex_words,
                "Fog_Index": fog_index,
                "Avg_Words_Per_Sentence": avg_words_per_sentence,
                "Complex_Word_Count": complex_word_count,
                "Word_Count": word_count,
                "Syllable_Per_Word": syllable_per_word,
                "Personal_Pronouns": personal_pronouns,
                "Avg_Word_Length": avg_word_length
            })
    res_df = pd.DataFrame(res)
    res_df.to_excel("Output_Data_Structure.xlsx", index=False)

print("Analysis complete. Results saved in 'Output_Data_Structure.xlsx'.")
