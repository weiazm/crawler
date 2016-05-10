# -*-coding:utf-8-*-
import datetime
import logging
import mysql.connector
import urllib2
from bs4 import BeautifulSoup

import Constant
from Constant import BBSContent
from HtmlUtil import HtmlCreator
from SoupUtil import SoupOperator
from SqlUtil import MysqlOperator
from StringUtil import LinkOperator

conn = mysql.connector.connect(**Constant.config)
logging.basicConfig(filename='log.log', level=logging.DEBUG)

cur = conn.cursor()
cur.execute('SELECT uid from uid where id = 1')
index = cur.fetchall()[0][0]
print index

url = "http://i.autohome.com.cn/4412576/info"
html = HtmlCreator(url, postDict={}, headerDict=Constant.headerDict, timeout=0, useGzip=True).getUrlRespHtml()
soup = BeautifulSoup(html,'lxml')
print LinkOperator.formatString(soup.find(class_="uData").get_text())