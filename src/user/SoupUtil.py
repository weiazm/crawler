# -*-coding:utf-8-*-
import string

from bs4 import BeautifulSoup

from Constant import BBSContent, User
from HtmlUtil import HtmlCreator
from SqlUtil import MysqlOperator
from StringUtil import LinkOperator


class SoupOperator(object):
    def __init__(self, html):
        self.__soup = BeautifulSoup(html, 'lxml')

    def getTitle(self):
        normal = self.__soup.find(class_="maxtitle")
        qa = self.__soup.find(class_="qa-maxtitle")
        if normal != None:
            return True, LinkOperator.formatString(normal.get_text())
        elif qa != None:
            return True, LinkOperator.formatString(qa.get_text())
        else:
            return False, "noTitleFound"

    def __formatString(self, str):
        str = str.replace(' ', '')
        char = '/'
        char2 = u'页'
        posf = str.index(char)
        post = str.index(char2)
        # print posf,post
        return str[posf + 1:post]

    # 得到帖子的页数
    def findTotlePageNum(self):
        text = self.__soup.find(id="x-pages2").get_text()
        return self.__formatString(text)

    # 找论坛总页面的页数
    def getBBSPageNum(self):
        str = self.__soup.find(class_="pagearea").find(class_="fr").get_text()[1:][0:-1]
        return string.atoi(str)

    # 得到帖子点击数
    def getBBSClickNum(self):
        clickNum = self.__soup.find(id="topic_detail_main").find(class_="conmain").find(id="maxwrap-maintopic").find(
            class_="fr fon12").find(id="x-views")
        return LinkOperator.formatString(clickNum.get_text())

    # 得到楼主内容
    def getF0Content(self, x, bbsId):
        soup = self.__soup.find(id="topic_detail_main").find(class_="conmain").find(id="maxwrap-maintopic").find(
            class_="clearfix contstxt outer-section")
        bb = BBSContent()
        bb.bbs_id = bbsId
        bb.uid = soup['uid']
        bb.from_floor = '0'
        bb.to_floor = '0'
        bb.content = LinkOperator.formatString(
            soup.find(class_="conright fr").find(class_="rconten").find(class_="conttxt").find(
                class_="w740").get_text())
        bb.forum_link_id = x
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
        bb.num_of_faces = self.__findGifNum(lis)
        bb.num_of_pictures = len(lis) - bb.num_of_faces
        return bb

    @classmethod
    def __findGifNum(self, lis):
        n = 0
        for lin in lis:
            if unicode(lin['src']).find('http://x.autoimg.cn/club/smiles/') and unicode(lin['src']).find('gif'):
                n += 1
        return n

    # Fixme
    @classmethod
    def __getBBSLinkFromLink(self, link, conn):
        soup = BeautifulSoup(HtmlCreator(link).getUrlRespHtml(), 'lxml')
        soupChild = soup.find(class_="content").find(class_="carea").find(id="subcontent").find_all(class_="list_dl")
        result = []
        for s in soupChild:
            try:
                lang = s.get('lang')
                if (lang != None):
                    langs = lang.split('|')
                    # print lang
                    _carId = unicode(langs[1])
                    _bbsId = unicode(langs[2])
                    _link = unicode(s.find_all('a', target="_blank")[0].get('href'))
                    _authorUid = unicode(langs[5])
                    _releaseTime = unicode(langs[4])
                    _replyNum = unicode(langs[3])
                    _clickNum = unicode('')
                    _lastReplyTime = unicode(s.find(class_="ttime").get_text())
                    _LastReplyUid = unicode(langs[6])
                    res = (_carId, _bbsId, _link, _authorUid, _releaseTime, _replyNum, _clickNum, _lastReplyTime,
                           _LastReplyUid)
                    result.append(res)
            except Exception, e:
                pass
                # logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' link=' + unicode(link) + ' Error = ' + unicode(e) + u"未知错误发生:" + unicode(s))
        # MysqlOperator(conn).insertForumLinks(set(result))
        return result

    @classmethod
    def getBBSLinksFromForumLink(self, linkList, conn):
        setValue = []
        for link in linkList:
            result = self.__getBBSLinkFromLink(link, conn)
            for res in result:
                setValue.append(res)
        MysqlOperator(conn).insertForumLinks(set(setValue))

    # 得到其他楼层的信息的list
    @classmethod
    def getAllFContentList(self, soup):
        # 除了楼主的内容
        list = soup.find(id="topic_detail_main").find(class_="conmain").find(id="maxwrap-reply").find_all(
            class_="clearfix contstxt outer-section")
        return list

    # 得到其他楼层内容
    @classmethod
    def getContents(cls, soups, x, bbsId):
        contentList = []
        for soup in soups:
            content = cls.__getContent(soup, x, bbsId)
            contentList.append(content)
        return contentList

    @classmethod
    def __getContent(cls, soup, x, bbsId):
        bb = BBSContent()
        bb.bbs_id = bbsId
        bb.uid = soup['uid']
        bb.from_floor = soup["rf"]
        bb.to_floor = bb.from_floor

        bb.content = soup.find(class_="conright fl").find(class_="rconten").find(class_="x-reply font14").find(
            class_="w740")
        content2 = None
        # face = None
        if bb.content == None:
            bb.content = BeautifulSoup("本楼已被管理员删除", "lxml")
        else:
            content2 = bb.content.find(class_="yy_reply_cont")

        if content2 != None:  # 说明有回复楼层
            try:
                bb.to_floor = bb.content.find(class_="relyhf").find(class_="relyhfcon").p.get_text().strip()
                bb.to_floor = LinkOperator.hanziConvertToNum(bb.to_floor)
            except:
                pass
            bb.content = LinkOperator.formatString(content2.get_text())
        else:
            bb.content = LinkOperator.formatString(bb.content.get_text())

        bb.forum_link_id = x
        bb.reply_time = soup["data-time"]
        # 特殊情况
        try:
            bb.device = LinkOperator.formatString(
                soup.find(class_="conright fl").find(class_="plr26 rtopconnext").find_all(target="_blank")[
                    -1].get_text())
        except Exception, e:
            bb.device = "noDevice"
        bb.num_of_links = bb.content.count('http://')
        bb.num_of_words = len(bb.content)

        # 计算图片表情数量 按有回复与无回复分类
        if bb.content == u'本楼已被管理员删除':
            lis = []
        elif bb.from_floor == bb.to_floor:
            lis = soup.find(class_="conright fl").find(class_="rconten").find(class_="x-reply font14").find(
                class_="w740").find_all('img')
        else:
            lis = soup.find(class_="conright fl").find(class_="rconten").find(class_="x-reply font14").find(
                class_="w740").find(class_="yy_reply_cont").find_all('img')

        bb.num_of_faces = cls.__findGifNum(lis)
        bb.num_of_pictures = len(lis) - bb.num_of_faces
        return bb

    @classmethod
    def getUser(cls, infoSoup, followingSoup, followersSoup, topicSoup, oilSoup, koubeiSoup, priceSoup, taskSoup,
                index):
        u = User()
        u.uid = index

        uData = infoSoup.find(class_="uData").get_text()
        if LinkOperator.formatString(uData).split('  ')[1].split(':')[1] == u'男':
            u.sex = 1
        else:
            u.sex = 0
        u.nickname = LinkOperator.formatString(uData).split('  ')[0].split(':')[1]
        u.location = LinkOperator.formatString(uData).split('  ')[-1].split(':')[1]

        if_auth = taskSoup.find(class_="all-task").find(class_="all-task-top").find_all(class_="all-task-box")[3].find(
            class_="task-sing-bom").get_text()
        if if_auth == u"已完成":
            u.auth = 1
        else:
            u.auth = 0

        u.auth_cars = ""

        u.follows = ''
        if followingSoup.find(class_="subdyn2") != None:
            u.num_of_follows = filter(lambda x: x.isdigit(),
                                  LinkOperator.formatString(
                                      followingSoup.find(class_="subdyn2").get_text().split(u"关注")[1]))
        if len(u.num_of_follows) == 0:
            u.num_of_follows = 0
        u.fans = ""

        if followersSoup.find(class_="subdyn2") != None:
            u.num_of_fans = filter(lambda x: x.isdigit(),
                               LinkOperator.formatString(
                                   followersSoup.find(class_="subdyn2").get_text().split(u"关注")[0]))
        if len(u.num_of_fans) == 0:
            u.num_of_fans = 0

        subTopic = topicSoup.find(class_="cl_m_item").find_all("ul")
        subTopicUl1 = subTopic[0].li.find_all("a")
        subTopicUl2 = subTopic[1]
        u.create_time = subTopicUl2.li.span.get_text()
        u.num_of_main_bbs = filter(lambda x: x.isdigit(), subTopicUl1[0].get_text())
        u.num_of_elite_bbs = filter(lambda x: x.isdigit(), subTopicUl1[1].get_text())
        u.level = filter(lambda x: x.isdigit(), topicSoup.find(class_="cl_m_item").find(class_="lv-txt").get_text())
        if len(u.level) == 0:
            u.level = 0
        u.points = filter(lambda x: x.isdigit(),
                          topicSoup.find(class_="cl_m_item").find(class_="lv-curr").get_text().split(u'：')[-1])
        if len(u.points) == 0:
            u.points = 0

        u.num_of_reply = 0
        u.num_of_reply_self = 0
        u.num_of_reply_others = 0
        u.first_post_time = "0001-01-01"
        u.last_post_time = "0001-01-01"
        u.avg_num_of_bbs = 0

        if len(oilSoup.find(class_="modifyPwd").get_text()) > 100:
            u.if_oil_consule = 1
        else:
            u.if_oil_consule = 0

        if len(koubeiSoup.find(class_="classification favoriteBg").get_text()) > 40:
            u.if_comment = 1
        else:
            u.if_comment = 0

        if priceSoup.find(class_="price-item-bd") != None:
            u.if_cost = 1
        else:
            u.if_cost = 0

        u.post_bbs_category_text = ""
        u.reply_bbs_category_text = ""

        return u
