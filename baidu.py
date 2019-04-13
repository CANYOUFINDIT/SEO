#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import re
import urllib, urllib2

word = 'CSND 安装pip时报错'
url = 'http://www.baidu.com.cn/s?wd={0}&pn=0'.format(word) 
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
} #定义头文件，伪装成浏览器

s = requests.Session()
r = s.get(url, headers=headers)
r.encoding = 'utf-8'
doc = r.text.encode("utf-8")

all = open('/home/fty/workspace/开源社区/rebound-master/baidu.html', 'a')
soup = BeautifulSoup(doc, 'lxml')
tagh3 = soup.find_all('h3')
for h3 in tagh3:
    href = h3.find('a').get('href')
    baidu_url = requests.get(url=href, headers=headers, allow_redirects=False)
    real_url = baidu_url.headers['Location']  #得到网页原始地址
    url_obj = re.match( r'https://blog.csdn.net/(.*)/article/details/(.*)', real_url, re.M|re.I)
    if url_obj:
        all.write(real_url + '\n')