# -*-coding:utf-8-*-
import mysql.connector

config = {'host': 'localhost',
          'user': 'why',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }
conn = mysql.connector.connect(**config)
cur = conn.cursor()
cur.execute('SELECT distinct(bbs_id) FROM refactor_crawler.bbs_content order by bbs_id')
bbsIds = cur.fetchall()
i=0
bbsId = 0
while i<len(bbsIds):
    bbsId = bbsIds[i][0]
    cur.execute('insert into uid (uid) values (%s)',[bbsId])
    i += 1
    if i%10000 ==0:
        print i,u'提交'
        conn.commit()
conn.commit()
print 'Done!'