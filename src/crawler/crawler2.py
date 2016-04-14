#-*-coding:utf-8-*-
import urllib
import urllib2
import zlib
import MySQLdb
import traceback
import string
import logging
import datetime
from bs4 import BeautifulSoup

def getUrlResponse(url, postDict={}, headerDict={}, timeout=0, useGzip=False) :
    # makesure url is string, not unicode, otherwise urllib2.urlopen will error
    url = str(url);

    if (postDict) :
        postData = urllib.urlencode(postDict);
        req = urllib2.Request(url, postData);
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
    else :
        req = urllib2.Request(url);

    if(headerDict) :
        #print "added header:",headerDict;
        for key in headerDict.keys() :
            req.add_header(key, headerDict[key]);

    defHeaderDict = {
        'User-Agent'    : 'userAgentIE9',
        'Cache-Control' : 'no-cache',
        'Accept'        : '*/*',
        'Connection'    : 'Keep-Alive',
    };

    # add default headers firstly
    for eachDefHd in defHeaderDict.keys() :
        #print "add default header: %s=%s"%(eachDefHd,defHeaderDict[eachDefHd]);
        req.add_header(eachDefHd, defHeaderDict[eachDefHd]);

    if(useGzip) :
        #print "use gzip for",url;
        req.add_header('Accept-Encoding', 'gzip, deflate');

    # add customized header later -> allow overwrite default header
    if(headerDict) :
        #print "added header:",headerDict;
        for key in headerDict.keys() :
            req.add_header(key, headerDict[key]);

    if(timeout > 0) :
        # set timeout value if necessary
        resp = urllib2.urlopen(req, timeout=timeout);
    else :
        resp = urllib2.urlopen(req);

    return resp;

def getUrlRespHtml(url, postDict={}, headerDict={}, timeout=0, useGzip=True) :
    resp = getUrlResponse(url, postDict, headerDict, timeout, useGzip);
    respHtml = resp.read();
    if(useGzip) :
        respInfo = resp.info();
        if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")) :
            respHtml = zlib.decompress(respHtml, 16+zlib.MAX_WBITS);
            #print "+++ after unzip, len(respHtml)=",len(respHtml);
    encoding = resp.headers.getparam('charset')
    return respHtml.decode(encoding,'ignore');

def getLinsFromUrl(url):
    html = getUrlRespHtml(url)
    soup = BeautifulSoup(html,'lxml')
    lins=[]
    for link in soup.find_all('a',target="_blank"):
        lin=link.get('href')
        if lin[0:11] == '/bbs/thread':
            lins.append(lin)
    #去重复
    lins = set(lins)
    return lins

def getLinsFromNum(num):
    conn = MySQLdb.connect("localhost", "root", "1234", "crawler")
    cursor = conn.cursor()
    n=1
    res = []
    while n<=1000:
        url='http://club.autohome.com.cn/bbs/forum-c-%s-%s.html?orderby=dateline&qaType=-1#pvareaid=101061'%(num,n)
        n+=1
        print url
        lins = getLinsFromUrl(url)
        for lin in lins:
            res.append(lin)
    res = set(res)
    n=1
    for lin in res:
        cursor.execute("insert into forum_lins(lin,category) values(\'%s\',\'%s\')"%(lin,num))
        n+=1
        print n
        if n%2000==0:
            conn.commit()
            print "commit"
    conn.commit()
    conn.close()

#nums=[442,982,2123,771,66,3589]
#for num in nums:
#    getLinsFromNum(num)
def selectLinkById(id,conn):

    #conn = MySQLdb.connect("localhost", "root", "1234", "crawler")
    cursor = conn.cursor()
    cursor.execute("select * from forum_lins where id=%s"%(id))
    return "http://club.autohome.com.cn"+cursor.fetchall()[0][1]

def findTotlePages(str):
    char = '/'
    char2 = u'页'
    posf = str.index(char)
    post = str.index(char2)
    #print posf,post
    return str[posf+2:post-1]

#得到楼主的回复与个人信息
def getF0Content(soup):
    #f0的内容
    soup = soup.find(id="topic_detail_main").find(class_="conmain").find(id="maxwrap-maintopic").find(class_="clearfix contstxt outer-section")
    #返回楼主uid，楼层,发帖时间，帖子内容,回复楼层
    try:
        return soup["uid"],0,soup["data-time"],soup.find(class_="conright fr").find(class_="rconten").find(class_="conttxt").find(class_="w740").get_text().strip(),0
    except:
        return soup["uid"],0,soup["data-time"],soup.find(class_="conright fr").find(class_="rconten").find(class_="conttxt tpt").get_text().strip(),1

#得到其他楼层的信息的list
def getAllFContentList(soup):
    #除了楼主的内容
    list = soup.find(id="topic_detail_main").find(class_="conmain").find(id="maxwrap-reply").find_all(class_="clearfix contstxt outer-section")
    return list

