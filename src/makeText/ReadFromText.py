# -*-coding:utf-8-*-
import codecs

import mysql.connector

config = {'host': '172.17.26.167',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }

conn = conn = mysql.connector.connect(**config)
cur = conn.cursor()
f = codecs.open("D:\\workSpace\\workSpace\\dytang\\data\\result\\content_result0.txt", "rb", "utf-8","ignore")
i = 0
for line in f:
    i+=1
    part = line.strip().split("\t\t")
    #print part[1],part[2]
    try:
        cur.execute("UPDATE refactor_crawler.main_content SET emotion = %s WHERE bbs_id = %s",[part[2],part[1]])
        if i%10000 == 0:
            print i
            conn.commit()
    except:
        print line
        continue

conn.commit()
cur.close()
conn.close
f.close()