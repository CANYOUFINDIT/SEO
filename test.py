# coding:utf-8

import os
import subprocess
import commands
#os.system()
#os.popen().read().strip()

#上面2种方法 是python 执行终端/控制台 命令的常见方法
#os.system('python a.py') #执行成功 返回 0 
'''print "a"
ping = os.popen('python a.py').read().strip()  #返回输出结果
#注：os.system() 执行完成 会关闭 所以当执行后续 命令需要依赖前面的命令时，请将多条命令写到一个 os.system() 内
print "b"
if ping == "":
    print "error"
'''
'''#但 这个方法执行的时候 是无法交互的 比如说  命令权限不够 需要输入登陆密码 可使用下面这种方法
import pexpect
ch = pepect.spwn('命令')
ch.expect('Password:')
ch.sendline('密码')
'''
'''
p = subprocess.Popen('python /home/fty/workspace/开源社区/rebound-master/a.py',shell=True,stdout=subprocess.PIPE)  
out,err = p.communicate()  
print out
print err
for line in out.splitlines():  
    print line  '''

output = commands.getstatusoutput('gcc /home/fty/workspace/开源社区/rebound-master/hello.c -o hello')  
print  type(output[0])