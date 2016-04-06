#-*-coding:utf-8-*-
'''
Created on 2016年4月5日

@author: why
'''
import urllib2
from bs4 import BeautifulSoup

def gethtml(url):
    req = urllib2.Request(url,headers={'User-Agent':'Magic Browser'})
    usock=urllib2.urlopen(req)
    encoding = usock.headers.getparam('charset')
    print encoding
    html = usock.read()
    usock.close()
    return html

html=gethtml("http://club.autohome.com.cn/bbs/forum-c-3204-1.html")
print html
soup = BeautifulSoup(html,"lxml")
#print soup.get_text()
