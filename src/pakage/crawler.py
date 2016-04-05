###-*-encoding:utf-8-*-
import requests
import urllib2
import urllib
import httplib
import re
import bs4
from bs4 import BeautifulSoup
import pprint
import time
import locale
import logging
import sys
import gc
import datetime
##reload(sys)
##sys.setdefaultencoding("utf8")



def main():
##    print sys.getfilesystemencoding(),sys.getdefaultencoding()
##    print "购买车型".decode("utf8").encode('gb2312')
##    print "凹凸有车".decode("utf8").encode('utf8').decode("utf8")
##    print "凹凸有车".decode("utf8")
##    print "凹凸有车"
##    print u"凹凸有车"
##    print "哈哈".decode("utf8")
    logging.basicConfig(filename='log.log',level=logging.DEBUG)
    logging.info("starting...")
    update_carmodel_country()

    #测评数据
##    crawl_cartest()
    #汽车基本信息
##    crawl_carmodel()
    #车型详细信息
##    get_car_model_detail("3335")
    #口碑信息

##    crawler_wom("/2619/index_6.html")
##    get_car_wom_detail("/3335")
##    crawler_wom("/2518")

##    get_all_cars_wom()

    pass

    #字符集测试
##    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


##    s="/3335"
##    s1="/3335/index.html"
##    print s.split("/")[1], s1.split("/")[1]

##    s="http://www.autohome.com.cn/2683/#levelsource=000000000_0&pvareaid=101594"
##    print s[27:].split("/")[0]
#-------------------------------------------------------------------------------
def get_all_cars_wom():
    import MySQLdb
    cnx = MySQLdb.connect(user='root', password='19781119',
                          host='127.0.0.1',
                          database='truth-discovery')
    cursor = cnx.cursor()

    i=0
    data=[]
    try:
        sql = ("select car_model_id from car_model ") #  where car_rival_2>0 and car_rival_3=0
##        sql="select ceiling(car_rival_3/15) as sumsum,car_model_id from car_model where car_rival_1/15-ceiling(car_rival_3/15)>1"

        # Insert new employee
        cursor.execute(sql)
        for car_model_id in cursor: # sumsum,
##          print(car_model_id[0])
##          print int(sumsum), unicode(car_model_id)
          data.append(car_model_id[0])

##            data.append((int(sumsum), unicode(car_model_id)))

        cnx.commit()
        i+=1

    except MySQLdb.Error as err:
        print i,"th row, Something went wrong: {}".format(err)
        cnx.commit()
        cnx.close()
        return

    cnx.close()
    print "start...."
    #get wom
    first=0
    for xy in data:
##        print "/"+str(xy[1])+"/index_"+str(xy[0]+1)+".html"
##        if xy=="3156":
##            first=1
####            return
##            #continue
##        if first==1:
        crawler_wom("/"+xy)
##        crawler_wom("/"+str(xy[1])+"/index_"+str(xy[0]+1)+".html")
##            check_wom_enough(xy)

        gc.collect()

#-------------------------------------------------------------------------------
def check_wom_enough(car_id):
    #car_id looks like "/3335" or "/3335/index_2.html"
    baselink="http://k.autohome.com.cn/"
    link=baselink+car_id
    next_page=car_id
##    print link
    try:

        req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
        usock = urllib2.urlopen(req)
        encoding = usock.headers.getparam('charset')
        #print encoding

        page = usock.read()#.decode(encoding)
        usock.close()
        #
        soup = BeautifulSoup(page)

        #print netpage
        wom_num1="0"
        wom_num2="0"

        netpage = soup.find("a",class_="page-item-last")
        if netpage!=None:
            str=netpage["href"]
            st=str.find("_")
            end=str.find(".")
            wom_num1=int(str[st+1:end])*15

        netpage = soup.find("span",class_="number-ren")
        if netpage!=None:
            wom_num2=unicode(netpage.string)

        print link,wom_num1,wom_num2
        davedb_wom_num(car_id,wom_num1,wom_num2)



    except urllib2.HTTPError, e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' HTTPError = ' + str(e.code))
        #if http error repeat
        time.sleep(5)
        check_wom_enough(next_page)
    except urllib2.URLError, e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' URLError = ' + str(e.reason))
        #if http error repeat
        time.sleep(5)
        check_wom_enough(next_page)
    except httplib.HTTPException, e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' HTTPException = ' + str(e.code))
        #if http error repeat
        time.sleep(5)
        check_wom_enough(next_page)
    except Exception:
        import traceback
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' Generic exception: ' + traceback.format_exc())
        #if http error repeat
        time.sleep(5)
        check_wom_enough(next_page)

