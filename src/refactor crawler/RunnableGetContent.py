# -*-coding:utf-8-*-
import logging
import urllib2
import datetime
import mysql.connector
from bs4 import BeautifulSoup
from HtmlUtil import HtmlCreator
from SqlUtil import MysqlOperator
from StringUtil import LinkOperator
from SoupUtil import SoupOperator
from Constant import BBSContent

config = {'host': '172.17.23.70',
          'user': 'why',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }
conn = mysql.connector.connect(**config)
logging.basicConfig(filename='log.log', level=logging.DEBUG)

cur = conn.cursor()
cur.execute('SELECT num FROM counter where id = 2')
index = cur.fetchall()[0][0]
#for x in range(1,1766627):
while index<1766626:
    x=index+1
    mo = MysqlOperator(conn)
    bbsContent = BBSContent()
    bbs = mo.selectLinkById(x)
    # (1, 3582, 49822317, u'/bbs/thread-c-3582-49822317-1.html', 21610587, datetime.datetime(2016, 2, 20, 13, 13), 6, 0,datetime.datetime(2016, 2, 20, 15, 44), 24772368)
    try:
        url = 'http://club.autohome.com.cn' + bbs[3]
        html = HtmlCreator(url).getUrlRespHtml()
    except urllib2.HTTPError, e:
        logging.info(' id=' + str(x) + u"连接html发生HTTPError,帖子可能被删除" + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S') + ' HTTPError = ' + str(e) + '---' + url)
        continue
    try:
        so = SoupOperator(html)
        # 标题
        title = so.getTitle()[1]
        # 帖子点击数量
        clickNum = so.getBBSClickNum()
        # 更新链接表的标题内容

        MysqlOperator.updateTitleAndClickNum(conn,x,clickNum,title)

        pageNum = so.findTotlePageNum()
        print pageNum+u'页： id='+unicode(x)+u' '+url
        # 楼主内容
        f0Content = so.getF0Content(x, bbs[2])

        mo.insertBBSContent(f0Content)

        # bbs中所有页的链接
        links = LinkOperator.makeLinkByPage(pageNum, url)
        soups = []
        for link in links:
            soups.append(BeautifulSoup(HtmlCreator(link).getUrlRespHtml(), "lxml"))
        for soup in soups:
            # 一页的所有楼层
            allFList = SoupOperator.getAllFContentList(soup)
            for content in SoupOperator.getContents(allFList, x, bbs[2]):
                #content.printContent()
                mo.insertBBSContent(content)

    except Exception, e:
        logging.error(' id=' + str(x) + u"抓取信息时发生错误" + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S') + ' Error = ' + str(e) + '---' + url)
        conn.rollback()
        index+=1
        continue
    else:
        index+=1
        cur.execute('update counter set num = %s where id = 2',[index])
        conn.commit()
