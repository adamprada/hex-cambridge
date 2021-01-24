import nltk
import string
import textract
import re
import sys
import time
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('punkt')  # if necessary...


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


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


def main():
    path = "../data_harvesting/harvested_data/chemistry"
    d = {}
    for dir in os.listdir(path):
        for file in os.listdir(path + "/" + dir):
            with open(path + "/" + dir + "/" + file, "r") as f:
                data = f.read().replace("\n", "")
                d[dir + "_" + file] = data
    with open("textbooks", "wb") as outfile:
        pickle.dump(d, outfile)


if __name__ == "__main__":
    main()
