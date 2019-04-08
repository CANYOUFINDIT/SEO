#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os

question = raw_input("please enter your question:\n")

request_url = "https://so.csdn.net/so/search/s.do?p=&q={0}&t=&domain=&o=&s=&u=&l=&f=".format(question)
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'TY_SESSION_ID=130ea2cc-c58f-4bfc-ae2f-d63981aaa980; JSESSIONID=9FA17B31B7231E11B3E40300F97854A5; uuid_tt_dd=10_30763140180-1543833936884-183079; dc_session_id=10_1543833936884.782145; ARK_ID=JS21afbef72ea23fb8ed38735da13834cf21af; UM_distinctid=167ea9b4f1d1e0-0fd55a57dee86f-18211c0a-1fa400-167ea9b4f1ff2; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=1788*1*PC_VC!6525*1*10_30763140180-1543833936884-183079; SESSION=c38de3f9-a82c-44e3-9fda-2985ebb5e51f; __yadk_uid=6YUj8tzELm0cgItzMcbIFJpJzJFfmqYt; firstDie=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1554362591,1554364502,1554364556,1554364586; c-login-auto=3; dc_tos=ppfg5g; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1554365573',
    'upgrade-insecure-requests': '1',
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