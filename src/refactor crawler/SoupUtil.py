#-*-coding:utf-8-*-
import logging
import string
import datetime
from bs4 import BeautifulSoup
from HtmlUtil import HtmlCreator
from SqlUtil import MysqlOperator

logging.basicConfig(filename='SoupUtil.log',level=logging.DEBUG)

class SoupOperator(object):

    def __init__(self,html):
        self.__soup = BeautifulSoup(html,'lxml')

    def getBBSPageNum(self):
        str = self.__soup.find(class_="pagearea").find(class_="fr").get_text()[1:][0:-1]
        return string.atoi(str)

    @classmethod
    def __getBBSLinkFromLink(self,link,conn):
        soup = BeautifulSoup(HtmlCreator(link).getUrlRespHtml(), 'lxml')
        soupChild = soup.find(class_="content").find(class_="carea").find(id="subcontent").find_all(class_="list_dl")
        result = []
        for s in soupChild:
            try:
                lang = s.get('lang')
                if(lang!=None):
                    langs = lang.split('|')
                    #print lang
                    _carId = unicode(langs[1])
                    _bbsId = unicode(langs[2])
                    _link = unicode(s.find_all('a',target="_blank")[0].get('href'))
                    _authorUid =unicode(langs[5])
                    _releaseTime =unicode(langs[4])
                    _replyNum =unicode(langs[3])
                    _clickNum =unicode('')
                    _lastReplyTime =unicode(s.find(class_="ttime").get_text())
                    _LastReplyUid =unicode(langs[6])
                    res = [_carId,_bbsId,_link,_authorUid,_releaseTime,_replyNum,_clickNum,_lastReplyTime,_LastReplyUid]
                    result.append(res)
            except Exception,e:
                logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' link=' + unicode(link) + ' Error = ' + unicode(e) + u"未知错误发生:" + unicode(s))
        MysqlOperator(conn).insertForumLinks(set(result))


    @classmethod
    def getBBSLinksFromForumLink(self,linkList,conn):
        for link in linkList:
            self.__getBBSLinkFromLink(link,conn)

