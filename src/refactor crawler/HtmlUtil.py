#-*-coding:utf-8-*-
import logging
import urllib
import urllib2
import zlib

class HtmlCreator(object):

    def __init__(self,url,postDict={}, headerDict={}, timeout=0, useGzip=True):
        self.__url = url
        self.__postDict = postDict
        self.__headerDict = headerDict
        self.__timeout = timeout
        self.__useGzip = useGzip

    def __getUrlResponse(self,url, postDict={}, headerDict={}, timeout=0, useGzip=False):
        # makesure url is string, not unicode, otherwise urllib2.urlopen will error
        url = str(url);

        if (postDict):
            postData = urllib.urlencode(postDict);
            req = urllib2.Request(url, postData);
            req.add_header('Content-Type', "application/x-www-form-urlencoded");
        else:
            req = urllib2.Request(url);

        if (headerDict):
            # print "added header:",headerDict;
            for key in headerDict.keys():
                req.add_header(key, headerDict[key]);

        defHeaderDict = {
            'User-Agent': 'userAgentIE9',
            'Cache-Control': 'no-cache',
            'Accept': '*/*',
            'Connection': 'Keep-Alive',
        };

        # add default headers firstly
        for eachDefHd in defHeaderDict.keys():
            # print "add default header: %s=%s"%(eachDefHd,defHeaderDict[eachDefHd]);
            req.add_header(eachDefHd, defHeaderDict[eachDefHd]);

        if (useGzip):
            # print "use gzip for",url;
            req.add_header('Accept-Encoding', 'gzip, deflate');

        # add customized header later -> allow overwrite default header
        if (headerDict):
            # print "added header:",headerDict;
            for key in headerDict.keys():
                req.add_header(key, headerDict[key]);

        if (timeout > 0):
            # set timeout value if necessary
            resp = urllib2.urlopen(req, timeout=timeout);
        else:
            resp = urllib2.urlopen(req);

        return resp;

    def getUrlRespHtml(self):
        resp = self.__getUrlResponse(self.__url, self.__postDict, self.__headerDict, self.__timeout, self.__useGzip);
        respHtml = resp.read();
        if (self.__useGzip):
            respInfo = resp.info();
            if (("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
                respHtml = zlib.decompress(respHtml, 16 + zlib.MAX_WBITS);
                # print "+++ after unzip, len(respHtml)=",len(respHtml);
        encoding = resp.headers.getparam('charset')
        return respHtml.decode(encoding, 'ignore');