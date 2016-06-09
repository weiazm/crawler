# coding=utf-8
import datetime
import logging
import threading
import traceback

import mysql.connector

import jieba.posseg as pseg

config = {'host': '172.17.26.167',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }


def jieba_cut(raw):
    words = pseg.cut(raw)
    i=0
    words_count=[0]*37
    for w in words:
##        print w.word,w.flag
        if (w.flag=='a'):
            words_count[0]+=1
        if (w.flag=='ad'):
            words_count[1]+=1
        if (w.flag=='an'):
            words_count[2]+=1
        if (w.flag=='b'):
            words_count[3]+=1
        if (w.flag=='c'):
            words_count[4]+=1
        if (w.flag=='d'):
            words_count[5]+=1
        if (w.flag=='e'):
            words_count[6]+=1
        if (w.flag=='f'):
            words_count[7]+=1
        if (w.flag=='g'):
            words_count[8]+=1
        if (w.flag=='h'):
            words_count[9]+=1
        if (w.flag=='i'):
            words_count[10]+=1
        if (w.flag=='j'):
            words_count[11]+=1
        if (w.flag=='k'):
            words_count[12]+=1
        if (w.flag=='l'):
            words_count[13]+=1
        if (w.flag=='m'):
            words_count[14]+=1
        if (w.flag=='n'):
            words_count[15]+=1
        if (w.flag=='nr'):
            words_count[16]+=1
        if (w.flag=='ns'):
            words_count[17]+=1
        if (w.flag=='nt'):
            words_count[18]+=1
        if (w.flag=='nz'):
            words_count[19]+=1
        if (w.flag=='o'):
            words_count[20]+=1
        if (w.flag=='p'):
            words_count[21]+=1
        if (w.flag=='q'):
            words_count[22]+=1
        if (w.flag=='r'):
            words_count[23]+=1
        if (w.flag=='s'):
            words_count[24]+=1
        if (w.flag=='t'):
            words_count[25]+=1
        if (w.flag=='u'):
            words_count[26]+=1
        if (w.flag=='v'):
            words_count[27]+=1
        if (w.flag=='vd'):
            words_count[28]+=1
        if (w.flag=='vn'):
            words_count[29]+=1
        if (w.flag=='w'):
            words_count[30]+=1
        if (w.flag=='x'):
            words_count[31]+=1
        if (w.flag=='y'):
            words_count[32]+=1
        if (w.flag=='z'):
            words_count[33]+=1
        #not belong to ICTPOS3.0
        if (w.flag=='uj'):
            words_count[34]+=1
        if (w.flag=='eng'):
            words_count[35]+=1
        words_count[36]+=1

    #extract the characteristc terms
    import jieba.analyse
    topK=100
    tags = jieba.analyse.extract_tags(raw, topK=topK)
    character_terms = len(tags)
##    print(",".join(tags))

    #calculate the ambiguity of the review
    import math

    quantifer=words_count[14]
    noun=words_count[15]+1
    verb=words_count[27]+1
    allterms=words_count[36]+1
    ambiguity=((quantifer+1)*1.0/allterms)*(noun*1.0/(noun+verb))*math.log(1+character_terms)

##    print 'ambiguity=',quantifer,noun,verb,allterms,character_terms,math.log(1+character_terms),ambiguity
    #print ambiguity
    return words_count,ambiguity






def run(id):
    conn = mysql.connector.connect(**config)
    logging.basicConfig(filename='jieba.log', level=logging.DEBUG)
    cur = conn.cursor()
    id = id
    cur.execute('SELECT start,end from count_jieba where id = %s', [id])
    startEnd = cur.fetchall()[0]
    cur.close()
    x = startEnd[0]
    index = x
    while index < startEnd[1]:
        try:


            cur = conn.cursor()
            cur.execute('select * from main_content where id = %s', [index])
            main_content = cur.fetchall()[0]
            bbs_id = main_content[3]
            content = main_content[8]
            #content = ''
            result = jieba_cut(content)
            words_count = result[0]
            ambiguity = result[1]
            #print index,words_count, ambiguity

            cur.execute('INSERT INTO refactor_crawler.main_content_jieba(bbs_id,a,ad,an,b,c,d,e,f,g,h,i,j,k,l,m,n,nr,ns,nt,nz,o,p,q,r,s,t,u,v,vd,vn,w,x,y,z,uj,eng,total,ambiguity)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        [bbs_id,words_count[0],words_count[1],words_count[2],words_count[3],words_count[4],words_count[5],words_count[6],words_count[7],words_count[8],words_count[9],words_count[10],words_count[11],words_count[12],words_count[13],words_count[14],words_count[15],words_count[16],words_count[17],words_count[18],words_count[19],words_count[20],words_count[21],words_count[22],words_count[23],words_count[24],words_count[25],words_count[26],words_count[27],words_count[28],words_count[29],words_count[30],words_count[31],words_count[32],words_count[33],words_count[34],words_count[35],words_count[36],ambiguity])


        except Exception, e:
            logging.error(' id=' + str(index) + u"分词时发生错误" + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + ' Error = ' + str(e) + '---')
            traceback.print_exc()
            conn.rollback()
            index += 1
            continue
        else:
            index += 1
            cur.execute('update count_jieba set start = %s where id = %s', [index, id])
            conn.commit()
            cur.close()
            print "Done!"


threads = []
# 1, 177
for i in xrange(70, 80):
    th = threading.Thread(target=run, args=(i,))
    threads.append(th)

for t in threads:
    t.start()
# 等待子线程结束
for t in threads:
    t.join()
