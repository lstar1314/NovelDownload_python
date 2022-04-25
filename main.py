#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import requests
import sys  
import re
import yaml

class NovelDownload():
    #根据配置文件生成self属性
    def __init__(self):
        self.config = self.getconfig()
        for i in self.config.items() :
            setattr(self, i[0], i[1])
        
        pass
    #获取配置文件内容，返回dict
    def getconfig(self,configfile='./config.yml'):
        with open(configfile, 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
        return config
        # print(result, type(result))
    #获取html
    def get(self,*args):
        url = self.BaseUrl + self.ExUrl
        r = requests.get(url,self.headers)
        r.encoding = self.encoding
        t = r.text
        f1 = open('get.txt','w')
        f1.write(t)
        f1.close()
        print("get html success ! save to text.txt")
        pass
    #处理文本核心代码
    def core(self,BaseUrl,Exurl):
        # print(BaseUrl,Exurl)
        # print('-'*20)
        url = BaseUrl + Exurl
        r = requests.get(url,self.headers)
        r.encoding = self.encoding
        t = r.text
        NextUrl = re.findall(self.Pattern['PatternNextUrl'],t)[0]
        NovelTitle = re.findall(self.Pattern['PatternTitle'],t)[0]
        Content = re.findall(self.Pattern['PatternContent'],t)[0]
        #该部分根据自己需要进行修改调整
        #########################
        Content = Content.replace("\\t", "")
        Content = Content.replace("&nbsp;", "")
        Content = Content.replace("&nbsp", "")
        Content = Content.replace("<br />", "")
        Content = Content.replace("\\r\\n", "\\n")
        #########################
        return NextUrl,NovelTitle,Content

    #测试生成效果
    def test(self,*args):
        t = self.core(self.BaseUrl,self.ExUrl)
        NextUrl = t[0]
        NovelTitle = t[1]
        Content = t[2]
        f1 = open('test.txt','w')
        f1.write(NextUrl)
        f1.write(NovelTitle)
        f1.write(Content)
        f1.close()
        print("get test success ! save to test.txt")
        pass

    def help(self,*args):
        print('get:        获取目标地址的html文件。')
        print('test:       生成示例文档。')
        print('download:   下载目标地址内容。')
        print('setconfig:  设置临时配置参数。')
        pass

    def setconfig(self,**kwargs):
        
        pass

    #循环下载
    def download(self,*args):
        print('正在下载...')
        ex = self.ExUrl
        while 1 :
            t = self.core(self.BaseUrl,ex)
            NovelTitle = t[1]
            Content = t[2]
            f1 = open(self.SaveFile,'a+')
            f1.write(NovelTitle)
            f1.write(Content)
            f1.close()
            print(NovelTitle)
            ex = t[0]

if __name__=="__main__":
    a = NovelDownload()
    while 1 :
        try:
            i = input("请输入命令：").split(" ")
            print(i)
            getattr(a, i[0]) (i[1:])
        except Exception as e:
            print(e)
            print("执行失败，请检查后重新输入！")

        
