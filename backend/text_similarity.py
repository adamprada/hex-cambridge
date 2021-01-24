import nltk
import string
import textract
import re
import sys
import time
import os
import pickle
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('punkt')  # if necessary...

import tensorflow as tf

dir_path = os.path.dirname(os.path.abspath(__file__))

@tf.keras.utils.register_keras_serializable()
def simple_standardization(input_data):
  lowercase = tf.strings.lower(input_data)
  return lowercase

model = tf.keras.models.load_model(os.path.join(dir_path, "../deep_learning/classification_model"))

labels = ["Biological chemistry",
          "Inorganic chemistry", 
          "Organic chemistry", 
          "Physical chemistry"]


def predict_field(text):
    ilabel = np.argmax(model.predict([text])[0])
    return labels[ilabel]

def prune_text_general(text):
    out = text
    out = re.sub(r"\d", "", out)
    out = re.sub(r"[^\w\s]", "", out)
    out = re.sub("\n", " ", out)
    out = re.sub(
        r"\bof\b|\bat\b|\ball\b|\bin\b|\bfor\b|\bto\b|\bis\b|\bthe\b|\band\b|\bor\b|\balso\b|\ba\b|", "", out, flags=re.IGNORECASE
    )
    out = out.strip()
    out = " ".join(out.split())
    return out


def FileParser(filename):
    """Read in file (tested pdf, docx, png) and return list of words

    Args:
        filename (file): pdf, docx, png

    Returns:
        list: list of strings with escape characters removed
    """
    text = textract.process(filename)
    text_decoded = text.decode()
    text_list = re.sub("[^A-Za-z0-9]+", " ", text_decoded)
    out = prune_text_general(text_list)
    return out


def stem_tokens(tokens):
    stemmer = nltk.stem.porter.PorterStemmer()
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words="english")
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


def categorise(filename):
    input_file = FileParser(filename)
    path = os.path.join(os.path.dirname(dir_path), "data_harvesting/similarity_data/")
    branch = predict_field(" ".join(input_file)) 
    path = os.path.join(path, "chemistry", branch.lower().replace(" ","_"))
    subject_name = []
    text_string = []
    similarity_scores = []
    for filename in os.listdir(path):
        subject_name.append(filename)
        with open(os.path.join(path,filename), 'r') as f:
            data = f.read().replace('\n', '')
            text_string.append(data)
            similarity_scores.append(cosine_sim(data, input_file))

    similarity_scores, subject_name = (list(t) for t in zip(*sorted(zip(similarity_scores, subject_name))))
    return [branch] + subject_name[-1:-4:-1]


def main():
    # eq_chapter = FileParser("/home/cdt1901/Projects/hackbridge/hex-cambridge/backend/sample_inputs/eq_chapter.pdf")
    # carb_chapter = FileParser("/home/cdt1901/Projects/hackbridge/hex-cambridge/backend/sample_inputs/carbonyl_chapter.pdf")
    in_file = "sample_inputs/Camera_flash.jpg"
    out = categorise(in_file)
    print(out)


if __name__ == "__main__":
    main()
