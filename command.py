#!/usr/bin/env python
# coding:utf-8
import os,sys

def get_language(file_path):
    """Returns the language a file is written in."""
    """              返回文件所使用的语言            """
    if file_path.endswith(".py"):
        return "python3"
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
        return "c"
    else:
        return '' # Unknown language

print sys.argv[1].lower()
language = get_language(sys.argv[1].lower())
print language

s = 'a.b'
print os.path.splitext(s)[0]