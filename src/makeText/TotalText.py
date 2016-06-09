# -*-coding:utf-8-*-
import codecs

import mysql.connector

import jieba

config = {'host': '172.17.26.167',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }

id = 0
end = 1759952
conn = conn = mysql.connector.connect(**config)
cur = conn.cursor()
f = codecs.open("content.txt", "w", "utf-8","ignore")

while id <= end:
    if id % 10000 ==0:
        cur.execute('select * from main_content where id >= %s and id < %s and label_emotion is NULL ', [id,id+10000])
        for main_content in cur.fetchall():
            content = main_content[8]
            uid = main_content[4]
            bbs_id = main_content[3]
            label_emotion = main_content[-1]
            if label_emotion == None:
                label_emotion = -1
            #print content
            seg_list = jieba.cut(content) # 默认是精确模式
            cut_content = " ".join(seg_list).replace(u"。",u"。<sssss>").replace(u"？",u"？<sssss>").replace(u"！",u"！<sssss>")
            if len(cut_content.split(" "))>2:
                result = str(uid)+"\t\t"+str(bbs_id)+"\t\t"+str(label_emotion)+"\t\t"+cut_content
                #print result
                f.write(result)
                f.write('\n')
        print id
    id +=1


cur.close()
conn.close
f.close()