def davedb_wom_num(car_id,wom_num1,wom_num2):
    #car_id looks like "/3335" or "/3335/index_2.html"
    import MySQLdb
    cnx = MySQLdb.connect(user='root', password='19781119',
                          host='127.0.0.1',
                          database='truth-discovery',use_unicode=True)#,charset='utf8',
    cursor = cnx.cursor()
##    cursor.execute("set names gbk")

    i=0

    try:
        add_tweets = ("update car_model set "
               " car_rival_1 = %s, car_rival_2 = %s "
               " where car_model_id = %s")

        data_tweets = (wom_num1,wom_num2,car_id)

        # Insert new employee
        cursor.execute(add_tweets, data_tweets)
        cnx.commit()
        i+=1

    except MySQLdb.Error as err:
        logging.info( str(i) + "th row, Something went wrong: {}".format(err))
        cnx.commit()
        cnx.close()
        return

    cnx.close()
#-------------------------------------------------------------------------------
def crawler_wom(car_id):
    #car_id looks like "/3335" or "/3335/index_2.html"
    baselink="http://k.autohome.com.cn"
    link=baselink+car_id
    next_page=car_id
##    print link
    try:

        req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
        usock = urllib2.urlopen(req)
        encoding = usock.headers.getparam('charset')
        #print encoding

        page = usock.read()#.decode(encoding)
        usock.close()
        #
        soup = BeautifulSoup(page)
        netpage = soup.find("a",class_="page-item-next")
        firstpage=soup.find("a",class_="page-item-info")
        #print netpage

        if netpage!=None:
            get_car_wom_detail(car_id,soup)
    ##                print baselink+netpage["href"]
            if (netpage["href"]!="###"):
    ##            print netpage["href"]
                next_page=netpage["href"]
                crawler_wom(next_page)
        elif firstpage!=None:
            time.sleep(1)
            crawler_wom(next_page)



    except urllib2.HTTPError, e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' HTTPError = ' + str(e.code))
        #if http error repeat
        time.sleep(5)
        crawler_wom(next_page)
    except urllib2.URLError, e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' URLError = ' + str(e.reason))
        #if http error repeat
        time.sleep(5)
        crawler_wom(next_page)
    except httplib.HTTPException, e:
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' HTTPException = ' + str(e.code))
        #if http error repeat
        time.sleep(5)
        crawler_wom(next_page)
    except Exception:
        import traceback
        logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' car_id='+car_id+' Generic exception: ' + traceback.format_exc())
        #if http error repeat
        time.sleep(5)
        crawler_wom(next_page)

def get_car_wom_detail(car_id,soup):


    data=[]
    first=1
    i=0
    for rootag in soup.select("div.mouthcon-cont-left"):
        xx=["","","","","","","","","","","","","","","",""]
        #user name
##        print rootag.find("div",class_="name-text").p.text.strip()
        xx[0]=rootag.find("div",class_="name-text").p.text.strip()
        j=0
        #详细口碑信息
        for dt in rootag.find_all("dt"):
##            print dt.text.strip()
            if dt.text.strip().encode("utf8")=="购买车型":
##                print "--"+dt.find_next("dd").text.replace("\n", " ").strip()
                xx[1]=dt.find_next("dd").text.replace("\n", " ").strip()
            elif dt.text.strip()=="购买地点".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[2]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="购车经销商".decode("utf8"):
##                print dt.find_next("dd").a.text.strip()
                pass

            elif dt.text.strip()=="购买时间".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[3]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="裸车购买价".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[4]=dt.find_next("dd").text.strip()
            elif dt.text.strip().find("目前行驶".decode("utf8"))>=0:
