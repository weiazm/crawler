# -*-coding:utf-8-*-

from bs4 import BeautifulSoup

import Constant
from SoupUtil import SoupOperator
from src.user.HtmlUtil import HtmlCreator

index = 195349
timeout = Constant.timeout
url = "http://i.autohome.com.cn/" + str(index)
print  url
# soup = BeautifulSoup(HtmlCreator(url, postDict={}, headerDict=Constant.headerDict, timeout=0, useGzip=True).getUrlRespHtml(),'lxml')
infoSoup = BeautifulSoup(
    HtmlCreator(url + "/info", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                useGzip=True).getUrlRespHtml(), 'lxml')
print  1
followingSoup = BeautifulSoup(
    HtmlCreator(url + "/following", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                useGzip=True).getUrlRespHtml(), "lxml")
print  2
followersSoup = BeautifulSoup(
    HtmlCreator(url + "/followers", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                useGzip=True).getUrlRespHtml(), "lxml")
print  3
topicSoup = BeautifulSoup(
    HtmlCreator("http://i.service.autohome.com.cn/clubapp/OtherTopic-" + str(index) + "-all-1.html",
                postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                useGzip=True).getUrlRespHtml(),
    "lxml")
print  4
oilSoup = BeautifulSoup(
    HtmlCreator(url + "/oil", postDict={}, headerDict=Constant.headerDict, timeout=timeout,
                useGzip=True).getUrlRespHtml(), "lxml")
print  5
koubeiSoup = BeautifulSoup(
    HtmlCreator("http://k.autohome.com.cn/myspace/koubei/his/" + str(index), postDict={},
                headerDict=Constant.headerDict, timeout=timeout,
                useGzip=True).getUrlRespHtml(), "lxml")
print  6
priceSoup = BeautifulSoup(
    HtmlCreator("http://jiage.autohome.com.cn/web/price/otherlist?memberid=" + str(index), postDict={},
                headerDict=Constant.headerDict, timeout=timeout, useGzip=True).getUrlRespHtml(), "lxml")
print  7
taskSoup = BeautifulSoup(
    HtmlCreator("http://i.autohome.com.cn/help/Task/" + str(index), postDict={},
                headerDict=Constant.headerDict,
                timeout=timeout, useGzip=True).getUrlRespHtml(), "lxml")
print  8

user = SoupOperator.getUser(infoSoup, followingSoup, followersSoup, topicSoup, oilSoup, koubeiSoup,
                            priceSoup,
                            taskSoup, index)
user.printUser()
