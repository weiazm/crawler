# -*-coding:utf-8-*-
import datetime
import logging

import mysql.connector
from bs4 import BeautifulSoup

import Constant
from HtmlUtil import HtmlCreator
from SoupUtil import SoupOperator
from SqlUtil import MysqlOperator

conn = mysql.connector.connect(**Constant.config)
logging.basicConfig(filename='log.log', level=logging.DEBUG)
cur = conn.cursor()
id = 14
cur.execute('SELECT start,end from count where id = %s', [id])
startEnd = cur.fetchall()[0]
print startEnd
x = startEnd[0]
while x < startEnd[1]:
    try:
        cur = conn.cursor()
        cur.execute('SELECT uid from uid where id = %s', [x])
        index = cur.fetchall()[0][0]
        # index = 1492838
        timeout = Constant.timeout
        url = "http://i.autohome.com.cn/" + str(index)
        print x, url
        # soup = BeautifulSoup(HtmlCreator(url, postDict={}, headerDict=Constant.headerDict, timeout=0, useGzip=True).getUrlRespHtml(),'lxml')
        infoSoup = BeautifulSoup(
            HtmlCreator(url + "/info", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                        useGzip=True).getUrlRespHtml(), 'lxml')
        followingSoup = BeautifulSoup(
            HtmlCreator(url + "/following", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                        useGzip=True).getUrlRespHtml(), "lxml")
        followersSoup = BeautifulSoup(
            HtmlCreator(url + "/followers", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                        useGzip=True).getUrlRespHtml(), "lxml")
        topicSoup = BeautifulSoup(
            HtmlCreator("http://i.service.autohome.com.cn/clubapp/OtherTopic-" + str(index) + "-all-1.html",
                        postDict={}, headerDict=Constant.headerDict, timeout=timeout, useGzip=True).getUrlRespHtml(),
            "lxml")
        oilSoup = BeautifulSoup(HtmlCreator(url + "/oil", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                                            useGzip=True).getUrlRespHtml(), "lxml")
        koubeiSoup = BeautifulSoup(HtmlCreator("http://k.autohome.com.cn/myspace/koubei/his/" + str(index), postDict={},
                                               headerDict=Constant.headerDict, timeout=timeout,
                                               useGzip=True).getUrlRespHtml(), "lxml")
        priceSoup = BeautifulSoup(
            HtmlCreator("http://jiage.autohome.com.cn/web/price/otherlist?memberid=" + str(index), postDict={},
                        headerDict=Constant.headerDict, timeout=timeout, useGzip=True).getUrlRespHtml(), "lxml")
        taskSoup = BeautifulSoup(
            HtmlCreator("http://i.autohome.com.cn/help/Task/" + str(index), postDict={}, headerDict=Constant.headerDict,
                        timeout=timeout, useGzip=True).getUrlRespHtml(), "lxml")

        user = SoupOperator.getUser(infoSoup, followingSoup, followersSoup, topicSoup, oilSoup, koubeiSoup, priceSoup,
                                    taskSoup, index)
        # user.printUser()
        MysqlOperator(conn).insertUser(user)
    except Exception, e:
        if str(e) == "timed out" or str(e) == "<urlopen error timed out>":
            conn.rollback()
            continue
        else:
            logging.error(' id=' + str(x) + u"抓取user时发生错误" + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + ' Error = ' + str(e) + '---' + url)
            conn.rollback()
            x += 1

            continue
    else:
        x += 1
        cur.execute('update count set start = %s where id = %s', [x, id])
        conn.commit()
        print "Done!"
