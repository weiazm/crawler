# -*-coding:utf-8-*-
import datetime
import logging
import threading

import bs4
import mysql.connector

import HtmlUtil
import StringUtil


class MainBBSContent(object):
    def __init__(self):
        self.car_id = ""
        self.bbs_id = ""
        self.link = ""
        self.author_uid = ""
        self.release_time = ""
        self.reply_num = ""
        self.click_num = ""
        self.title = ""

    def printContent(self):
        print self.car_id, self.bbs_id, self.link, self.author_uid, self.release_time, self.reply_num, self.click_num, self.title


config = {'host': 'localhost',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }


def getMainBBSContent(soup, uid):
    result = []
    if soup.find(class_="topicList") == None:
        return result
    soups = soup.find(class_="topicList").find_all("tr")
    for soup in soups:
        if soup.find(class_="m_t10") != None:
            res = MainBBSContent()
            try:
                res.car_id = str(soup.find(class_="m_t10").a["href"]).split("-")[-2]
                res.bbs_id = str(soup.find(class_="cp1").a["href"]).split("-")[-2]
                res.link = str(soup.find(class_="cp1").a["href"])
                res.author_uid = uid
                res.release_time = filter(lambda x: x.isdigit(),
                                          str(soup.find_all(class_="txtCen")[-1].get_text())) + "00"
                res.reply_num = ""
                res.click_num = ""
                res.title = StringUtil.LinkOperator.formatString(soup.find(class_="cp1").get_text())
            except Exception, e:
                logging.warn(' uid=' + str(uid) + u"解析soup发生错误" + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + ' Error = ' + str(e) + '---')
                continue
            # res.printContent()
            result.append(res)
    return result


def insertBBSContent(conn, result):
    # c = MainBBSContent
    for res in result:
        c = res
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO refactor_crawler.forum_links_user(car_id,bbs_id,link,author_uid,release_time,title)VALUES(%s,%s,%s,%s,%s,%s)",
            [c.car_id, c.bbs_id, c.link, c.author_uid, c.release_time, c.title])
        cursor.close()


def getStatistic(url, uid):
    html = HtmlUtil.HtmlCreator(url, timeout=3).getUrlRespHtml()
    soup = bs4.BeautifulSoup(html, "lxml")
    pageNum = 1
    if soup.find(class_="paging") != None:
        pageNum = soup.find(class_="paging").find_all(target="_self")[-2].get_text()
    print pageNum
    result = []
    result.extend(getMainBBSContent(soup, uid))
    x = 1
    while x < int(pageNum):
        x += 1
        url = "http://i.service.autohome.com.cn/clubapp/OtherTopic-" + str(uid) + "-all-" + str(x) + ".html"
        html = HtmlUtil.HtmlCreator(url, timeout=3).getUrlRespHtml()
        soup = bs4.BeautifulSoup(html, "lxml")
        result.extend(getMainBBSContent(soup, uid))
        print x
    return result


def run(id):
    conn = mysql.connector.connect(**config)
    logging.basicConfig(filename='logUserMain.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count2 where id = %s', [id])
    startEnd = cur.fetchall()[0]
    x = startEnd[0]
    index = x
    while index < startEnd[1]:
        try:
            cur = conn.cursor()
            cur.execute('SELECT uid FROM refactor_crawler.user where id = %s', [index, ])
            uid = cur.fetchall()[0][0]
            print uid
            url = "http://i.service.autohome.com.cn/clubapp/OtherTopic-" + str(uid) + "-all-1.html"
            print url
            result = getStatistic(url, uid)
            print result
            insertBBSContent(conn, result)
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
            cur.execute('update count2 set start = %s where id = %s', [index, id])
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
