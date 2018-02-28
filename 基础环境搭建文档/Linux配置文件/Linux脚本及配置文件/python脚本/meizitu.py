#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import urllib.request


urls = ['http://www.meizitu.com/a/sifang_5_{}.html'.format(str(pages_num)) for pages_num in range(1, 14)]
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Cookie': 'UM_distinctid=15ab669b2430-0242b4a2769a-6a11157a-15f900-15ab669b24442; bdshare_firstime=1489119070954; safedog-flow-item=7C127904395598B5A6C3082FDD56D04D; CNZZDATA30056528=cnzz_eid%3D653286371-1489115686-%26ntime%3D1489393614'
}
dirpath = "d:/down_imgs/photoAlbum/"   # 定义图片的下载位置，目录需存在
serial = 1

# get main html sound code
def get_page(url):
    req = requests.get(url, headers=header)
    print("已打开图片分类页")
    time.sleep(3)
    html = BeautifulSoup(req.text, 'lxml')
    links_cont = html.find_all('div', class_="pic")
    url_links = []
    # 提取图片的合集页面
    print("正在提取当前分类页所有图片合集url")
    for page_links in links_cont:
        url_links.append(page_links.find('a').get('href'))
    return url_links


# open pic detail page
def detail_page(detail_link):
    detail_req = requests.get(detail_link, headers=header)
    time.sleep(3)
    print("已打开图片合集页")
    detail_html = BeautifulSoup(detail_req.text, 'lxml')
    pic_urls = detail_html.select('#picture > p > img')
    pic_url_list = []
    print("正在提取图片合集页所有图片url")
    for pic_url in pic_urls:
        pic_url_list.append(pic_url.get('src'))
    # 提取图片的url，即下载地址
    return pic_url_list


# download images
def download(download_link):
    file_path = dirpath + time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    # 可在此处加目录存在判断，及二级目录创建，或单独定义函数
    try:  # 进行图片下载操作，出现错误匹配except
        req_img = urllib.request.Request(download_link, None, header)
        print("正在请求打开图片url: %s" % download_link)
        time.sleep(4)
        open_img = urllib.request.urlopen(req_img, timeout=20)
        time.sleep(1)
        print("正在准备保存图片")
        read_img = open_img.read()
        with open(file_path + download_link.split('/')[-1], 'wb') as f:
            f.write(read_img)
            f.close()
            open_img.close()
            print("已将图片保存至: %s" % file_path + download_link.split('/')[-1])
            time.sleep(1)
    except urllib.error.HTTPError:  # Open url error: 403, 404, 500, 502
        print("Error: open url %s error, To prepare download the next images ..." % download_link)
        time.sleep(5)
    except urllib.request.HTTPError:  # Request url Error: 403, 404, 500, 502
        print("Error: Connect url %s error, To prepare download the next images ..." % download_link)
        time.sleep(5)


if __name__ == "__main__":
    for url in urls:   # 循环图片分类url
        detail_links = get_page(url)    # 调用函数打开图片分类url
        for detail_link in detail_links:  # 取出单个图片的所有下载url
            download_links = detail_page(detail_link)   # 调用函数从图片合集url获取图片详情页url
            for download_link in download_links:   # 循环传递图片单个url到download_link变量
                download(download_link)   # 循环下载传递进来的图片下载链接
                print("--- 已成功保存了%s张图片 ---" % serial)
                serial += 1
            print('已成功保存一套图片 ^_^')
            print("---------------------------------")