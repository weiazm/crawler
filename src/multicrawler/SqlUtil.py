# -*-coding:utf-8-*-


class MysqlOperator(object):
    @classmethod
    def updateTitleAndClickNum(cls, conn, id, clickNum, title):
        cursor = conn.cursor()
        cursor.execute('update forum_links set title =%s,click_num =%s where id =%s', [title, clickNum, id])
        cursor.close()

    def __init__(self, connection):
        self.__conn = connection

    def selectCarIds(self):
        cursor = self.__conn.cursor()
        cursor.execute("select * from car_id_brand")
        values = cursor.fetchall()
        cursor.close()
        return values

    # FIXME
    def insertForumLinks(self, carIdAndlinks):
        cursor = self.__conn.cursor()

        try:
            for c in carIdAndlinks:
                cursor.execute(
                    'insert into forum_links (car_id,bbs_id,link,author_uid,release_time,reply_num,click_num,last_reply_time,last_reply_uid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    [c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8]])
        except Exception, e:
            # print e
            # logging.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' carIdAndLinks=' + str(c) + ' Error = ' + str(e) + u"插入数据库发生异常:" )
            self.__conn.rollback()
        else:
            print u"插入数据库行数：" + unicode(cursor.rowcount)
            self.__conn.commit()
        finally:
            cursor.close()

    def selectLinkById(self, id):
        cursor = self.__conn.cursor()
        cursor.execute('select * from forum_links where id = %s', [id])
        # return 'http://club.autohome.com.cn'+cursor.fetchall()[0]
        return cursor.fetchall()[0]

    def insertBBSContent(self, content):
        # c = Constant.BBSContent
        c = content
        cursor = self.__conn.cursor()
        cursor.execute(
            'insert into bbs_content(forum_link_id,bbs_id,uid,from_floor,to_floor,reply_time,content,num_of_links,num_of_words,num_of_pictures,num_of_faces,device) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            [c.forum_link_id, c.bbs_id, c.uid, c.from_floor, c.to_floor, c.reply_time, c.content, c.num_of_links,
             c.num_of_words, c.num_of_pictures, c.num_of_faces, c.device])
        cursor.close()
