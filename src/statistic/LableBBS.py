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
cur.execute('SELECT bbs_id from temp')
i = 1
for line in cur.fetchall():
    bbs_id = line[0];
    print i
    cur.execute('UPDATE refactor_crawler.main_content SET auto_label = 0 WHERE bbs_id = %s', [bbs_id, ])
    i += 1;

# cur.execute('SELECT uid FROM refactor_crawler.user where id = %s', [index, ])
conn.commit()
