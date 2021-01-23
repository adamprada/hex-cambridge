"""
sudo apt install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

pip install textract
"""

import textract
import re
import sys


def FileParser(filename):
    """Read in file (tested pdf, docx, png) and return list of words

    Args:
        filename (file): pdf, docx, png

    Returns:
        list: list of strings with escape characters removed
    """
    text = textract.process(filename)
    text_decoded = text.decode()
    text_list = re.sub("[^A-Za-z0-9]+", " ", text_decoded).split(" ")
    return text_list

def main():
    words = FileParser(sys.argv[1])
    print(words)


if __name__ == "__main__":
    main()
