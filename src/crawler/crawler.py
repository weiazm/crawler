#-*-coding:utf-8-*-
import urllib
import urllib2
import zlib
import MySQLdb
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

def do(num):
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

nums=[442,982,2123,771,66,3589]
for num in nums:
    do(num)