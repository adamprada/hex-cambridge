#!/usr/bin/env python3
import os
import re
import subprocess

def get_text_from_html(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def get_html_from_url(url):
    from urllib.request import urlopen
    html = urlopen(url).read()
    text = get_text_from_html(html)
    return html

def get_text_from_url(url):
    html = get_html_from_url(url)
    text = get_text_from_html(html)
    return text

def prune_html(html):
    out = html.decode().split("</header>",1)[1]
    return out

def prune_text_general(text):
    out = text
    out = re.sub(r'\d',"",out)
    out = re.sub(r'[^\w\s]','',out)
    out = re.sub('\n',' ',out)
    out = out.strip()
    out = " ".join(out.split())
    return out

def prune_text(text):
    out = text.split("Back to top",1)[0]
    out = re.split("Page ID\d+",out)[1]
    out = re.sub(r'\\\[(.*?)\\\]',"",out)
    out = re.sub(r'\\\((.*?)\\\)',"",out)
    out = prune_text_general(out)
    return out

def check_chapter(chapter):
    out = True
    if re.match("\d\.\d",chapter) is None:
        out = False
    return out

class Datapoint:
    def __init__(self, subject, branch, chapter, text,
            chapter_number,section_number):
        self.subject = subject
        self.branch = branch
        self.chapter = chapter
        self.chapter_number = chapter_number
        self.section_number = section_number
        self.text = text
        self.path = subject + "/" + branch

def get_datapoint_from_file(filepath):
    with open(textbookpath + "/" + xmlfile, 'r') as xfile:
        data = xfile.read().replace('\n', '')
        url = re.findall(r'<url href="(.*?)"',data)[0]
        chapter = get_text_from_html(data)
        if check_chapter(chapter):
            tmp = re.split("[\.:]",chapter)
            chapter_number = tmp[0]
            section_number = tmp[1]
            chapter = tmp[2]
            chapter = prune_text_general(chapter)
            html = get_html_from_url(url)
            html = prune_html(html)
            text = get_text_from_html(html)
            text = prune_text(text)
            return Datapoint(subject,branch,chapter,text,chapter_number,section_number)
        else:
            return None


datalist = []
rootpath = "./textbooks"
datapath = "./training_data"
for subject in os.listdir(rootpath):
    print("Subject:     " + subject)
    subjectpath = rootpath + "/" + subject
    for branch in os.listdir(subjectpath):
        print("Branch:      " + branch)
        branchpath = subjectpath + "/" + branch
        for textbook in os.listdir(branchpath):
            print("Textbook:    " + textbook)
            textbookpath = branchpath + "/" + textbook
            for xmlfile in os.listdir(textbookpath):
                if "T_" in xmlfile:
                    datapoint = get_datapoint_from_file(textbookpath + "/" + xmlfile)
                    if datapoint is not None:
                        datalist.append(datapoint)

for point in datalist:
    bashCommand = "mkdir -p "+ datapath + "/" + point.path
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
for point in datalist:
#    with open(datapath + "/" + point.path + "/" + point.chapter, 'w') as xfile:
    print(point.chapter)
    if (point.chapter != "") and (len(point.chapter)>1):
        with open(datapath + "/" + point.path + "/" + point.chapter, 'w') as xfile:
            xfile.write(point.text)
