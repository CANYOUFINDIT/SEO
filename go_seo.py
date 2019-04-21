#!/usr/bin/env python
# coding:utf-8

import json
import os,sys, commands
import requests
from bs4 import BeautifulSoup
import re
import npyscreen


reload(sys)
sys.setdefaultencoding('utf-8')

programme_list = []
result = []
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
            os.system('./'+head)
        return output, 'C'
    else:
        print "Unknown language"
        return '' # Unknown language


# 爬取指定url的博客内容
def csdn(request_url):
    result = []
    r = s.get(request_url, headers=headers)
    r.encoding = 'utf-8'
    doc = r.text.encode("utf-8")
    soup = BeautifulSoup(doc, 'html.parser')
    title = soup.find('h1', class_='title-article')
    #time = soup.find('span', class_='time')
    # 阅读量
    reading_volume = soup.find('span', class_='read-count')
    body = soup.find('div', id='content_views')
    result.append(title.get_text().encode('utf-8'))
    result.append(request_url)
    #result.append('时间：'+ time.get_text().encode('utf-8'))
    result.append(reading_volume.get_text())
    result.append(body .get_text().strip().encode('utf-8'))
    return result


def smf(request_url):
    result = []
    r = s.get(request_url, headers=headers)
    r.encoding = 'utf-8'
    doc = r.text.encode("utf-8")
    soup = BeautifulSoup(doc, 'html.parser')
    head = soup.find('div', class_='post-topheader__info mb15')
    # 问题标题
    title = head.find('h1', class_ = 'h2 post-topheader__info--title')
    result.append('标题：' + title.get_text().strip().encode('utf-8'))
    result.append('原文链接：' + request_url)
    # 阅读量
    reading_volume = head.find('span')
    result.append('阅读量：' + reading_volume.get_text().encode('utf-8'))
    # 问题描述
    body = soup.find('div', class_='question fmt')
    result.append('问题描述：\n' + body.get_text().encode('utf-8'))
    # 回答数量
    answer_num = soup.find('div', class_='pb15')
    result.append('回答数量：' + answer_num.string.encode('utf-8'))
    # 是否有已采纳的回答
    is_resolved = soup.find('article', class_='clearfix widget-answers__item accepted')
    if is_resolved:
        fmt = is_resolved.find('div', class_='answer fmt')
        result.append('已采纳的回答：' + fmt.get_text().encode('utf-8') +'\n\n' )
    else :
        result.append('已采纳的回答：无\n\n')
    # 其他回答
    answer = soup.find_all('article', class_='clearfix widget-answers__item')
    other_answer = '其他回答：\n'
    for ans in answer:
        fmt = ans.find('div', class_='answer fmt')
        #result.append('其他回答：' + fmt.get_text().encode('utf-8'))
        other_answer = other_answer + fmt.get_text().encode('utf-8') + '\n'
        other_answer = other_answer + '-----------------------------------回答分割线-----------------------------------\n'
    result.append(other_answer)
    return result

# CSDN文章界面
class CSDNForm(npyscreen.ActionForm):
    def create(self):
        self.name = 'CSDN BLOG'
        self.title = self.add(npyscreen.FixedText, name='标题', value = "")
        self.link = self.add(npyscreen.FixedText, name='原文链接', value = "")
        self.reading_volume = self.add(npyscreen.FixedText, name='阅读量', value = "")
        self.body = self.add(npyscreen.MultiLineEdit,name ="正文",value = "",max_height=None, rely=9)


    def beforeEditing(self):
        result = self.parentApp.getForm('MAIN').result
        self.title.value = result[0]
        self.link.value = result[1]
        self.reading_volume.value = result[2]
        self.body.value = result[3]

    def on_ok(self):
        self.parentApp.switchForm('MAIN')
        

    def on_cancel(self):
        self.parentApp.switchForm(None)

# 文章界面
class smfForm(npyscreen.ActionForm):
    def create(self):
        self.name = 'SegmentFual ANSWER'
        self.title = self.add(npyscreen.FixedText, name='标题', value = "")
        self.link = self.add(npyscreen.FixedText, name='原文链接', value = "")
        self.reading_volume = self.add(npyscreen.FixedText, name='阅读量', value = "")
        self.answer_num = self.add(npyscreen.FixedText, name='回答数量', value = "")
        self.question = self.add(npyscreen.MultiLineEdit,name ="问题描述",value = "",max_height=None, rely=9)

    def beforeEditing(self):
        result = self.parentApp.getForm('MAIN').result
        self.title.value = result[0]
        self.link.value = result[1]
        self.reading_volume.value = result[2]
        self.question.value = result[3] + '\n' + result[5] + '\n' + result[6] + '\n'
        self.answer_num.value = result[4]

    def on_ok(self):
        self.parentApp.switchForm('MAIN')
        

    def on_cancel(self):
        self.parentApp.switchForm(None)

# 目录界面
class ListForm(npyscreen.ActionForm):
    def create(self):
        self.name = "LIST"
        self.parentApp.value = ""
        self.num = None
        self.result = []
        lists = []
        for menu in programme_list:
            menu_mem = menu[0]
            lists.append(menu_mem)
        self.ms = self.add(npyscreen.TitleSelectOne, max_height=None, value = [0,], name="Pick One",
                values = lists, scroll_exit=True)

    def beforeEditing(self):
        self.num = None
        self.result = []

    def on_ok(self):
        self.result = []
        self.num = self.ms.value[0]
        if self.num is None :
            print "num can't be null"
        elif programme_list[int(self.num)-1][2] == 'segmentfual':
            self.result = smf(programme_list[int(self.num)-1][1])
            self.parentApp.switchForm('SMFFORM')
        elif programme_list[int(self.num)-1][2] == 'CSDN':
            self.result = csdn(programme_list[int(self.num)-1][1])
            self.parentApp.switchForm('CSDNFORM')

    def on_cancel(self):
        self.parentApp.switchForm(None)

# 界面联系
class goApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", ListForm, name = "LIST")
        self.addForm("CSDNFORM", CSDNForm, name = "CSDN BLOG")
        self.addForm("SMFFORM", smfForm, name = "SegmentFual ANSWER")

def main():
    try:
        # 第一步，获取文件扩展名，并在终端中执行，显示运行结果
        if len(sys.argv) == 1:
            print "文件路径为空！"
        else:
            output, tail = get_language(sys.argv[1])
            
        # 第二步，解析错误，获得索引关键字error
        if output[0] != 0:
            error = output[1]
            if tail == "java":
                n_list = re.search(r'.*error:(.*)', error.split('\n')[0])
                error = n_list.group(1) if n_list else None
            else:
                n_list = [i.start() for i in re.finditer('\n', error)]
                error = error[n_list[-1]:].strip('\n')
            # 第三步，通过关键字运行爬虫
            answer1 = raw_input("\n是否开启面向搜索引擎编程? (Y/Other keys) ")
            if answer1 == "Y" or answer1 == "y" or answer1 == "yes":
                answer2 = raw_input("自动填充报错信息? (Y/Other keys) ")
                if answer2 != "Y" and answer2 != "y" and answer2 != "yes":
                    error = raw_input("请输入报错信息：")
                # 爬取数据，得到解决方案的链接和标题的列表
                spider('segmentfual', tail, error)
                spider('CSDN', tail, error)
                goApp().run()
    except:
        print "seo error"

main()