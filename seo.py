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
def spider(blog, language, word):
    url = 'http://www.baidu.com.cn/s?wd={0} {1} {2}&pn=0'.format(blog, language, word) 
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
        if blog == "CSDN":
            url_obj = re.match( r'https://blog.csdn.net/(.*)/article/details/(.*)', real_url, re.M|re.I)
        elif blog == "segmentfual":
            url_obj = re.match( r'https://segmentfault.com/q/(.*)', real_url, re.M|re.I)
        if url_obj:
            programme_list.append([text, real_url, blog])


# 爬取指定url的博客内容
def csdn(request_url):
    r = s.get(request_url, headers=headers)
    r.encoding = 'utf-8'
    doc = r.text.encode("utf-8")
    soup = BeautifulSoup(doc, 'html.parser')
    print "\033[1;22;47m=================================================================\033[0m"
    print "\033[22;47m==\033[0m"
    title = soup.find('h1', class_='title-article')
    print "\033[33m" + title.get_text() + "\033[0m"
    print request_url
    time = soup.find('span', class_='time')
    print time.get_text() + "\n"
    body = soup.find('div', id='content_views')
    print '\033[22;37m' + body.get_text().strip() + '\033[0m\n'
    print "\033[22;47m==\033[0m"
    print "\033[22;47m===================================================================\033[0m\n"


def show_answer(fmt):
    for a in fmt:
        if a.name == "pre":
            print '\033[33m' + a.get_text() + '\033[0m'
        elif a.name == "code":
            print '\033[35m' + a.get_text() + '\033[0m'
        else:
            for a in a:
                print a

def smf(request_url):
    r = s.get(request_url, headers=headers)
    r.encoding = 'utf-8'
    doc = r.text.encode("utf-8")
    soup = BeautifulSoup(doc, 'html.parser')
    print "\033[1;22;47m=================================================================\033[0m"
    print "\033[22;47m==\033[0m"
    head = soup.find('div', class_='post-topheader__info mb15')
    # 问题标题
    title = head.find('h1', class_ = 'h2 post-topheader__info--title')
    print "\033[34m标题:", title.get_text().strip(), "\033[0m"
    print request_url
    # 阅读量
    reading_volume = head.find('span')
    print reading_volume.get_text() , "阅读量"
    # 问题描述
    body = soup.find('div', class_='question fmt')
    show_answer(body)
    print "==================================回答======================================="
    # 回答数量
    answer_num = soup.find('div', class_='pb15')
    print answer_num.string
    # 是否有已采纳的回答
    is_resolved = soup.find('article', class_='clearfix widget-answers__item accepted')
    if is_resolved:
        print "---------------------------------------------------------------------------"
        print "\033[22;32m已采纳的回答：\033[0m"
        fmt = is_resolved.find('div', class_='answer fmt')
        show_answer(fmt)
    # 其他回答
    answer = soup.find_all('article', class_='clearfix widget-answers__item')
    for ans in answer:
        print "------------------------------其他回答--------------------------------------"
        fmt = ans.find('div', class_='answer fmt')
        show_answer(fmt)
    print "\033[22;47m==\033[0m"
    print "\033[1;22;47m=================================================================\033[0m\n"
  

# 返回语言
def get_language(file_path):
    # 文件后缀名
    head = os.path.splitext(file_path)[0]
    tail = os.path.splitext(file_path)[-1]
    if file_path.endswith(".py"):
        output = commands.getstatusoutput('python {}'.format(file_path))
        print output[1]
        return output, 'python'
    elif file_path.endswith(".java"):
        output = commands.getstatusoutput("javac {0}".format(file_path))
        print output[1]
        return output, 'java' # Compile Java Source File 编译JAVA源文件
    elif file_path.endswith(".class"):
        output = commands.getstatusoutput("java {0}".format(head))
        print output[1]
        return output, tail # Run Java Class File 运行JAVA类文件
    elif file_path.endswith(".c"):
        output = commands.getstatusoutput("gcc {0} -o {1}".format(file_path, head))  
        if output[0] == 0:
            os.system(head)
        return output, 'C'
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
            if programme_list[int(program_num)-1][2] == 'segmentfual':
                smf(programme_list[int(program_num)-1][1])
            elif programme_list[int(program_num)-1][2] == 'CSDN':
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
            output, tail = get_language(sys.argv[1])

        if output[0] != 0:
            error = output[1]
            if tail == "java":
                pass
            else:
                n_list = [i.start() for i in re.finditer('\n', error)]
                error = error[n_list[-1]:].strip('\n')
            answer1 = raw_input("\n是否开启面向搜索引擎编程? (Y/Other keys) ")
            if answer1 == "Y" or answer1 == "y" or answer1 == "yes":
                answer2 = raw_input("自动填充报错信息? (Y/Other keys) ")
                if answer2 != "Y" and answer2 != "y" and answer2 != "yes":
                    error = raw_input("请输入报错信息：")
                spider('segmentfual', tail, error)
                spider('CSDN', tail, error)
                print error
                print tail
                answer_list()
                process()
    except:
        pass

main()