##                print "--"+dt.find_next("dd").text.replace("\n", " ").strip()
                xx[5]=dt.find_next("dd").text.replace("\n", " ").strip()

            elif dt.text.strip()=="空间".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[6]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="动力".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[7]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="操控".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[8]=dt.find_next("dd").text.strip()
            elif (dt.text.strip()=="油耗".decode("utf8")) | (dt.text.strip()=="耗电量".decode("utf8")):
##                print "--"+dt.find_next("dd").text.strip()
                xx[9]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="舒适性".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[10]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="外观".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[11]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="内饰".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[12]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="性价比".decode("utf8"):
##                print "--"+dt.find_next("dd").text.strip()
                xx[13]=dt.find_next("dd").text.strip()
            elif dt.text.strip()=="购车目的".decode("utf8"):
##                print "--"+dt.find_next("dd").text.replace("\n", " ").strip()
                xx[14]=dt.find_next("dd").text.replace("\n", " ").strip()
            j=j+1
        #wom time
##        print rootag.parent.find("span",class_="time").a.text[:10]
        xx[15]=rootag.parent.find("span",class_="time").a.text[:10]

##        j=0
##        for dd in rootag.find_all("dd"):
##            atag=dd.find("a")
##            # remove the supplier
##            if isinstance(atag,bs4.Tag):
##                if atag.has_attr('class'):
##                    continue
##                    print atag.text.strip()
##            print dd.text.replace("\n", " ").strip()
##            xx.append(dd.text.replace("\n", " ").strip())
##            j=j+1
##        if j<15:
##            print "----------------------",j
        data.append(xx)
        i=i+1

    davedb_wom(car_id,data)
##    pp = pprint.PrettyPrinter()
##    pp.pprint(data)
    return


##    pass

def davedb_wom(car_id,data):
    #car_id looks like "/3335" or "/3335/index_2.html"
    import MySQLdb
    cnx = MySQLdb.connect(user='root', password='19781119',
                          host='127.0.0.1',
                          database='truth-discovery',use_unicode=True)#,charset='utf8',
    cursor = cnx.cursor()
##    cursor.execute("set names gbk")

    i=0
    for x in data:
        try:
            add_tweets = ("INSERT INTO car_wom "
                   "(car_id,user_id,car_model_detail,buy_address,buy_date,buy_price,car_gas,car_distance,evl_space,evl_engine,evl_drive,evl_gas,evl_comfort,evl_exterior,evl_interior,evl_price_perfomance,buy_purpose,car_wom_date) "
                   "VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)")
##            print x[5].split(" ")[0],x[5].split(" ")[1]
            d1=d2=""
            #gas and distance #.encode("utf8")  .encode("mbcs") .decode("utf-8")
            if len(x[5])>0:

                d1= x[5].split(" ")[0]
                if len(x[5].split(" "))>1:
                    d2= x[5].split(" ")[1]
            print "---->insert ",x[0] , x[1],d1,d2
##            if isinstance(x[0], unicode):
##                print x[0]
####                print "1212121"

            data_tweets = (car_id.split("/")[1],x[0] ,x[1],x[2],x[3],x[4],d1,d2,x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15])

            # Insert new employee
            cursor.execute(add_tweets, data_tweets)
##            cursor.getsql()
            cnx.commit()
            i+=1

        except MySQLdb.Error as err:
            logging.info( i + "th row, Something went wrong: {}".format(err))
            cnx.commit()
            cnx.close()
            return

    cnx.close()
#-------------------------------------------------------------------------------
def get_car_model_detail(car_id):
    link="http://www.autohome.com.cn/"+car_id


    req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
    usock = urllib2.urlopen(req)
    encoding = usock.headers.getparam('charset')
    print encoding,link
    #time.sleep(2)
    page = usock.read()#.decode(encoding)
    usock.close()


    soup = BeautifulSoup(page)

    data=[]
    first=1
    i=0
    xx=[]
##    #?????
##    ss=soup.select("a.font-score")[0].text
##    xx.append(ss)
    #??????
    for rootag in soup.select("div.rival-car"):
        ss= rootag.find_next("a")["href"][27:].split("/")[0]#rootag.find_next("a").text.replace("\n","").strip()#,rootag.find_next("div").a.text
        if(ss!=car_id):
            xx.append(ss)
            print ss
    #??????
    ss=soup.select("div.autoseries-info")[0].find("dl").find("dt").a.text
    ss=ss[:len(ss)-1]
    print ss.split("-")[0],ss.split("-")[1]
    xx.append(ss.split("-")[0])
    xx.append(ss.split("-")[1])
    data.append(xx)


    savedb_car_detail(car_id,data)

    pass

