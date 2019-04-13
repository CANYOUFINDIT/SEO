#!/usr/bin/env python
# coding:utf-8

import os,sys, commands
import requests
from bs4 import BeautifulSoup
import re

programme_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
} #定义头文件，伪装成浏览器
s = requests.Session()

# 在百度中搜索CSDN博客，返回博客超链接列表
def spider_csdn(word):
    url = 'http://www.baidu.com.cn/s?wd=CSDN {0}&pn=0'.format(word) 
    r = s.get(url, headers=headers)
    r.encoding = 'utf-8'
    doc = r.text.encode("utf-8")
    soup = BeautifulSoup(doc, 'html.parser')
    tagh3 = soup.find_all('h3')
    for h3 in tagh3:
        text = h3.find('a').get_text()
        href = h3.find('a').get('href')
        baidu_url = requests.get(url=href, headers=headers, allow_redirects=False)
        real_url = baidu_url.headers['Location']  #得到网页原始地址
        url_obj = re.match( r'https://blog.csdn.net/(.*)/article/details/(.*)', real_url, re.M|re.I)
        if url_obj:
            programme_list.append([text, real_url])


# 爬取指定url的博客内容
def csdn(request_url):
    r = s.get(request_url, headers=headers)
    r.encoding = 'utf-8'
    doc = r.text.encode("utf-8")
    soup = BeautifulSoup(doc, 'html.parser')
    print "\033[22;47m===================================================================\033[0m"
    print "\033[22;47m==\033[0m\n"
    title = soup.find('h1', class_='title-article')
    print "文章标题:"
    print "\033[33m" + title.get_text() + "\033[0m"
    print request_url
    print "时间:"
    time = soup.find('span', class_='time')
    print time.get_text() + "\n"
    print "内容:"
    body = soup.find('div', id='content_views')
    print '\033[22;37m' + body.get_text().strip() + '\033[0m\n'
    print "\033[22;47m==\033[0m"
    print "\033[22;47m===================================================================\033[0m\n"


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
        print "Unknown language"
        return '' # Unknown language


def answer_list():
    for i, x in enumerate(programme_list):
        print i+1, '\033[22;32m' + x[0] + '\033[0m'

def process():
    try:
        program_num = raw_input("请输入解决方案序号 [方案列表(l)/退出(enter)] ")
        if program_num == "l" or program_num == "L":
            answer_list()
            process()
        elif program_num == "":
            return
        else:
            csdn(programme_list[int(program_num)-1][1])
            process()
            return
    except:
        print "请输入正确的指令"
        process()

def main():
    try:
        if len(sys.argv) == 1:
            print "文件路径为空！"
        else:
            output = get_language(sys.argv[1].lower())

        if output[0] != 0:
            error = output[1]
            n_list = [i.start() for i in re.finditer('\n', error)]
            error = error[n_list[-1]:].strip('\n')
            answer1 = raw_input("\n是否开启面向搜索引擎编程? (Y/Other keys) ")
            if answer1 == "Y" or answer1 == "y" or answer1 == "yes":
                answer2 = raw_input("自动填充报错信息? (Y/Other keys) ")
                if answer2 != "Y" and answer2 != "y" and answer2 != "yes":
                    error = raw_input("请输入报错信息：")
                #spider_baidu(error)
                spider_csdn(error)
                answer_list()
                process()
    except:
        pass

main()