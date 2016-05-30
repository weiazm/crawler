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

index = 20000
while index <= 1759952:
    try:
        cur = conn.cursor()
        cur.execute('SELECT bbs_id FROM refactor_crawler.main_content where id = %s', [index, ])
        bbs_id = cur.fetchall()[0][0]
        # print bbs_id
        cur.execute(
            'SELECT * FROM refactor_crawler.bbs_content where bbs_id = %s and from_floor != 0 order by reply_time ',
            [bbs_id, ])
        contents = cur.fetchall()
        print index
        if len(contents) > 0:
            first_reply_time = contents[0][6]
            last_reply_time = contents[-1][6]
            num_of_reply = len(contents)
            # print first_post_time,last_post_time
            cur.execute(
                "UPDATE `refactor_crawler`.`main_content`SET`first_reply_time` = %s,`last_reply_time` = %s , `num_of_reply` = %s WHERE  `bbs_id` = %s",
                [first_reply_time, last_reply_time, num_of_reply, bbs_id])
            # conn.commit()
        index += 1
        if index % 5000 == 0:
            conn.commit()
    except:
        index += 1
        continue
conn.commit()