def savedb_car_detail(car_model_id,data):
 #
    import MySQLdb
    cnx = MySQLdb.connect(user='root', password='19781119',
                          host='127.0.0.1',
                          database='truth-discovery')
    cursor = cnx.cursor()

    i=0
    for x in data:
        try:
            add_tweets = ("update car_model set "
                   " car_rival_1 = %s, "
                   " car_rival_2 = %s,"
                   " car_rival_3 = %s,"
                   " car_rival_4 = %s,"
                   " car_price_low = %s,"
                   " car_price_high = %s"
                   " where car_model_id = %s")

            data_tweets = (x[0],x[1],x[2],x[3],x[4],x[5],car_model_id)

            # Insert new employee
            cursor.execute(add_tweets, data_tweets)
            cnx.commit()
            i+=1

        except MySQLdb.Error as err:
            print i,"th row, Something went wrong: {}".format(err)
            cnx.commit()
            cnx.close()
            return

    cnx.close()

#-------------------------------------------------------------------------------
def crawl_cartest():
    t=["1","2","3"]

    for bigtype in t:
        get_cartest(bigtype)

def get_cartest(test_type):
    link="http://www.autohome.com.cn/channel2/bestauto/list.aspx?type="+test_type
    print link

    req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
    usock = urllib2.urlopen(req)
    encoding = usock.headers.getparam('charset')
    print encoding
    page = usock.read().decode(encoding)
    usock.close()

    soup = BeautifulSoup(page)
    data=[]
    first=1
    for rootag in soup.find_all("tr"):
        if first==1:
            first=0
            continue
        x=["","","",""]
        i=0
        for tag in rootag.descendants:
            if (tag.name=="p") & (i==1):
                for ttag in tag.children:
                    if ttag.name=="a":
                        x[i]=unicode(ttag.string)
                        i=i+1
            elif (tag.name=="p") & (i!=1):
                x[i]=unicode(tag.string)
                i=i+1
##                print i,x[i]

        data.append(x)
##        print x
    savedb_cartest(test_type,data)
    print "--------------------"
##    print data
    return