#将表情链接转为号码字符串
def faceLinkConvertToNumStr(faces):
    result = ""
    for face in faces:
        result=result + face["src"].split("/")[-1].split(".")[0]+"."
    return result

#将楼层汉字转为数字
def hanziConvertToNum(str):
    str = str.split(" ")[-1]
    if str==u"主楼":
        return 0
    else:
        str_list = list(str)
        str_list.pop()
        res="".join(str_list)
        if res==u"沙":
            return 1
        elif res==u"板":
            return 2
        elif res==u"地":
            return 3
        return res


#根据list内容得到需要的东西
def getAllFContent(list):
    result = []
    for soup in list:
        uid = soup["uid"]
        dataTime = soup["data-time"]
        floorNum = soup["rf"]
        content = soup.find(class_="conright fl").find(class_="rconten").find(class_="x-reply font14").find(class_="w740")
        content2 = None
        #face = None
        if content == None:
            content = BeautifulSoup("本楼已被管理员删除","lxml")
        else:
            content2 = content.find(class_="yy_reply_cont")
        replyFloorNum = floorNum
        if content2!= None:
            #face = content2.find_all("img")
            #face = faceLinkConvertToNumStr(face)
            #print content.find(class_="relyhf").find(class_="relyhfcon").p.find_all("a").get_text()
            try:
                replyFloorNum = content.find(class_="relyhf").find(class_="relyhfcon").p.get_text().strip()
                replyFloorNum = hanziConvertToNum(replyFloorNum)
            except:
                pass
            content = content2.get_text().strip()
        else:
            #face = content.find_all("img")
            #face = faceLinkConvertToNumStr(face)
            content = content.get_text().strip()
        #res = [uid,floorNum,dataTime,content,face,replyFloorNum]
        res = [uid, floorNum, dataTime, content, replyFloorNum]
        result.append(res)
    return result

#得到标题
def getTitle(soup):
    if soup.find(class_="maxtitle") != None:
        return soup.find(class_="maxtitle").get_text()
    elif soup.find(class_="qa-maxtitle") != None:
        return soup.find(class_="qa-maxtitle").get_text()

#构造分页链接
def makeLinkByPage(page,url):
    links = []
    parts = url.split("-")
    bbsId = parts[3]
    for x in range (1,string.atoi(page)+1):
        link = parts[0]+"-"+parts[1]+"-"+parts[2]+"-"+parts[3]+"-"+str(x)+".html"
        links.append(link)
    return bbsId,links

def insertIntoDatabase(conn,forum_lin_id,post_id,title,uid, from_floor, reply_time, content,to_floor):
    cursor = conn.cursor()
    title = title.replace("\"","-")
    content = content.replace("\"","-")
    sql = "insert into forum_content value(0,"+forum_lin_id+","+post_id+",\""+title+"\","+uid+"," +from_floor+"," +reply_time+",\""+ content+"\","+to_floor+")"
    #print sql
    cursor.execute(sql)


conn = MySQLdb.connect("localhost", "root", "1234", "crawler",charset="utf8")
logging.basicConfig(filename='log2.log',level=logging.DEBUG)
#for x in range(924,990945):
for x in range(24556, 30000):
    try:
        url = selectLinkById(x,conn)
        try:
            html = getUrlRespHtml(url)
        except urllib2.HTTPError, e:
            logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' id=' + str(x) + ' HTTPError = ' + str(e.code)+u"帖子可能被删除:"+url)
            continue
        soup = BeautifulSoup(html,"lxml")
        title = getTitle(soup)
        F0 = getF0Content(soup)
        page = findTotlePages(soup.find(id="x-pages2").get_text()).strip()
        print str(x)+" "+page+u"页 "+url
        soups = []
        links = makeLinkByPage(page,url)
        #print x,links[0],title,F0[0], F0[1], F0[2], F0[3],F0[4]
        insertIntoDatabase(conn, unicode(x),unicode(links[0]),unicode(title),unicode(F0[0]), unicode(F0[1]), unicode(F0[2]), unicode(F0[3]),unicode(F0[4]))
        for link in links[1]:
            soups.append(BeautifulSoup(getUrlRespHtml(link),"lxml"))
        for soup in soups:
            for lis in getAllFContent(getAllFContentList(soup)):
                #print x,links[0],title,lis[0],lis[1],lis[2],lis[3],lis[4]
                insertIntoDatabase(conn, unicode(x),unicode(links[0]),unicode(title),unicode(lis[0]),unicode(lis[1]),unicode(lis[2]),unicode(lis[3]),unicode(lis[4]))
    except Exception,e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' id=' + str(x) + ' Error = ' + str(e) + u"未知错误发生:" + url)
        conn.rollback()
        continue
    else:
        conn.commit()