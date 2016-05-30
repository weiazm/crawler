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

index = 45000
while index <= 649208:
    try:
        cur = conn.cursor()
        cur.execute('SELECT uid FROM refactor_crawler.user where id = %s', [index, ])
        uid = cur.fetchall()[0][0]
        # print uid
        cur.execute(
            'SELECT * FROM refactor_crawler.bbs_content where uid = %s and from_floor != 0 order by reply_time ',
            [uid, ])
        contents = cur.fetchall()
        print index
        if len(contents) > 0:
            first_reply_time = contents[0][6]
            last_reply_time = contents[-1][6]
            # print first_post_time,last_post_time
            cur.execute(
                "UPDATE `refactor_crawler`.`user`SET`first_reply_time` = %s,`last_reply_time` = %s WHERE  `uid` = %s",
                [first_reply_time, last_reply_time, uid])
            # conn.commit()
        index += 1
        if index % 5000 == 0:
            conn.commit()
    except:
        index += 1
        continue
conn.commit()
