#!/usr/bin/env python
# coding:utf-8

import os,sys, commands
import requests
from bs4 import BeautifulSoup
import re

#num = 0
programme_list = []

def spider_csdn(question):
    #global num
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

    soup = BeautifulSoup(doc, 'html.parser')
    dl = soup.find_all('dl', class_='search-list J_search')
    for dl in dl:
        if dl.span.get_text().encode('utf-8') == "博客": #or dl.span.get_text().encode('utf-8') == "问答"
            programme_list.append(dl.a)
            #print num , '\033[1;32m' + dl.a.get_text() + '\033[0m\n- [\033[1;31m' + dl.a['href'] + '\033[0m]'
            #num += 1


def spider_baidu(question):
    #global num
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
    soup = BeautifulSoup(doc, 'html.parser')
    div = soup.find_all('div', class_='result c-container')
    for div in div:
        programme_list.append(div.a)
        #print num , '\033[1;32m' + div.a.get_text() + '\033[0m\n- [\033[1;31m' + div.a['href'] + '\033[0m]'
        #num += 1


def spider_csdn_blog(url):
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
    print "--------------------------------------------------------------------------"
    # 标题
    title = soup.find('h1', class_='title-article')
    print '\033[1;34m' + title.get_text() + '\033[0m\n- [ \033[1;33m' + url + '\033[0m ]'
    time = soup.find('span', class_='time')
    print time.get_text()
    body = soup.find('div', id='content_views')
    print body.get_text()
    print "--------------------------------------------------------------------------"


# 返回语言
def get_language(file_path):

    if file_path.endswith(".py"):
        output = commands.getstatusoutput('python {}'.format(file_path))
        print output[1]
        #execution = os.popen('python {}'.format(file_path)).read().strip()  #返回输出结果
        return output
    elif file_path.endswith(".js"):
        return "node"
    elif file_path.endswith(".go"):
        return "go run"
    elif file_path.endswith(".rb"):
        return "ruby"
    elif file_path.endswith(".java"):
        return 'javac' # Compile Java Source File 编译JAVA源文件
    elif file_path.endswith(".class"):
        return 'java' # Run Java Class File 运行JAVA类文件
    elif file_path.endswith(".c"):
        output = commands.getstatusoutput("gcc {0} -o {1}".format(file_path, os.path.splitext(file_path)[0]))  
        #execution = os.popen("gcc {0} -o {1}".format(sys.argv[1].lower(), os.path.splitext(file_path)[0])).read().strip()
        if output[0] == 0:
            os.system(os.path.splitext(file_path)[0])
        return output
    else:
        return '' # Unknown language


def answer_list():
    for i, x in enumerate(programme_list):
        print i+1, '\033[1;32m' + x.get_text() + '\033[0m\n'

def process():      
    #for i, x in enumerate(programme_list):
        #print i+1, '\033[1;32m' + x.get_text() + '\033[0m\n'
        #print '- ', x['href']
        #print
    program_num = raw_input("请输入解决方案序号 [方案列表(l)/退出(enter)] ")
    #print programme_list[i-1]['href']
    if program_num == "e" or program_num == "":
        return
    elif program_num == "l" or program_num == "L":
        answer_list()
        process()
    else:
        spider_csdn_blog(programme_list[int(program_num)-1]['href'])
        #answer3 = raw_input("继续(c)/退出(other keys) ")
        #print ''
        #if answer3 == 'c' or answer3 == 'C':
        process()
        return


try:
    if len(sys.argv) == 1:
        print "文件路径为空！"
    else:
        output = get_language(sys.argv[1].lower())

    if output[0] == 256:
        error = output[1]
        n_list = [i.start() for i in re.finditer('\n', error)]
        error = error[n_list[-1]:].strip('\n')
        answer1 = raw_input("\n是否开启面向搜索引擎编程? (Y/n) ")
        if answer1 == "Y" or answer1 == "y" or answer1 == "yes":
            answer2 = raw_input("自动填充报错信息? (Y/n) ")
            if answer2 != "Y" and answer2 != "y" and answer2 != "yes":
                error = raw_input("请输入报错信息：")
            #spider_baidu(error)
            spider_csdn(error)
            answer_list()
            process()
except:
    pass