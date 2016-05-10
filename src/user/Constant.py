headerDict = {
    'Accept': '*/*',
    'User-Agent': 'userAgentIE9',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Cookie':'sessionfid=4121374679; cookieCityId=110100; sessionid=6EC40638-B5C7-D1D0-1FF3-E0BD9C414491%7C%7C2016-05-09+21%3A51%3A58.462%7C%7Cwww.baidu.com; sessionuid=6EC40638-B5C7-D1D0-1FF3-E0BD9C414491||2016-05-09+21%3A51%3A58.462||www.baidu.com; AccurateDirectseque=404; historybbsName4=c-3013%7CYeti%7C%2F2014%2F12%2F02%2F4830af1a-902a-4e9d-8467-81299a4baa9b_s.jpg; pcpopclub=FED2E26D21C3752F53F08A78BA78D8AD31EF533028DE92F6D4164E3EB69BCBE063CDBEA283F9CA0F81EAE397A35EDEC0B21FD52F17DF90C1926C3DBC564EE81A436D824375F17419270208C69A0566A6F8B7924E883A45E941052F55120855A373FD3BE05844D6A0B3604667DC9F9D7AC4D2F9FF08483197767FEEA3C29F2B3EB6BDAEE142E34362EB66EFD5C16C5B7B6E3A80C77C3A889E1D4AA3ECB5F2C0D712D40F7ECA3064AE32591970E71001EC50F81FE2A5324421B96FC28280848E10C21CE5C47487D8F0EF04A52CB2D85CE7B3B6422622965F957D1D591B458E2B896FBC645FD76A086614125D27A4BC7341237FAE939DBB37619C7996B886460EDF8FC632DC79A86AB23FF62498408D00EAA82B45BBE895483A4D7CCD0C8B0736429CC540C0ED1E6839081478408E23EF287CF2235DB6161BDCC8F81FA90E9E859E06528005E1499162DA5F722D; clubUserShow=26959260|2767|11|IWillFollow|0|0|0||2016-05-09 21:54:17|0; autouserid=26959260; ASP.NET_SessionId=5kfvjaokkozdkigvdkbm4j2m; sessionuserid=26959260; sessionlogin=7f598fd65b364308a183a5b22f155f57019b5d9c; __utma=1.171959473.1462801915.1462808954.1462844273.3; __utmb=1.0.10.1462844273; __utmc=1; __utmz=1.1462844273.3.3.utmcsr=i.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/4412576/club/sendreply; sessionip=219.217.246.8; area=230199; sessionvid=FED7A807-96CB-ADBB-23B9-77CE543BAD24; ref=www.baidu.com%7C%7C0%7C8-1%7C2016-05-09+21%3A52%3A16.790%7C2016-05-09+21%3A51%3A58.462'
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