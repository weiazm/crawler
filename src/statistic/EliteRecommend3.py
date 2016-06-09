# -*-coding:utf-8-*-
import datetime
import logging
import threading
import traceback

import mysql.connector
from bs4 import BeautifulSoup

from HtmlUtil import HtmlCreator

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
    'Cookie': 'cookieCityId=110100; sessionid=ECD798C6-6389-97EB-FB47-AD1374FD60D7%7C%7C2016-05-21+00%3A50%3A12.182%7C%7Cwww.baidu.com; sessionuid=ECD798C6-6389-97EB-FB47-AD1374FD60D7||2016-05-21+00%3A50%3A12.182||www.baidu.com; mylead_26959260=11; sessionip=219.217.246.8; AccurateDirectseque=404; historybbsName4=c-3074%7C%E5%93%88%E5%BC%97H7%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg6%2FM08%2F08%2F7C%2Fuserphotos%2F2015%2F12%2F10%2F14%2FwKgH3FZpF8uAdbCoAAE88v4wZAY344_s.jpg%2Cc-3068%7C%E6%A0%87%E8%87%B4301%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg23%2FM07%2F3F%2F68%2Fuserphotos%2F2016%2F04%2F19%2F21%2FwKjBwFcWNMOAVNDbAAEoNg4P1cg743_s.jpg; ASP.NET_SessionId=uowzwiauwa5krcl011gtbk4e; pcpopclub=93AC62A50B148ABC2E3CB2272809FB7D566EB679F5C33217F79C87291554996070F578C526CA72E177417F45080ABBB1B9ACBB41F11230F142A4A86F4C0904A0CB8B8B7373432371BA4D85468E03E6C0A3CFF6F8BD25E164793C3F6578A5E78D9DDA098993413C3580AFFDB396DC68FB726D5F72D433954F368775664EB53C9F078D6E758AD0B84F91B8627847FA93F56BCB5567EBB71C3FEDBCCB1EBF198BA0C41982972D0766D56D7C90C59F0B046E462AE30F21BBBF5DB2FD8979D574FDDF23B0859372199E6A1E4E5B1E436B6AA46BE47653F4DECE8F14E601EC122C5E40DC7B581EB4B0CC94ACED4F991AFAD012BA258BB2E9F73D4C7E55D56BB56CED6261B7553A1B6A1098E0EECFBF005D44ED644C1438621BC576F914EF0409A3CE6905FCB9934511F26D4E6AA41A018BDCA53D17C0FEAD0C3C634E12199824DA4EE4AF994E88FBAE4EAC98AA7176; clubUserShow=26959260|2767|11|IWillFollow|0|0|0||2016-06-03 20:44:34|0; autouserid=26959260; __utma=1.1061922101.1463763020.1464950908.1464956231.18; __utmb=1.0.10.1464956231; __utmc=1; __utmz=1.1464767397.13.7.utmcsr=club.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/bbs/thread-c-81-50403083-1.html; sessionuserid=26959260; sessionlogin=dc508f5180ba47eaab114bb67decac2c019b5d9c; ref=x.autoimg.cn%7C0%7C0%7Cwww.baidu.com%7C2016-06-03+20%3A44%3A38.354%7C2016-06-03+17%3A42%3A50.932; sessionvid=DDDC9B1D-A84C-4C70-852E-882DD55F6E03; area=230199'
}


# def getMedalString(soups):
#     result=""
#     for soup in soups:
#         result = result +'^'+ soup.get_text()
#     return result

def run(id):
    conn = mysql.connector.connect(**config)
    logging.basicConfig(filename='EliteRecommend.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count3 where id = %s', [id])
    startEnd = cur.fetchall()[0]
    cur.close()
    x = startEnd[0]
    index = x
    while index < startEnd[1]:
        try:
            cur = conn.cursor()
            cur.execute('select * from main_content where id = %s', [index])
            main_content = cur.fetchall()[0]
            bbs_id = main_content[3]
            cur.execute('select * from forum_links where bbs_id = %s', [bbs_id])
            forum_link = cur.fetchall()[0]
            link = forum_link[3]
            url = "http://club.autohome.com.cn" + str(link)
            # url = 'http://club.autohome.com.cn/bbs/thread-c-333-53025433-1.html'
            # url = 'http://club.autohome.com.cn/bbs/thread-c-3013-50644886-1.html'
            print url
            html = HtmlCreator(url, timeout=2, headerDict=headerDict).getUrlRespHtml()
            soup = BeautifulSoup(html, "html5lib").find(id="topic_detail_main").find(class_="conmain").find(
                class_="clearfix contstxt outer-section")
            tag = soup.find(id="seal")
            print tag
            if_elite = 0
            if_recommend = 0
            if tag != None:
                if str(tag) == '<span class="pngfix Jing" id="seal"> </span>':
                    if_elite = 1
                if str(tag) == '<span class="pngfix Jian" id="seal"> </span>':
                    if_recommend = 1
                cur.execute('update main_content set if_elite =%s,if_recommend = %s where bbs_id =%s',
                            [if_elite, if_recommend, bbs_id])
            print if_elite, if_recommend
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
            cur.execute('update count3 set start = %s where id = %s', [index, id])
            conn.commit()
            cur.close()
            print "Done!"


threads = []
# 1, 177
for i in xrange(140, 150):
    th = threading.Thread(target=run, args=(i,))
    threads.append(th)

for t in threads:
    t.start()
# 等待子线程结束
for t in threads:
    t.join()
