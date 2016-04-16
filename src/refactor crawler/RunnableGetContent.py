#-*-coding:utf-8-*-
import logging
import urllib2
import datetime
import mysql.connector
from HtmlUtil import HtmlCreator
from SqlUtil import MysqlOperator
from StringUtil import LinkOperator
from SoupUtil import SoupOperator
from Constant import BBSContent

conn = mysql.connector.connect(user='root', password='1234', database='refactor_crawler', use_unicode=True)
logging.basicConfig(filename='RunnableGetContent.log',level=logging.DEBUG)

#for x in range(1,1766627):
for x in range(1, 2):
    bbs = MysqlOperator(conn).selectLinkById(x)
    #(1, 3582, 49822317, u'/bbs/thread-c-3582-49822317-1.html', 21610587, datetime.datetime(2016, 2, 20, 13, 13), 6, 0,datetime.datetime(2016, 2, 20, 15, 44), 24772368)
    try:
        url = 'http://club.autohome.com.cn'+bbs[3]
        html = HtmlCreator(url).getUrlRespHtml()
    except urllib2.HTTPError,e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' id=' + str(x) + ' HTTPError = ' + str(
            e.code) + u"帖子可能被删除:" + url)
        continue
    so = SoupOperator(html)

conn.cursor().execute("insert into test(test) values(%s)",["'"])
conn.commit()




