headerDict = {
    'Accept': '*/*',
    'User-Agent': 'userAgentIE9',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Cookie': 'sessionfid=3504148999; cookieCityId=110100; sessionid=6EC40638-B5C7-D1D0-1FF3-E0BD9C414491%7C%7C2016-05-09+21%3A51%3A58.462%7C%7Cwww.baidu.com; sessionuid=6EC40638-B5C7-D1D0-1FF3-E0BD9C414491||2016-05-09+21%3A51%3A58.462||www.baidu.com; mylead_26959260=11; sessionfid=4121374679; pcpopclub=B4ECC05609BFE9353DA591014DE58A5847364610369332D456000614D58AE8709911EA1350120BCDF8BDE9246350CCA94A2B0F73364BA8BC313EE3ADB49B6C00E97C2F052BEFFA8AA918FF4DDF62990A02103D19990312E72DF959428E795CE1706388B94EBE0EE2FDC600CBCC68008FFDEC90DABC0A943F7902D2AA2A7018A30BB517096AD3B7A28C4033EE886F6B10AC24CAFFBCE427EC1223BAECB0D0110E34CD015F6F579DBB355FAA053C63E804C44C6EFE6EA14A852B63FEF3835B59218C8EF8A060FFF062EC1C6E70B543B5722D7E26FA2DD246FC17B2DA37EC57511845D2F3B6073C13E2DA694F8B77A15302C29A95D92B3E808A147D7FDD8783AAF78532E21F2D2307B2028BF2500EFFA11B46259F8222F30F440030608E1C980250BC0437A7F86B45C90E8C35089007AC3DDA8DE26B149B4A3173369D3EF1EE6146AF10E729; clubUserShow=27679841|0|230100|testUser3|0|0|0||2016-05-10 13:22:05|1; autouserid=27679841; mylead_27679841=11; historybbsName4=c-3013%7CYeti%7C%2F2014%2F12%2F02%2F4830af1a-902a-4e9d-8467-81299a4baa9b_s.jpg%2Cc-3074%7C%E5%93%88%E5%BC%97H7%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg6%2FM08%2F08%2F7C%2Fuserphotos%2F2015%2F12%2F10%2F14%2FwKgH3FZpF8uAdbCoAAE88v4wZAY344_s.jpg%2Cc-871%7C%E9%AB%98%E5%B0%94%E5%A4%AB%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg23%2FM03%2F3E%2FCA%2Fuserphotos%2F2016%2F02%2F04%2F19%2FwKgFV1azMeaAEInbAAHJkFVXPZU784_s.jpg; sessionip=219.217.246.8; sessionuserid=27679841; sessionlogin=1141d625c1be4249934754941303b39801a65c61; ASP.NET_SessionId=wkvebsgd1ujdmdejuad4wpxa; __utma=1.171959473.1462801915.1463542539.1463760127.22; __utmb=1.0.10.1463760127; __utmc=1; __utmz=1.1463451242.20.7.utmcsr=i.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/4412576/club/sendreply; ref=www.baidu.com%7C%7C0%7C8-1%7C2016-05-21+00%3A02%3A11.519%7C2016-05-09+21%3A51%3A58.462; sessionvid=BB02A84B-B176-474C-8555-0A2A15196C07; area=230199',
}

config2 = {'host': '172.17.23.70',
           'user': 'why',
           'password': '48152659-+',
           'port': 3306,
           'database': 'refactor_crawler',
           'charset': 'utf8'
           }
config = {'host': 'localhost',
          'user': 'root',
          'password': '48152659-+',
          'port': 3306,
          'database': 'refactor_crawler',
          'charset': 'utf8'
          }

timeout = 20

class BBSContent(object):
    def __init__(self):
        self.forum_link_id = ""
        self.bbs_id = ""
        self.uid = ""
        self.from_floor = ""
        self.to_floor = ""
        self.reply_time = ""
        self.content = ""
        self.num_of_links = ""
        self.num_of_words = ""
        self.num_of_pictures = ""
        self.num_of_faces = ""
        self.device = ""

    def printContent(self):
        print self.forum_link_id, self.bbs_id, self.uid, self.from_floor, self.to_floor, self.reply_time, self.content, self.num_of_links, self.num_of_words, self.num_of_pictures, self.num_of_faces, self.device

class User(object):
    def __init__(self):
        self.uid = ""
        self.sex = ""
        self.nickname = ""
        self.location = ""
        self.auth = ""
        self.auth_cars = ""
        self.points = ""
        self.level = ""
        self.follows = ""
        self.num_of_follows = ""
        self.fans = ""
        self.num_of_fans = ""
        self.create_time = ""
        self.num_of_main_bbs = ""
        self.num_of_elite_bbs = ""
        self.num_of_reply = ""
        self.num_of_reply_self = ""
        self.num_of_reply_others = ""
        self.first_post_time = ""
        self.last_post_time = ""
        self.avg_num_of_bbs = ""
        self.if_oil_consule = ""
        self.if_comment = ""
        self.if_cost = ""
        self.post_bbs_category_text = ""
        self.reply_bbs_category_text = ""

    def printUser(self):
        print 'uid:', self.uid
        print 'sex:', self.sex
        print 'nickname:', self.nickname
        print 'location:', self.location
        print 'auth:', self.auth
        print 'auth_cars:', self.auth_cars
        print 'points:', self.points
        print 'level:', self.level
        print 'follows:', self.follows
        print 'num_of_follows:', self.num_of_follows
        print 'fans:', self.fans
        print 'num_of_fans:', self.num_of_fans
        print 'create_time:', self.create_time
        print 'num_of_main_bbs:', self.num_of_main_bbs
        print 'num_of_elite_bbs:', self.num_of_elite_bbs
        print 'num_of_reply:', self.num_of_reply
        print 'num_of_reply_sele:', self.num_of_reply_self
        print 'num_of_reply_others:', self.num_of_reply_others
        print 'first_post_time:', self.first_post_time
        print 'last_post_time:', self.last_post_time
        print 'avg_num_of_bbs:', self.avg_num_of_bbs
        print 'if_oil_consule:', self.if_oil_consule
        print 'if_comment:', self.if_comment
        print 'if_cost:', self.if_cost
        print 'post_bbs_category_text:', self.post_bbs_category_text
        print 'reply_bbs_category_text:', self.reply_bbs_category_text