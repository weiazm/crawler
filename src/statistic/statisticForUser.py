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


def getStatistic(contents):
    num_of_reply_self = getReplySelf(contents)
    num_of_reply_others = getReplyOthers(contents)
    num_of_reply = num_of_reply_self + num_of_reply_others
    return num_of_reply, num_of_reply_self, num_of_reply_others


def getReplySelf(contents):
    result = 0
    bbs_id_list = []
    for content in contents:
        if content[4] == 0:
            bbs_id_list.append(content[2])
    bbs_id_list = set(bbs_id_list)
    for content in contents:
        if content[4] != 0:
            if content[2] in bbs_id_list:
                result += 1
    return result


def getReplyOthers(contents):
    result = 0
    bbs_id_list = []
    for content in contents:
        if content[4] == 0:
            bbs_id_list.append(content[2])
    bbs_id_list = set(bbs_id_list)
    for content in contents:
        if content[4] != 0:
            if content[2] not in bbs_id_list:
                result += 1
    return result


index = 1
while index <= 568584:
    try:
        cur = conn.cursor()
        cur.execute('SELECT uid FROM refactor_crawler.user where id = %s', [index, ])
        uid = cur.fetchall()[0][0]
        # print uid
        cur.execute('SELECT * FROM refactor_crawler.bbs_content where uid = %s order by reply_time', [uid, ])
        contents = cur.fetchall()
        result = getStatistic(contents)
        # print result
        cur.execute(
            "UPDATE `refactor_crawler`.`user`SET`num_of_reply` = %s,`num_of_reply_self` = %s,`num_of_reply_others` = %s WHERE  `uid` = %s",
            [result[0], result[1], result[2], uid])
        index += 1
        if index % 5000 == 0:
            conn.commit()
            print "Done!"
    except:
        index += 1;
        continue

conn.commit()
