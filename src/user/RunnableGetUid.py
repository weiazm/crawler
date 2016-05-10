# -*-coding:utf-8-*-
import mysql.connector
#database connetcion
config = {'host': 'localhost',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }
conn = mysql.connector.connect(**config)
cur = conn.cursor()
cur.execute('SELECT distinct(refactor_crawler.bbs_content.uid) FROM refactor_crawler.bbs_content order by uid')
uids = cur.fetchall()
i = 0
uid = 0
while i < len(uids):
    uid = uids[i][0]
    cur.execute('insert into uid (uid) values (%s)', [uid])
    i += 1
    if i % 100000 == 0:
        print i
        conn.commit()
conn.commit()
print 'Done!'
