"""
retrieve set of links to kata texts on remote site

for each link:
    access and retrieve everything within the "article" element
    Write out all of the content to a file within a directory whose name matches the last part of the followed link
"""

import re
import pathlib
import sys
from urllib import request

from bs4 import BeautifulSoup
from html2text import html2text

def retrieve_article(link):
    html_doc = request.urlopen(link).read().decode('utf-8')
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.body.find(id="content").article

grammar = re.compile("Kata\d\d")
html_doc = request.urlopen("http://codekata.pragprog.com/").read().decode('utf-8')
soup = BeautifulSoup(html_doc, 'html.parser')
links = {
    link.get("href")
    for link in soup.find_all('a')
    if grammar.findall(str(link))    # if a link matches Kata{0-9}{0-9}
}

for link in links:
    uri = link.split("/")[-2]
    pathlib.Path(uri).mkdir(exist_ok=True) 
    with open("{0}/kata.md".format(uri), "w") as kata:
        kata.write(html2text(str(retrieve_article(link))))
