#coding: utf8
from util import *

import requests
import os, re, logging

global headers
headers = {"Host" : "www.jianshu.com",
"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0",
"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language" : "zh-CN,en-CA;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding" : "gzip, deflate, br",
"Referer" : "https://www.jianshu.com/u/5e65478eb27c",
"Connection" : "keep-alive"}

class Article(object):
    '''jianshu 简书'''
    
    def __init__(self, url):
        self.url = url
        self.get()
        self.save()
    
    def get(self):
        resp = requests.get(self.url, headers=headers)
        html = resp.text

        print(resp.url)
        ttl = re.search('class="article".*?<h1 class="title">(.*?)</h1>', html, re.DOTALL).group(1)
        self.title = ttl

        ctt = re.search('''<!-- 文章内容 -->(.*?)<!-- 如果是付费文章，未购买，则显示购买按钮 -->''', html, re.DOTALL).group(1)
        # 处理图片
        img_urls = re.findall("upload-images.jianshu.io/upload_images/.*?jpg|upload-images.jianshu.io/upload_images/.*?gif", html)
        ctt_alterimg = ctt.replace('//upload-images.jianshu.io/upload_images/','../Images/')
        
        # 替换 
        ctt_altimg = re.sub('<div class="image-package">.*?<div.*?<div.*?<div.*?(<img.*?/>).*?\
        (<div class="image-caption">.*?</div>)\s*?</div>', "\1\2", ctt_altimg, flags = re.DOTALL)
        self.content = ctt_alterimg

        # 下载图片
        prefix = './Images/'
        if not os.path.exists(prefix):
            os.makedirs(prefix)
        for imgurl in img_urls:
            fname = prefix + re.search("upload_images/(.*)",imgurl).group(1)
            imgurl = 'https://'+imgurl
            ir = requests.get(imgurl)
            sz = open(fname, 'wb').write(ir.content)

        # js 异步载入的评论, 暂不能处理
        try:
            cmt = re.search('''class="comment-list".*?/u/5e65478eb27c.*?class="author-tag".?class="comment-wrap"\
        (<p>.+?</p>)<div class="tool-gr''', html, re.DOTALL).group(1)
        except:
            self.commentHTML = " "
        else:
            self.commentHTML = '<hr /><div class="comment">译者评论:<br />%s</div>'%cmt

    def save(self):
        prefix = './htmls/'
        if not os.path.exists(prefix):
            os.makedirs(prefix)

        fname = prefix + replace_invalid_filename_char(self.title) + ".html"

        html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>%s\
        </title></head><body>%s%s</body></html>'%(self.title, self.content, self.commentHTML)

        with open(fname, 'w+',encoding='utf8') as f:
            f.write(html)
        


if __name__ == "__main__":
    with open('./Seveneves_url.txt','r') as f:
        for url in f:
            #print(url)
            thisA = Article(url.replace('\n',''))
            print(thisA.title)