#-*-coding:utf-8-*-
import logging

class LinkOperator(object):

    @classmethod
    def formatString(cls,str):
        return str.replace('\t', ' ').replace('\n', ' ').replace('\"')

    @classmethod
    def makeLinkByCarId(self,carId):
        return 'http://club.autohome.com.cn/bbs/forum-c-'+str(carId)+'-1.html?orderby=dateline&qaType=-1#pvareaid=101061'

    @classmethod
    def makeLinkByPageNum(self,url,pageNum):
        n = 1
        result = []
        while n<=pageNum:
            parts = url.split('-')
            res = parts[0]+'-'+parts[1]+'-'+parts[2]+'-'+str(n)+'.'+parts[3].split('.')[1]+'-'+parts[4]
            result.append(res)
            n+=1
        return result