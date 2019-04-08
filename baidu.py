#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os

question = raw_input("Please enter your question:\n")

request_url = "https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd={0}&rsv_pq=f58cf5d100008816&rsv_t=95ac5g6jee0WeJYqjnGAt95WVwtYncO9YdHkgIMPLRD5WSk3BEzTtI1WM9c&rqlang=cn&rsv_enter=1&rsv_sug3=3&rsv_sug1=3&rsv_sug7=101&rsv_sug2=0&prefixsug={1}&rsp=3&inputT=2764&rsv_sug4=11740&rsv_sug=1".format(question, question)

header = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Cookie': 'BAIDUID=5F29791CDF99AA281318B150B46C8331:FG=1; BIDUPSID=5F29791CDF99AA281318B150B46C8331; PSTM=1543833700; BD_UPN=123353; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1440_21098_28775_28721_28558_28584_28604_28625_28605; delPer=0; BD_CK_SAM=1; PSINO=2; H_PS_645EC=373019KYllDgk%2FtEKnTgigg1ZORaznZQd%2BpW4bGinJiJeFGUtKdJMPObjX4; BDSVRTM=125; WWW_ST=1554603999782',
'Host': 'www.baidu.com',
'is_pbs': 'HHHHHHHHHHHHHHHHHHHHHHH',
'is_referer': 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=HHHHHHHHHHHHHHHHHHHHHHH&oq=HHHHHHHHHHHHHHHHHHHHHHH&rsv_pq=9248985e000050a2&rsv_t=d6b1h38e4lkDTgGQz941QmJH%2BVwFzT9%2FOgQ05VtHLoVtCW4sapgPCvKoORU&rqlang=cn&rsv_enter=0&prefixsug=HHHHHHHHHHHHHHHHHHHHHHH&rsp=3&rsv_sug=1&bs=HHHHHHHHHHHHHHHHHHHHHHH',
'is_xhr': '1',
'Referer': 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=HHHHHHHHHHHHHHHHHHHHHHH&oq=HHHHHHHHHHHHHHHHHHHHHHH&rsv_pq=b513924f0001422a&rsv_t=373019KYllDgk%2FtEKnTgigg1ZORaznZQd%2BpW4bGinJiJeFGUtKdJMPObjX4&rqlang=cn&rsv_enter=0&prefixsug=HHHHHHHHHHHHHHHHHHHHHHH&rsp=3&rsv_sug=1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
}

s = requests.Session()
r = s.get(request_url, headers=header)
r.encoding = 'utf-8'
doc = r.text.encode("utf-8")
#print doc
'''
with open(os.path.abspath('baidu.html'), 'w') as f1:
    f1.write(doc) '''

soup = BeautifulSoup(doc, 'html.parser')

# 清空html内容
with open(os.path.abspath('爬虫/baidu.html'), 'w') as f1:
    f1.truncate()

div = soup.find_all('div', class_='result c-container')
for div in div:
    with open(os.path.abspath('爬虫/baidu.html'), 'a') as f1:
        f1.write(str(div.a)+"\n<br>\n")
