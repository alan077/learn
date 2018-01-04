#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests as req
import re,os,time
#定义HTTP请求参数
url = 'https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%C3%C0%C5%AE&fr=ala&ala=1&alatpl=cover&pos=0&hs=2&xthttps=111111'
url = 'http://www.ivrfans.cn/'
Urllist = []
headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
}
stream = True
allow_redirects = True
verify = True
timeout = 10
#定义下载路径及图片下载功能
def Donwload(Urllist):
    #定义下载目录
    DownLoad_Path = os.getcwd() + r'\Image'
    if not os.path.isdir(DownLoad_Path):
        os.mkdir(DownLoad_Path)
        print('创建图片下载目录%s'% DownLoad_Path)
    else:
        print('图片下载目录%s' % DownLoad_Path)
    for i in Urllist:
        ImageName =  i.split('/')[-1]
        DownLoad_Image = os.path.join(DownLoad_Path,ImageName)
        #print(DownLoad_Image)
        try:
            r = req.get(url=i, headers=headers, stream=stream, allow_redirects=allow_redirects, verify=verify,timeout=timeout)
        except:
            print("\033[1;31;40m无法访问%s \033[0m " % i)
        if r.status_code == 200:
            try:
               with open(DownLoad_Image, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
                    print("%s %s 图片下载成功" % (time.ctime(),DownLoad_Image))
            except:
                print('%s %s 图片下载失败'% (time.ctime(),DownLoad_Image))
    print("一共下载图片%s张，下载目录%s", (len(os.listdir(DownLoad_Path)),DownLoad_Path))
#定义爬取网站
def Req(url):
    try:
        r = req.get(url,headers=headers,stream=stream,allow_redirects=allow_redirects,verify =verify)
        REQ = r.text
        New_url = set(re.findall(r'(http:[^\s]*?(jpg|png|gif))',str(REQ)))
        for Url, Format in New_url:
            Urllist.append(Url)
    except:
        print("\033[1;31;40m 无法访问%s \033[0m " % url)

if __name__ == "__main__":
    Req(url)
    Donwload(Urllist)
