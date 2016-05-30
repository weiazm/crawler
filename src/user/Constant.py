headerDict = {
    'Accept': '*/*',
    'User-Agent': 'userAgentIE9',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Cookie': 'cookieCityId=110100; sessionid=ECD798C6-6389-97EB-FB47-AD1374FD60D7%7C%7C2016-05-21+00%3A50%3A12.182%7C%7Cwww.baidu.com; sessionuid=ECD798C6-6389-97EB-FB47-AD1374FD60D7||2016-05-21+00%3A50%3A12.182||www.baidu.com; mylead_26959260=11; historybbsName4=c-3074%7C%E5%93%88%E5%BC%97H7%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg6%2FM08%2F08%2F7C%2Fuserphotos%2F2015%2F12%2F10%2F14%2FwKgH3FZpF8uAdbCoAAE88v4wZAY344_s.jpg; sessionip=219.217.246.8; pcpopclub=99F856C44F5CE1420CD30BBC6F72B41671371D67E93E26D38BB5BEE5A657C34EAB78EC022D9B9AA7BBF1D5D0091D927C1C75617B0026ECDDE4EEE62DD448035E1B34BC42C378A57AB8C8B09C9A30FA7E8FB8D8BC0DBCF1E85D83F0E60064C8C9F0B21E320A26F9A11AF301E82BAFEAB0A8F7875F305109CE2AA9606D9407913FE55FDBE49044B1415A06FF1B8FF90D708D1557FFE7DA3D3905A3006DF1478C6EF93C157BC723C6C56A4FB6D46AC19330EC485550574391B40169A7CE58F803F70A6B3821685DA7D0EDEFCA4AC5F67C96870ACCC6A34DAD84F1C766D85F5C9E1CEE1862B415D69099BB395375AF511A9710B11491D7BBAB1CA51BAD414F861EB171414B0E2C731E5D7A0D9B8E60F06180CE72F74E70C70914477BC0622A1118D6DB712C3320973452843030E0AC950510E2FB001F5D835F3367002E8B2B49218F51BA26E831BE1B3B50F60E67; clubUserShow=26959260|2767|11|IWillFollow|0|0|0||2016-05-21 12:23:10|0; autouserid=26959260; ASP.NET_SessionId=qc3hzlmcd4mcbqa2bv2jp0x2; sessionuserid=26959260; sessionlogin=981a2418aacc4b6e876617ee139cba9e019b5d9c; __utma=1.1061922101.1463763020.1463905254.1464264863.4; __utmb=1.0.10.1464264863; __utmc=1; __utmz=1.1463905254.3.3.utmcsr=i.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/4412576/club/sendreply; ref=www.baidu.com%7C%7C0%7C8-1%7C2016-05-26+20%3A17%3A50.660%7C2016-05-21+00%3A50%3A12.182; sessionvid=3982B38D-097E-44DE-ACDF-49C48C20F5DB; area=230199',
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