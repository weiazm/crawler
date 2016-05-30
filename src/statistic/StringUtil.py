# -*-coding:utf-8-*-
import string


class LinkOperator(object):
    # 将楼层汉字转为数字
    @classmethod
    def hanziConvertToNum(cls, str):
        str = str.split(" ")[-1]
        if str == u"主楼":
            return 0
        else:
            str_list = list(str)
            str_list.pop()
            res = "".join(str_list)
            if res == u"沙":
                return 1
            elif res == u"板":
                return 2
            elif res == u"地":
                return 3
            return res

    # 构造分页连接
    @classmethod
    def makeLinkByPage(cls, page, url):
        links = []
        parts = url.split("-")
        for x in range(1, string.atoi(page) + 1):
            link = parts[0] + "-" + parts[1] + "-" + parts[2] + "-" + parts[3] + "-" + str(x) + ".html"
            links.append(link)
        return links

    @classmethod
    def formatString(cls, strd):
        return unicode(strd.replace('\t', ' ').replace('\n', ' ').replace("'", "''").strip())

    @classmethod
    def makeLinkByCarId(self, carId):
        return 'http://club.autohome.com.cn/bbs/forum-c-' + str(
            carId) + '-1.html?orderby=dateline&qaType=-1#pvareaid=101061'

    @classmethod
    def makeLinkByPageNum(self, url, pageNum):
        n = 1
        result = []
        while n <= pageNum:
            parts = url.split('-')
            res = parts[0] + '-' + parts[1] + '-' + parts[2] + '-' + str(n) + '.' + parts[3].split('.')[1] + '-' + \
                  parts[4]
            result.append(res)
            n += 1
        return result
