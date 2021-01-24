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


def find_second_underscore(text):
    counter = 0
    for i in range(len(text)):
        if text[i] == "_":
            counter += 1
        if counter == 2:
            return i


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
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words="english")


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


def categorise(filename):
    subject_name = []
    text_string = []
    similarity_scores = []
    path = "/home/cdt1901/Projects/text_similarity/training_data"
    # for dir in os.listdir(path):
    #     for file in os.listdir(path + "/" + dir):
    #         subject_name.append(dir + "_" + file)
    #         with open(path + "/"+ dir + "/" + file, 'r') as f:
    #             data = f.read().replace('\n', '')
    #             text_string.append(data)
    #             similarity_scores.append(cosine_sim(data, eq_worksheet))

    with open("textbooks", "rb") as f:
        textbooks = pickle.load(f)

    for subj, text in textbooks.items():
        subject_name.append(subj)
        similarity_scores.append(cosine_sim(text, filename))

    similarity_scores, subject_name = (list(t) for t in zip(*sorted(zip(similarity_scores, subject_name))))

    return [
        re.sub("_", " ", subject_name[-1][: find_second_underscore(subject_name[-1])]).capitalize(),
        subject_name[-1][find_second_underscore(subject_name[-1]) + 1 :],
        subject_name[-2][find_second_underscore(subject_name[-2]) + 1 :],
        subject_name[-2][find_second_underscore(subject_name[-2]) + 1 :],
    ]


def main():
    # eq_chapter = FileParser("/home/cdt1901/Projects/hackbridge/hex-cambridge/backend/sample_inputs/eq_chapter.pdf")
    # carb_chapter = FileParser("/home/cdt1901/Projects/hackbridge/hex-cambridge/backend/sample_inputs/carbonyl_chapter.pdf")
    eq_worksheet = FileParser("/home/cdt1901/Projects/hackbridge/hex-cambridge/backend/sample_inputs/Camera_flash.jpg")
    out = categorise(eq_worksheet)
    print(out)


if __name__ == "__main__":
    main()
