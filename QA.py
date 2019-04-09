# coding:utf-8

import requests
from bs4 import BeautifulSoup
import os


url = 'https://so.csdn.net/so/search/s.do?q=%E5%AE%89%E8%A3%85pip%E6%97%B6%E6%8A%A5%E9%94%99&t=ask&u='
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
s = requests.Session()
r = s.get(url, headers=header)
r.encoding = 'utf-8'
doc = r.text.encode("utf-8")
'''
with open(os.path.abspath('SEO/spider.html'), 'w') as f1:
    f1.write(str(doc))
'''
soup = BeautifulSoup(doc, 'html.parser')

div = soup.find_all('dl', class_='search-list J_search')
for d in div:
    print d.a.get_text()


#request_url = div[0].a['href']
request_url = 'https://ask.csdn.net/questions/679094'
s = requests.Session()
r = s.get(request_url, headers=header)
r.encoding = 'utf-8'
doc = r.text.encode("utf-8")
soup = BeautifulSoup(doc, 'html.parser')
question = soup.find('div', class_='questions_detail_con')
print question.dt.get_text()
print question.dd.p.get_text()

answer = soup.find_all('div', class_='answer_detail_con')
for a in answer:
    print a.p