def savedb_cartest(testype,data):
 #
    import MySQLdb
    cnx = MySQLdb.connect(user='root', password='19781119',
                          host='127.0.0.1',
                          database='truth-discovery')
    cursor = cnx.cursor()

    i=0
    for x in data:
        try:
            add_tweets = ("INSERT INTO car_test "
                   "(test_type,test_rank,car_model,car_model_detail,test_date,test_value) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
            print x[0],x[1]
##            y=x[1]
            y = x[1].split(" ")[1]

            if testype=="1":testype="speed"
            if testype=="2":testype="brake"
            if testype=="3":testype="gas"
            data_tweets = (testype,x[0],y,x[1],x[2],x[3])

            # Insert new employee
            cursor.execute(add_tweets, data_tweets)
            cnx.commit()
            i+=1

        except MySQLdb.Error as err:
            print i,"th row, Something went wrong: {}".format(err)
            cnx.commit()
            cnx.close()
            return

    cnx.close()
#-------------------------------------------------------------------------------
def crawl_carmodel():
    t=["a00","a0","a","b","c","d","suv","mpv","s","p","mb","qk"]
##    t=["a00"]

    for bigtype in t:
        get_carmodel(bigtype)

def get_carmodel(bigtype):
    link="http://www.autohome.com.cn/"+bigtype+"/"

    req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
    usock = urllib2.urlopen(req)
    encoding = usock.headers.getparam('charset')
    page = usock.read()#.decode(encoding)
    usock.close()

    soup = BeautifulSoup(page)

    for rootag in soup.select("div.tab-content-item"):
##        print "iiiiiiiiiii"
        for tttag in rootag.descendants:
            if tttag.name=="dl":
                car_brand=""



                for tag in tttag.children:

                    if tag.name=="dt":
                        for descendant in tag.descendants:
                            if (descendant.name=="div") :
                                for child in descendant.children:
                                    if (child.name=="a") :
                                        car_brand=unicode(child.string)
                                        print car_brand

                    if tag.name=="dd":

                        for child in tag.children:
                            car_company=""
                            if ((child.name=="div")) :

                                data=[]
                                car_company=unicode(child.string)
                                if (car_company is None) | (car_company=="None"):
                                    continue

                                for descendant in child.find_next("ul").descendants:

                                    if (descendant.name=="h4") :
                                        for child in descendant.children:
                                            if (child.name=="a") :
                                                x=["",""]
                                                x[0]=unicode(child.string)
                                                x[1]=child['href']
                                                data.append(x)
                                                print x[1],unicode(child.string)
                                savedb_carmodel(bigtype,data,car_brand,car_company)
        return



def savedb_carmodel(bigtype,data,car_brand,car_company):
 #
    import MySQLdb
    cnx = MySQLdb.connect(user='root', password='19781119',
                          host='127.0.0.1',
                          database='truth-discovery')
    cursor = cnx.cursor()
##    delete_cluster=("TRUNCATE fruit_nutrient")
##    cursor.execute(delete_cluster)
##    cnx.commit()
    i=0

    for x in data:

        try:
            add_tweets = ("INSERT INTO car_model "
                   "(car_type,car_model,car_model_url,car_company,car_brand) "
                   "VALUES (%s, %s, %s, %s, %s)")

            data_tweets = (bigtype, x[0],x[1],car_company,car_brand)

            # Insert new employee
            cursor.execute(add_tweets, data_tweets)
            cnx.commit()
            i+=1

        except MySQLdb.Error as err:
            print i,"th row, Something went wrong: {}".format(err)
            cnx.commit()
            cnx.close()
            return

    cnx.close()
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def update_carmodel_country():

    for bigtype in range(12,13):
        get_china_carmodel(bigtype)

def get_china_carmodel(brand_country):
    link="http://www.autohome.com.cn/car/0_0-0.0_0.0-0-0-0-0-0-"+str(brand_country)+"-0-0/"

    req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
    usock = urllib2.urlopen(req)
    encoding = usock.headers.getparam('charset')
    page = usock.read()#.decode(encoding)
    usock.close()

    soup = BeautifulSoup(page)

    for rootag in soup.select("div.tab-content-item"):
        print "iiiiiiiiiii"
        for tttag in rootag.descendants:
            if tttag.name=="dl":
                car_brand=""



                for tag in tttag.children:

                    if tag.name=="dt":
                        for descendant in tag.descendants:
                            if (descendant.name=="div") :
                                for child in descendant.children:
                                    if (child.name=="a") :
                                        car_brand=unicode(child.string)
                                        print car_brand

                    if tag.name=="dd":

                        for child in tag.children:
                            car_company=""
                            if ((child.name=="div")) :

                                data=[]
                                car_company=unicode(child.string)
                                if (car_company is None) | (car_company=="None"):
                                    continue

                                for descendant in child.find_next("ul").descendants:

                                    if (descendant.name=="h4") :
                                        for child in descendant.children:
                                            if (child.name=="a") :
                                                x=["",""]
                                                x[0]=unicode(child.string)
                                                x[1]=child['href']
                                                data.append(x)
                                                print x[1],unicode(child.string)
                                savedb_china_carmodel(brand_country,data,car_brand,car_company)
        return

def savedb_china_carmodel(brand_country,data,car_brand,car_company):
 #
    import MySQLdb
    cnx = MySQLdb.connect(user='root', password='19781119',
                          host='127.0.0.1',
                          database='truth-discovery')
    cursor = cnx.cursor()
##    delete_cluster=("TRUNCATE fruit_nutrient")
##    cursor.execute(delete_cluster)
##    cnx.commit()
    i=0

    for x in data:

        try:
            add_tweets = ("update car_model set china_brand= %s "
                   "where car_model = %s and car_company= %s and car_brand= %s")

            data_tweets = (brand_country,x[0],car_company,car_brand)

            # Insert new employee
            cursor.execute(add_tweets, data_tweets)
            cnx.commit()
            i+=1

        except MySQLdb.Error as err:
            print i,"th row, Something went wrong: {}".format(err)
            cnx.commit()
            cnx.close()
            return

    cnx.close()


if __name__ == '__main__':
    main()
