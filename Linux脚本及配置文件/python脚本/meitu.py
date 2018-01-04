#/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib,os,re,getpass
import urllib.request as Req
User = getpass.getuser()
Dir = r'C:\Users\%s\Desktop\Image User' % User
def FileDownload(path):
    if not os.path.isdir(Dir):
        os.mkdir(Dir)
    Pos = path.rindex('/')
    t = os.path.join(Dir,path[Pos+1:])
    return t
if __name__ == "__main__":
    #url = 'https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%C3%C0%C5%AE&fr=ala&ala=1&alatpl=cover&pos=0&hs=2&xthttps=111111'
    url = 'http://www.ivrfans.cn/'
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    }
    req = Req.Request(url,headers=headers)
    WebPage = Req.urlopen(req)
    data = WebPage.read()
    for link,t in set(re.findall(r'(http:[^\s]*?(jpg|png|gif))',str(data))):
        print(link)
        try:
            Req.urlretrieve(link,FileDownload(link))
        except:
            print('This URL Fial')
