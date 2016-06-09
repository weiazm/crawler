# -*-coding:utf-8-*-

import mysql.connector

config = {'host': 'localhost',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }
conn = mysql.connector.connect(**config)
cur = conn.cursor()
# 5617263	204
i = 0
id = 0
while i <= 1759952:
    if i % 10000 == 0:
        id = id + 1
        print id
        cur.execute('INSERT INTO refactor_crawler.count_jieba(id,start,end) VALUES(%s,%s,%s);', [id, i, i + 10000])
    i = i + 1

conn.commit()
