#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os

question = raw_input("please enter your question:\n")

request_url = "https://so.csdn.net/so/search/s.do?p=&q={0}&t=&domain=&o=&s=&u=&l=&f=".format(question)
header = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
}

s = requests.Session()
r = s.get(request_url, headers=header)
r.encoding = 'utf-8'
doc = r.text.encode("utf-8")
#print type(doc)

soup = BeautifulSoup(doc, 'html.parser')

# 清空html内容
with open(os.path.abspath('爬虫/csdn.html'), 'w') as f1:
    f1.truncate()

dl = soup.find_all('dl', class_='search-list J_search')
for dl in dl:
    if dl.span.get_text().encode('utf-8') == "博客" or dl.span.get_text().encode('utf-8') == "问答":
        #print str(dl.a)
        #print dl.a.get_text()
        print dl.a.get_text() + '[' + dl.a['href'] + ']'
        print "--------------------------------------------"
        with open(os.path.abspath('爬虫/csdn.html'), 'a') as f1:
            f1.write(str(dl.a)+"\n<br>\n")
            #f1.write(dl.a.get_text().encode("utf-8")+"\n")