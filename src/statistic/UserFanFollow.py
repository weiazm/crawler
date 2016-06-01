# -*-coding:utf-8-*-
import bs4
import mysql.connector

import HtmlUtil
import StringUtil

headerDict = {
    'Accept': '*/*',
    'User-Agent': 'userAgentIE9',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    "Upgrade-Insecure-Requests": "1",
    'Cookie': 'cookieCityId=110100; sessionid=ECD798C6-6389-97EB-FB47-AD1374FD60D7%7C%7C2016-05-21+00%3A50%3A12.182%7C%7Cwww.baidu.com; sessionuid=ECD798C6-6389-97EB-FB47-AD1374FD60D7||2016-05-21+00%3A50%3A12.182||www.baidu.com; mylead_26959260=11; historybbsName4=c-3074%7C%E5%93%88%E5%BC%97H7%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg6%2FM08%2F08%2F7C%2Fuserphotos%2F2015%2F12%2F10%2F14%2FwKgH3FZpF8uAdbCoAAE88v4wZAY344_s.jpg; sessionip=219.217.246.8; ASP.NET_SessionId=sqis1rm4skumtpym40421uzc; sessionfid=3504148999; pcpopclub=FBF49F8225FC74EC341B081090CB580E0810AABA7410921DAD8900D52AAEB1B1040A7D0E63D7FEC611C28DBFCB676F033E081B984459F64E18206555F5D65DBAF94CCD2D6E543C581DA48C21A138A2B16AF38B1FD394A364A49B0892836E896D4BC94156D7584BF0F1A98762D73EC45CCF357E63F3F1D449C6A703A214F940DF607756A5B216EA3875018D9681EBC890BAF4B82AD328AA536C9C72369F8251CFB14DCABA35C8A0902724AFAD301574C0C754C4BA4AE2FE7E720DBC31BA6B8A133B5E861B120178ECE0DF57FB0332EFA7C442C1DDF5E9C114C6CF481716DA440BB42D482BCE7986E0FC426700750D95D913D390423C3926D43FFC97D392E8E98796ADBF32BFADC7B1468E7225D7C35E4E80E32AF3B8EC7B78C5CA3806F740823E67E8EDC4EBC562B2DDFC10998A833BBC0986D8BA09A1CBD1952A3CDA5DFA093F816BCC5A1085B63E4229C366; clubUserShow=26959260|2767|11|IWillFollow|0|0|0||2016-05-31 11:37:36|0; autouserid=26959260; sessionuserid=26959260; sessionlogin=143cbfb3ba5147f5a8d0fd52eec1553b019b5d9c; __utma=1.1061922101.1463763020.1464619623.1464664654.10; __utmb=1.0.10.1464664654; __utmc=1; __utmz=1.1464619623.9.6.utmcsr=i.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/4412576/club/sendreply; ref=www.baidu.com%7C%7C0%7C8-1%7C2016-05-31+11%3A37%3A48.240%7C2016-05-21+00%3A50%3A12.182; sessionvid=AE4A04CC-8231-4387-8579-65D14F481299; area=230199',
}

config = {'host': 'localhost',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }


def getStatistic(urlFollow, urlFan):
    htmlFollow = HtmlUtil.HtmlCreator(urlFollow, headerDict=headerDict, timeout=2).getUrlRespHtml()
    htmlFan = HtmlUtil.HtmlCreator(urlFan, headerDict=headerDict, timeout=2).getUrlRespHtml()
    soupFollow = bs4.BeautifulSoup(htmlFollow, "lxml").find(class_="m_t25").find(id="dynamic")
    soupFan = bs4.BeautifulSoup(htmlFan, "lxml").find(class_="m_t25").find(id="dynamic")
    soup = bs4.BeautifulSoup(htmlFollow, "lxml")
    # 计算数量
    num_of_follow = filter(lambda x: x.isdigit(), StringUtil.LinkOperator.formatString(
        soupFollow.find(class_="subdyn2").get_text()).split(u"关注")[-1].replace(u"人", ""))
    num_of_fans = filter(lambda x: x.isdigit(), StringUtil.LinkOperator.formatString(
        soupFan.find(class_="subdyn2").get_text()).split(u"关注")[0].replace(u"人", "").replace(u"已有", ""))
    if len(num_of_follow) == 0:
        num_of_follow = 0
    if len(num_of_fans) == 0:
        num_of_fans = 0
    print num_of_follow, num_of_fans
    # 页数
    pageNumFollow = 1
    print soup
    if soupFollow.find(class_="paging") != None:
        pageNumFollow = soupFollow.find(class_="paging").find(class_="current").get_text()
    pageNumFans = 1
    if soupFan.find(class_="paging") != None:
        pageNumFans = soupFan.find(class_="paging").find(class_="current").get_text()
    print pageNumFollow, pageNumFans


index = 1
conn = mysql.connector.connect(**config)
cur = conn.cursor()
cur.execute('SELECT uid FROM refactor_crawler.user where id = %s', [index, ])
uid = cur.fetchall()[0][0]
print uid
uid = 1804955
urlFollow = "http://i.autohome.com.cn/" + str(uid) + "/following?page=99"
urlFan = "http://i.autohome.com.cn/" + str(uid) + "/followers?page=100"
print urlFollow, urlFan
# uid = 26959260
result = getStatistic(urlFollow, urlFan)
print result
# cur.execute("UPDATE `refactor_crawler`.`user` SET `auth_cars` = %s WHERE `uid` = %s", [result, uid])
