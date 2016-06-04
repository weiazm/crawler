# -*-coding:utf-8-*-
import datetime
import logging
import threading
import traceback

import mysql.connector
from bs4 import BeautifulSoup

from HtmlUtil import HtmlCreator
from StringUtil import LinkOperator

config = {'host': '172.17.26.167',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }


class BBSContent(object):
    def __init__(self):
        self.bbs_id = ""
        self.uid = ""
        self.from_floor = ""
        self.to_floor = ""
        self.reply_time = ""
        self.content = ""
        self.num_of_links = ""
        self.num_of_words = ""
        self.num_of_pictures = ""
        self.num_of_faces = ""
        self.device = ""
        self.if_in_twenty = ""
        self.if_elite = 0
        self.if_recommend = 0

    def printContent(self):
        print self.bbs_id, self.uid, self.from_floor, self.to_floor, self.reply_time, self.content, self.num_of_links, self.num_of_words, self.num_of_pictures, self.num_of_faces, self.device, self.if_in_twenty, self.if_elite, self.if_recommend


def getBBSClickNum(soup):
    clickNum = soup.find(
        class_="fr fon12").find(id="x-views")
    return LinkOperator.formatString(clickNum.get_text())


def getBBSReplyNum(soup):
    clickNum = soup.find(
        class_="fr fon12").find(id="x-replys")
    return LinkOperator.formatString(clickNum.get_text())


def findGifNum(lis):
    n = 0
    for lin in lis:
        if unicode(lin['src']).find('http://x.autoimg.cn/club/smiles/') and unicode(lin['src']).find('gif'):
            n += 1
    return n


def getF0Content(soup, bbsId, carId):
    bb = BBSContent()
    #########################
    bb.elite = 0
    bb.if_recommend = 0
    soup2 = soup.find(id="topic_detail_main").find(class_="conmain").find(
        class_="clearfix contstxt outer-section")
    tag = soup2.find(id="seal")
    if tag != None:
        if str(tag) == '<span class="pngfix Jing" id="seal"> </span>':
            bb.if_elite = 1
        if str(tag) == '<span class="pngfix Jian" id="seal"> </span>':
            bb.if_recommend = 1
    #########################

    soup = soup.find(id="topic_detail_main").find(class_="conmain").find(
        id="maxwrap-maintopic").find(
        class_="clearfix contstxt outer-section")
    bb.bbs_id = bbsId
    bb.uid = soup['uid']
    bb.from_floor = '0'
    bb.to_floor = '0'
    bb.content = LinkOperator.formatString(
        soup.find(class_="conright fr").find(class_="rconten").find(class_="conttxt").find(
            class_="w740").get_text())
    bb.reply_time = soup["data-time"]
    # 特殊情况
    try:
        bb.device = LinkOperator.formatString(
            soup.find(class_="conright fr").find(class_="plr26 rtopcon").find_all(target="_blank")[-1].get_text())
    except Exception, e:
        bb.device = "noDevice"
    bb.num_of_links = bb.content.count('http://')
    bb.num_of_words = len(bb.content)
    # 计算图片表情数量
    lis = soup.find(class_="conright fr").find(class_="rconten").find(class_="conttxt").find(
        class_="w740").find_all('img')
    bb.num_of_faces = findGifNum(lis)
    bb.num_of_pictures = len(lis) - bb.num_of_faces
    tempList = ['3582', '3460', '3454', '2778', '2615', '3013', '3788', '3691', '2123', '3204', '3677',
                '656', '314', '874', '3413', '364', '982', '526', '442', '871', '519', '614']
    if str(carId) in tempList:
        bb.if_in_twenty = 1
    else:
        bb.if_in_twenty = 0
    return bb


def run(id):
    conn = mysql.connector.connect(**config)
    logging.basicConfig(filename='logOFContent.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count where id = %s', [id])
    startEnd = cur.fetchall()[0]
    cur.close()
    x = startEnd[0]
    index = x
    while index < startEnd[1]:
        try:
            cur = conn.cursor()
            cur.execute('select * from forum_links_user where id = %s', [index])
            bbs = cur.fetchall()[0]
            bbs_id = bbs[2]
            car_id = bbs[1]
            url = bbs[3]
            # url = 'http://club.autohome.com.cn/bbs/thread-c-333-53025433-1.html'
            print url
            html = HtmlCreator(url, timeout=3).getUrlRespHtml()
            soup = BeautifulSoup(html, "html5lib")
            html = None
            # 帖子点击数量
            clickNum = getBBSClickNum(soup)
            replyNum = getBBSReplyNum(soup)
            # 更新链接表的标题内容
            # print bbs_id, clickNum, replyNum
            cur.execute('update forum_links_user set click_num =%s,reply_num =%s where bbs_id =%s',
                        [clickNum, replyNum, bbs_id])
            # 楼主内容
            c = getF0Content(soup, bbs_id, car_id)
            soup = None
            # c.printContent()
            cur.execute(
                'insert into main_content_user(bbs_id, uid, from_floor, to_floor, reply_time, content, num_of_links, num_of_words, num_of_pictures, num_of_faces, device,if_in_twenty,if_elite,if_recommend) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                [c.bbs_id, c.uid, c.from_floor, c.to_floor, c.reply_time, c.content, c.num_of_links,
                 c.num_of_words, c.num_of_pictures, c.num_of_faces, c.device, c.if_in_twenty, c.if_elite,
                 c.if_recommend])
            c = None
        except Exception, e:
            if str(e) == "timed out" or str(
                    e) == "<urlopen error timed out>" or str(
                e) == "[Errno 10054] " or str(
                e) == "<urlopen error [Errno 11001] getaddrinfo failed>" or str(
                e) == "HTTP Error 500: Internal Server Error" or str(
                e) == "HTTP Error 503: Service Unavailable" or str(
                e) == "[Errno 10053] ":
                conn.rollback()
                continue
            else:
                logging.error(' id=' + str(index) + u"抓取user时发生错误" + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + ' Error = ' + str(e) + '---')
                traceback.print_exc()
                conn.rollback()
                index += 1
                continue
        else:
            index += 1
            cur.execute('update count set start = %s where id = %s', [index, id])
            conn.commit()
            cur.close()
            print "Done!"


threads = []
# 1, 563
for i in xrange(70, 80):
    th = threading.Thread(target=run, args=(i,))
    threads.append(th)

for t in threads:
    t.start()
# 等待子线程结束
for t in threads:
    t.join()
