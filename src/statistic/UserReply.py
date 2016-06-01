# -*-coding:utf-8-*-
import datetime
import logging
import threading
import traceback

import bs4
import mysql.connector

import HtmlUtil
import StringUtil


class ReplyContent(object):
    def __init__(self):
        self.bbs_id = ""
        self.uid = ""
        self.to_floor = ""
        self.reply_time = ""
        self.content = ""
        self.if_in_twenty = ""
        self.link = ""

    def printContent(self):
        print self.bbs_id, self.uid, self.to_floor, self.reply_time, self.content, self.if_in_twenty, self.link


config = {'host': 'localhost',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }


def insertReplyContent(conn, result):
    for res in result:
        c = res
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO refactor_crawler.bbs_content_user(bbs_id,uid,to_floor,reply_time,content,if_in_twenty,link)VALUES(%s,%s,%s,%s,%s,%s,%s)",
            [c.bbs_id, c.uid, c.to_floor, c.reply_time, unicode(c.content), c.if_in_twenty, c.link])
        cursor.close()


def getReplyContent(soup, uid):
    result = []
    if soup.find(class_="topicList") == None:
        return result
    soups = soup.find(class_="topicList").find_all("tr")
    temp = 0
    for soup in soups:
        if soup.find(class_="pr fullWidth") != None:
            res = ReplyContent()
            try:
                res.uid = uid
                res.to_floor = StringUtil.LinkOperator.formatString(
                    soup.find_all(class_="rcon m_t5")[0].find(class_="rUser_rc").find_all(target="_blank")[
                        -1].get_text()).replace(u"楼", "").replace("[", "").replace("]", "").replace(u"主", "0").replace(
                    u"板凳", "2").replace(u"沙发", "1").replace(u"地板", "3")
                res.to_floor = filter(lambda x: x.isdigit(), res.to_floor)
                if res.to_floor == '':
                    res.to_floor = '0'
                # 回复时间
                try:
                    res.reply_time = filter(lambda x: x.isdigit(),
                                            str(soup.find_all(class_="txtCen")[-1].get_text())) + "00"
                except Exception, e:
                    if str(e) == "list index out of range":
                        res.reply_time = temp
                # 减少错误
                if len(res.reply_time) > 11:
                    temp = res.reply_time
                else:
                    res.reply_time = temp

                res.content = StringUtil.LinkOperator.formatString(
                    soup.find_all(class_="rcon m_t5")[-1].find(class_="rUser_rc").get_text())
                res.link = soup.find(class_="rUser_rc").a["href"]
                res.bbs_id = res.link.split("-")[-2]
                res.if_in_twenty = res.link.split("-")[-3]
                tempList = ['3582', '3460', '3454', '2778', '2615', '3013', '3788', '3691', '2123', '3204', '3677',
                            '656', '314', '874', '3413', '364', '982', '526', '442', '871', '519', '614']
                if res.if_in_twenty in tempList:
                    res.if_in_twenty = 1
                else:
                    res.if_in_twenty = 0
            except Exception, e:
                print e
                # traceback.print_exc()
                continue
            # res.printContent()
            result.append(res)
    return result


def getStatistic(url, uid):
    html = HtmlUtil.HtmlCreator(url, timeout=3).getUrlRespHtml()
    soup = bs4.BeautifulSoup(html, "lxml")
    pageNum = 1
    if soup.find(class_="paging") != None:
        pageNum = soup.find(class_="paging").find_all(target="_self")[-2].get_text()
    print pageNum
    result = []
    result.extend(getReplyContent(soup, uid))
    x = 1
    while x < int(pageNum):
        x += 1
        url = "http://i.service.autohome.com.cn/clubapp/OtherReply-" + str(uid) + "-" + str(x) + ".html"
        html = HtmlUtil.HtmlCreator(url, timeout=3).getUrlRespHtml()
        soup = bs4.BeautifulSoup(html, "lxml")
        result.extend(getReplyContent(soup, uid))
        print x
    return result


def run(id):
    conn = mysql.connector.connect(**config)
    logging.basicConfig(filename='logUserReply.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count3 where id = %s', [id])
    startEnd = cur.fetchall()[0]
    x = startEnd[0]
    index = x
    while index < startEnd[1]:
        try:
            cur = conn.cursor()
            cur.execute('SELECT uid FROM refactor_crawler.user where id = %s', [index, ])
            uid = cur.fetchall()[0][0]
            print uid,
            url = "http://i.service.autohome.com.cn/clubapp/OtherReply-" + str(uid) + "-1.html"
            print url
            result = getStatistic(url, uid)
            insertReplyContent(conn, result)
        except Exception, e:
            if str(e) == "timed out" or str(e) == "<urlopen error timed out>" or str(
                    e) == "HTTP Error 404: Not Found" or str(e) == "[Errno 10054] " or str(
                e) == "<urlopen error [Errno 11001] getaddrinfo failed>" or str(
                e) == "HTTP Error 500: Internal Server Error" or str(e) == "HTTP Error 503: Service Unavailable":
                conn.rollback()
                continue
            else:
                logging.error(' id=' + str(index) + u"抓取user时发生错误" + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + ' Error = ' + unicode(e) + '---')
                traceback.print_exc()
                conn.rollback()
                index += 1

                continue
        else:
            index += 1
            cur.execute('update count3 set start = %s where id = %s', [index, id])
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
