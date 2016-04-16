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
for x in range(153, 200):
    bbsContent = BBSContent()
    bbs = MysqlOperator(conn).selectLinkById(x)
    #(1, 3582, 49822317, u'/bbs/thread-c-3582-49822317-1.html', 21610587, datetime.datetime(2016, 2, 20, 13, 13), 6, 0,datetime.datetime(2016, 2, 20, 15, 44), 24772368)
    try:
        url = 'http://club.autohome.com.cn'+bbs[3]
        html = HtmlCreator(url).getUrlRespHtml()
        print url
    except urllib2.HTTPError,e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' id=' + str(x) + ' HTTPError = ' + str(
            e.code) + u"帖子可能被删除:" + url)
        continue
    so = SoupOperator(html)
    #标题
    title=so.getTitle()[1]
    pageNum = so.findTotlePageNum()
    #帖子点击数量
    clickNum = so.getBBSClickNum()
    #楼主内容
    f0Content = so.getF0Content(x,bbs[2])

    #更新链接表的标题内容
    #MysqlOperator.updateTitleAndClickNum(conn,x,clickNum,title)




