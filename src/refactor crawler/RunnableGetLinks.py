#-*-coding:utf-8-*-
import logging
import mysql.connector
from HtmlUtil import HtmlCreator
from SqlUtil import MysqlOperator
from StringUtil import LinkOperator
from SoupUtil import SoupOperator

url = "http://club.autohome.com.cn/bbs/forum-c-3582-1.html?orderby=dateline&qaType=-1#pvareaid=101061"
hc = HtmlCreator(url)
html = hc.getUrlRespHtml()
conn = mysql.connector.connect(user='root', password='1234', database='refactor_crawler', use_unicode=True)
carIdBrands = MysqlOperator(conn).selectCarIds()
for car in carIdBrands:
    print car[0],car[1],car[2],car[3]
    link = LinkOperator.makeLinkByCarId(car[1])
    print link
    html = HtmlCreator(link).getUrlRespHtml()
    pageNum = SoupOperator(html).getBBSPageNum()
    result = LinkOperator.makeLinkByPageNum(link,pageNum)
    for res in result:
        print res
    SoupOperator.getBBSLinksFromForumLink(result,conn)