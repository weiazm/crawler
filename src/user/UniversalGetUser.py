# -*-coding:utf-8-*-
import datetime
import logging
import threading

import mysql.connector
from bs4 import BeautifulSoup

import Constant
import statisticForUser
from SoupUtil import SoupOperator
from SqlUtil import MysqlOperator
from src.user.HtmlUtil import HtmlCreator


def run(id):
    conn = mysql.connector.connect(**Constant.config)
    logging.basicConfig(filename='log.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count where id = %s', [id])
    startEnd = cur.fetchall()[0]
    x = startEnd[0]
    while x < startEnd[1]:
        try:
            cur = conn.cursor()
            cur.execute('SELECT uid from uid where id = %s', [x])
            index = cur.fetchall()[0][0]
            # index = 1492838

            cur.execute('SELECT * FROM refactor_crawler.bbs_content where uid = %s order by reply_time', [index, ])
            contents = cur.fetchall()
            result = statisticForUser.getStatistic(contents)

            cur.execute(
                'SELECT * FROM refactor_crawler.bbs_content where uid = %s and from_floor = 0 order by reply_time ',
                [index, ])
            timeContents = cur.fetchall()

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
                            postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                            useGzip=True).getUrlRespHtml(),
                "lxml")
            oilSoup = BeautifulSoup(
                HtmlCreator(url + "/oil", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                            useGzip=True).getUrlRespHtml(), "lxml")
            koubeiSoup = BeautifulSoup(
                HtmlCreator("http://k.autohome.com.cn/myspace/koubei/his/" + str(index), postDict={},
                            headerDict=Constant.headerDict, timeout=timeout,
                            useGzip=True).getUrlRespHtml(), "lxml")
            priceSoup = BeautifulSoup(
                HtmlCreator("http://jiage.autohome.com.cn/web/price/otherlist?memberid=" + str(index), postDict={},
                            headerDict=Constant.headerDict, timeout=timeout, useGzip=True).getUrlRespHtml(), "lxml")
            taskSoup = BeautifulSoup(
                HtmlCreator("http://i.autohome.com.cn/help/Task/" + str(index), postDict={},
                            headerDict=Constant.headerDict,
                            timeout=timeout, useGzip=True).getUrlRespHtml(), "lxml")

            user = SoupOperator.getUser(infoSoup, followingSoup, followersSoup, topicSoup, oilSoup, koubeiSoup,
                                        priceSoup,
                                        taskSoup, index)
            user.num_of_reply = result[0]
            user.num_of_reply_self = result[1]
            user.num_of_reply_others = result[2]

            if len(contents) > 0:
                user.first_post_time = contents[0][6]
                user.last_post_time = contents[-1][6]

            # user.printUser()
            MysqlOperator(conn).insertUser(user)
        except Exception, e:
            if str(e) == "timed out" or str(e) == "<urlopen error timed out>" or str(
                    e) == "HTTP Error 404: Not Found" or str(e) == "[Errno 10054] " or str(
                e) == "<urlopen error [Errno 11001] getaddrinfo failed>" or str(
                e) == "HTTP Error 500: Internal Server Error":
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


threads = []
for i in xrange(1, 59):
    th = threading.Thread(target=run, args=(i,))
    threads.append(th)

for t in threads:
    t.start()
# 等待子线程结束
for t in threads:
    t.join()
