# coding=utf-8
import mysql.connector
import os
import time


def compareList(indexsBefore, indexsAfter):
    beforeList = []
    for index in indexsBefore:
        beforeList.append(index[1])
    afterList = []
    for index in indexsAfter:
        afterList.append(index[1])

    x = 0
    result = []
    for index in afterList:
        # print str(index)[-4:]
        if str(index)[-4:] == '9999':
            pass
        elif index == 1766626:
            pass
        elif index == beforeList[x]:
            result.append(x + 1)
        x += 1
    if len(result) > 0:
        return False, result
    else:
        return True, result


def restart(crawlerId):
    bashLine = "bash /home/why/desktop/restart.sh " + str(crawlerId)
    os.system(bashLine)


config = {'host': 'localhost',
          'user': 'why',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }

conn = mysql.connector.connect(**config)
cur = conn.cursor()
cur.execute('SELECT * FROM count ')
indexsBefore = cur.fetchall()
cur.close()
conn.close()
count = 1

while 1:
    time.sleep(500)  # 查询时间间隔
    print '第', count, '次查询'
    conn = mysql.connector.connect(**config)
    cur2 = conn.cursor()
    cur2.execute('SELECT * FROM count ')
    indexsAfter = cur2.fetchall()
    cur2.close()
    conn.close()

    result = compareList(indexsBefore, indexsAfter)
    if result[0] == False:
        # 调用shell播放mp3
        os.system(u"play p.mp3")
        print ''  # 'before:', indexsBefore
        print '错误id: ', result[1]
        # for failId in result[1]:
        #	restart(failId)
        print ''  # 'after:', indexsAfter
    indexsBefore = indexsAfter
    count += 1
