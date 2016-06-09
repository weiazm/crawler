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

headerDict = {
    'Accept': '*/*',
    'User-Agent': 'userAgentIE9',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Cookie': 'sessionfid=3504148999; cookieCityId=110100; sessionid=ECD798C6-6389-97EB-FB47-AD1374FD60D7%7C%7C2016-05-21+00%3A50%3A12.182%7C%7Cwww.baidu.com; sessionuid=ECD798C6-6389-97EB-FB47-AD1374FD60D7||2016-05-21+00%3A50%3A12.182||www.baidu.com; mylead_26959260=11; pcpopclub=83A19D8091978C893571F1FE05481E65DC13460343C4D32C548422D75D4CB2BC08DDF7225F8D1DA14C38BEB82EE546717985FDB57E48CD78A6B71F0E8648547FE941E94CE33BA0AF1060A8302C05E1626893926E9658DDA2E50F59AB30AB5E84D71F93FC7A30BF587B9CEC8291D277DC646DF2E7C7F88CBBA31A74FCA9A56D87698A10C50047878E1C85E9D308F5942CF4CC33F219C0B8DEDFF5AE893DECE378AC8DE3A7C6B78BBFBEF3FC612E35A1402C82E8CE0E06426E0740B45D39A1BF410F374BF0E342A605D7010F6804BEE1A1ABEFCF5D04FF130EDADB776C56EDF3B9D9199BBF2198057CAD0E2D7087EF656B6F8966F27D3CC55AF2A7AA9C2948644A21F61F7295BA4D5C57ADBA42442B0DDD1341F2462E93A835600E54FCCAAFFBC76C88022A804E02875688B12B7EE5CEA5763A35DE985189E4B5E80A71C76EAF29FC0A356F9FFAE4354DB74B94; clubUserShow=26959260|2767|11|IWillFollow|0|0|0||2016-05-30 22:48:04|0; historybbsName4=c-3074%7C%E5%93%88%E5%BC%97H7%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg6%2FM08%2F08%2F7C%2Fuserphotos%2F2015%2F12%2F10%2F14%2FwKgH3FZpF8uAdbCoAAE88v4wZAY344_s.jpg%2Cc-3068%7C%E6%A0%87%E8%87%B4301%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg23%2FM07%2F3F%2F68%2Fuserphotos%2F2016%2F04%2F19%2F21%2FwKjBwFcWNMOAVNDbAAEoNg4P1cg743_s.jpg%2Cc-3460%7C%E7%BC%A4%E6%99%BA%7C%2Cc-3582%7C%E6%9C%AC%E7%94%B0XR-V%7C; ASP.NET_SessionId=zmkwdzupd55nl02qhc3mivnn; sessionip=219.217.246.8; __utma=1.1061922101.1463763020.1465043847.1465088620.24; __utmb=1.0.10.1465088620; __utmc=1; __utmz=1.1465088620.24.9.utmcsr=i.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/4412576/club/sendreply; ref=x.autoimg.cn%7C0%7C0%7Cwww.baidu.com%7C2016-06-05+09%3A04%3A03.998%7C2016-06-03+17%3A42%3A50.932; sessionvid=64E1B50B-6914-4CF7-BBAD-1CC5BD64D548; area=230199'
}


# def getMedalString(soups):
#     result=""
#     for soup in soups:
#         result = result +'^'+ soup.get_text()
#     return result

def run(id):
    conn = mysql.connector.connect(**config)
    logging.basicConfig(filename='phoneAuth.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count2 where id = %s', [id])
    startEnd = cur.fetchall()[0]
    cur.close()
    x = startEnd[0]
    index = x
    while index < startEnd[1]:
        try:
            cur = conn.cursor()
            cur.execute('select * from user where id = %s', [index])
            user = cur.fetchall()[0]
            uid = user[1]
            url = "http://i.autohome.com.cn/" + str(uid) + "/info"
            print url
            html = HtmlCreator(url, timeout=2, headerDict=headerDict).getUrlRespHtml()
            # htmlInfo = HtmlCreator(url2, timeout=2,headerDict=headerDict).getUrlRespHtml()
            # soups = BeautifulSoup(html, "html5lib").find(class_="mainContainer").find(class_="rightside").find(class_="user-state").find(class_="user-honor user-honor-cur").\
            #     find(class_="user-honor-inner")
            # medal = getMedalString(soups)
            soup = BeautifulSoup(html, "html5lib").find(class_="mainContainer").find(id="rightContainer").find(
                class_="uData").find_all('p')[2].get_text()
            phone_auth = LinkOperator.formatString(soup).split(':')[-1]
            cur.execute('update user set phone_auth =%s where uid =%s', [phone_auth, uid])
        except Exception, e:
            if str(e) == "timed out" or str(
                    e) == "<urlopen error timed out>" or str(
                e) == "HTTP Error 404: Not Found" or str(
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
            cur.execute('update count2 set start = %s where id = %s', [index, id])
            conn.commit()
            cur.close()
            print "Done!"


threads = []
# 1, 563
for i in xrange(1, 52):
    th = threading.Thread(target=run, args=(i,))
    threads.append(th)

for t in threads:
    t.start()
# 等待子线程结束
for t in threads:
    t.join()
