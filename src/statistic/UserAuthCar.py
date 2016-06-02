# -*-coding:utf-8-*-
import datetime
import logging
import threading

import bs4
import mysql.connector

import HtmlUtil
import StringUtil

config = {'host': 'localhost',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }


def getPageNum(soup):
    pages = soup.find(class_="page paging")
    num = 1
    page = None
    if pages != None:
        page = pages.find_all('a')
    if page != None:
        num = page[-1].get_text()
        print num
    return int(num)


def getStatistic(uid):
    url = "http://i.autohome.com.cn/" + str(uid) + "/car?page=50"
    print url
    html = HtmlUtil.HtmlCreator(url, timeout=2).getUrlRespHtml()
    soup = bs4.BeautifulSoup(html, "lxml")
    cars = soup.find_all(class_="fcpc")
    pageNum = getPageNum(soup)
    print pageNum
    result = ""
    for car in cars:
        # print StringUtil.LinkOperator.formatString(car.get_text())
        if car.find(style="display:none;") == None:
            result = result + '^' + StringUtil.LinkOperator.formatString(car.get_text()) + u'（认证）'
        else:
            result = result + '^' + StringUtil.LinkOperator.formatString(car.get_text())
    if pageNum > 1:
        while pageNum > 1:
            pageNum = pageNum - 1
            url = url = "http://i.autohome.com.cn/" + str(uid) + "/car?page=" + str(pageNum)
            html = HtmlUtil.HtmlCreator(url).getUrlRespHtml()
            soup = bs4.BeautifulSoup(html, "lxml")
            cars = soup.find_all(class_="fcpc")
            for car in cars:
                # print StringUtil.LinkOperator.formatString(car.get_text())
                if car.find(style="display:none;") == None:
                    result = result + '^' + StringUtil.LinkOperator.formatString(car.get_text()) + u'（认证）'
                else:
                    result = result + '^' + StringUtil.LinkOperator.formatString(car.get_text())
    return result


def run(id):
    conn = mysql.connector.connect(**config)
    logging.basicConfig(filename='log.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count where id = %s', [id])
    startEnd = cur.fetchall()[0]
    x = startEnd[0]
    index = x
    while index < startEnd[1]:
        try:
            cur = conn.cursor()
            cur.execute('SELECT uid FROM refactor_crawler.user where id = %s', [index, ])
            uid = cur.fetchall()[0][0]
            print uid
            # uid = 26959260
            result = getStatistic(uid)
            # print result
            cur.execute("UPDATE `refactor_crawler`.`user` SET `auth_cars` = %s WHERE `uid` = %s", [result, uid])
        except Exception, e:
            if str(e) == "timed out" or str(e) == "<urlopen error timed out>" or str(
                    e) == "HTTP Error 404: Not Found" or str(e) == "[Errno 10054] " or str(
                e) == "<urlopen error [Errno 11001] getaddrinfo failed>" or str(
                e) == "HTTP Error 500: Internal Server Error":
                conn.rollback()
                continue
            else:
                logging.error(' id=' + str(index) + u"抓取user时发生错误" + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + ' Error = ' + str(e) + '---')
                conn.rollback()
                index += 1

                continue
        else:
            index += 1
            cur.execute('update count set start = %s where id = %s', [index, id])
            conn.commit()
            print "Done!"


threads = []
for i in xrange(1, 52):
    th = threading.Thread(target=run, args=(i,))
    threads.append(th)

for t in threads:
    t.start()
# 等待子线程结束
for t in threads:
    t.join()
