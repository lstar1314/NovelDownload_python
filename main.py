#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import requests
import sys  
import re
import yaml


# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
class NovelDownload():
    #根据配置文件生成self属性
    def __init__(self):
        # self.context = ssl._create_unverified_context()
        self.getconfig()
        # for i in self.config.items() :
        #     setattr(self, i[0], i[1])
        pass
    #获取配置文件内容，返回dict
    def getconfig(self,configfile='./config.yml'):
        with open(configfile, 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.config = config
        for i in self.config.items() :
            setattr(self, i[0], i[1])
        return config
    #获取html
    def get(self,*args):
        
        url = self.BaseUrl + self.ExUrl
        r = requests.get(url,self.headers,verify=False)
        # r = requests.get(url)
        r.encoding = self.encoding
        t = r.text
        f1 = open('get.txt','w')
        f1.write(t)
        f1.close()
        print("get html success ! save to text.txt")
        pass
    #处理文本核心代码
    def _core(self,BaseUrl,Exurl):
        print(Exurl)
        url = BaseUrl + Exurl
        r = requests.get(url,self.headers,verify=False)
        # r = requests.get(url)
        r.encoding = self.encoding
        t = r.text
        NextUrl = re.findall(self.PatternNextUrl,t)[0]
        NovelTitle = re.findall(self.PatternTitle,t)[0]
        Content = re.findall(self.PatternContent,t)[0]
        #该部分根据参数ctreplace进行文本替换
        for i in range(0,len(self.ctreplace),2):
            Content = Content.replace(self.ctreplace[i],self.ctreplace[i+1])
        #已进行优化
        #########################
        # Content = Content.replace("</P><p>", "\n")
        # Content = Content.replace("&nbsp;", "")
        # Content = Content.replace("&nbsp", "")
        # Content = Content.replace("<br />", "")
        # Content = Content.replace("\\r\\n", "\\n")
        #########################
        return NextUrl,NovelTitle,Content
    
    #测试生成效果
    
    def test(self,*args):
        t = self._core(self.BaseUrl,self.ExUrl)
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
    
    #显示调用方法
    def help(self,*args):
        print('get:        \n    获取目标地址的html文件。')
        print('test:       \n    生成示例文档。')
        print('download:   \n    下载目标地址内容。')
        print('setconfig 参数名1 参数值1,参数值2,...:  \n    命令行设置配置参数。')
        print('getconfig:  \n    重新加载配置文件。')
        print('showconfig: \n    显示目前程序参数配置。')
        print('exit: \n    退出。')
        pass
    #命令行修改参数
    def setconfig(self,*args):
        for i in range(0,len(args),2):
            old = getattr(self,args[i])
            st = args[i+1]
            if ',' in args[i+1]:
                st = args[i+1].split(',')
            self.config[args[i]] = st
            setattr(self,args[i],st)
            print('{} 参数:由 {} --->调整为---> {}'.format(args[i],old,getattr(self,args[i])))
        
        pass
    
    #分级展示算法
    def _showconfig2(self,config,e=0):
        for key,value in config.items():
            # print(value,type(value))
            if isinstance(value,dict) :
                print('----'*e,end='')
                print('{} : '.format(key))
                e = e + 1
                e = self._showconfig2(value,e)
            else:
                print('----'*e,end='')
                print('{} : {}'.format(key,value))
        return e -1

    #显示的配置文件内容
    def showconfig(self,*args):
        self._showconfig2(self.config)

    #循环下载
    def download(self,*args):
        print('正在下载...')
        ex = self.ExUrl
        while 1 :
            t = self._core(self.BaseUrl,ex)
            NovelTitle = t[1]
            Content = t[2]
            f1 = open(self.SaveFile,'a+')
            f1.write(NovelTitle)
            f1.write(Content)
            f1.write("\n")
            f1.close()
            print(NovelTitle)
            time.sleep(0.1)
            ex = t[0]
    #退出
    def exit(self,*args):
        sys.exit(0)
        pass

if __name__=="__main__":
    a = NovelDownload()
    while 1 :
        try:
            i = input("请输入命令：").split(" ")
            # print(i)
            a.getconfig('./config.yml')
            getattr(a, i[0]) (*i[1:])
            print('\n')
        except Exception as e:
            print("执行失败，请检查后重新输入！")
            print('error : {}'.format(e))
            print('\n')

        
