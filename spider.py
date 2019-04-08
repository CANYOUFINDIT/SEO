# coding:utf-8

import requests
from bs4 import BeautifulSoup
import os

url = 'https://blog.csdn.net/Cris_0525/article/details/88545190'

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

s = requests.Session()
r = s.get(url, headers=header)
r.encoding = 'utf-8'
doc = r.text.encode("utf-8")

soup = BeautifulSoup(doc, 'html.parser')
body = soup.find('div', class_='blog-content-box')

with open(os.path.abspath('SEO/spider.html'), 'w') as f1:
    f1.write(str(body))
