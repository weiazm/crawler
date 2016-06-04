# -*-coding:utf-8-*-

from bs4 import BeautifulSoup

from HtmlUtil import HtmlCreator


def getBBSLinkFromLink(link):
    soup = BeautifulSoup(HtmlCreator(link).getUrlRespHtml(), 'html5lib')
    soupChild = soup.find(class_="content").find(class_="carea").find(id="subcontent").find_all(class_="list_dl")
    for s in soupChild:
        try:
            lang = s.get('lang')
            if (lang != None):
                langs = lang.split('|')
                # print lang
                _bbsId = unicode(langs[2])
                tag = s.dt.span
                print _bbsId, tag
        except Exception, e:
            pass


link = "http://club.autohome.com.cn/bbs/forum-c-3582-1.html?orderby=dateline&qaType=-1#pvareaid=101061"
print link
getBBSLinkFromLink(link)
# html = HtmlCreator(link).getUrlRespHtml()
# soup = BeautifulSoup(html,'html5lib')
# pageNum = soup.find(class_="pagearea").find(class_="fr").get_text()[1:][0:-1]
# result = LinkOperator.makeLinkByPageNum(link, pageNum)
# for res in result:
#     print res
#     __getBBSLinkFromLink(res)
