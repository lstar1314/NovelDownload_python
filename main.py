#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import requests
import sys  
import re
# reload(sys)  
# sys.setdefaultencoding('utf8')   
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate",
}
# url = 'https://dijiubook.net/29_29946/11606834.html'
# r=requests.get(url,headers)
# r.encoding='gbk'
# t=r.text
# # print(t)
# f1 = open('test.txt','w')
# # f1.write(t)
# NextUrl = re.findall("章节目录</a>.*<a href=\"(.*?)\">下一章</a>",t)
# print(NextUrl)
# NovelTitle = re.findall("<h1>(.*?)</h1>",t)
# print(NovelTitle)
# f1.write(NovelTitle[0])
# Content = re.findall('</br>([\s\S]*)</br>',t)
# # print(Content)
# Content[0] = Content[0].replace("\\t", "")
# Content[0] = Content[0].replace("&nbsp;", "")
# Content[0] = Content[0].replace("&nbsp", "")
# Content[0] = Content[0].replace("<br />", "")
# Content[0] = Content[0].replace("\\r\\n", "\\n")
# # print(Content[0])
# f1.write(Content[0])

BaseUrl = 'https://dijiubook.net'
ProUrl = '/29_29946/11606834.html'

while 1:
    try:
        f1 = open('DZJH.txt','a+')
        url = BaseUrl + ProUrl
        r=requests.get(url,headers)
        r.encoding='gbk'
        t=r.text
        NextUrl = re.findall("章节目录</a>.*<a href=\"(.*?)\">下一章</a>",t)
        print(NextUrl)
        NovelTitle = re.findall("<h1>(.*?)</h1>",t)
        print(NovelTitle)
        f1.write(NovelTitle[0])
        Content = re.findall('</br>([\s\S]*)</br>',t)
        Content[0] = Content[0].replace("\\t", "")
        Content[0] = Content[0].replace("&nbsp;", "")
        Content[0] = Content[0].replace("&nbsp", "")
        Content[0] = Content[0].replace("<br />", "")
        Content[0] = Content[0].replace("\\r\\n", "\\n")
        f1.write(Content[0])
        f1.close()
        ProUrl = NextUrl[0]
        time.sleep(0.1)
    except Exception as e:
        print(e)
        filename = input("继续？：")
    pass