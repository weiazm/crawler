headerDict = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'cookieCityId=110100; sessionid=B7EB79CF-8638-2EDC-CE72-34A044C1E51B%7C%7C2016-04-06+10%3A50%3A45.156%7C%7Cwww.baidu.com; sessionuid=B7EB79CF-8638-2EDC-CE72-34A044C1E51B||2016-04-06+10%3A50%3A45.156||www.baidu.com; sessionfid=2399945834; AccurateDirectseque=404; wwwjbtab=1%2C0; sessionip=219.217.246.6; area=230199; historybbsName4=c-9901135%7C%E6%96%B0%E6%80%9D%E5%9F%9F%7C%2Cc-364%7C%E7%A6%8F%E5%85%8B%E6%96%AF%7C%2F2014%2F09%2F09%2F2b3181bb-10c3-48e8-a812-2b82da7ffcb4_s.jpg%2Cc-982%7C%E8%8B%B1%E6%9C%97%7C%2F2012%2F12%2F3%2F0facda97-631f-424c-8e3e-70e2f2a45a37_s.jpg%2Cc-526%7C%E5%8D%A1%E7%BD%97%E6%8B%89%7C%2F2014%2F10%2F16%2F5f68376d-c6a6-480a-804e-6ac07efee3b8_s.jpg%2Cc-442%7C%E9%80%9F%E8%85%BE%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg10%2FM10%2F1C%2FDC%2Fuserphotos%2F2015%2F12%2F23%2F16%2FwKgH0VZ6YDGAQLHcAAFqVYty-BQ691_s.jpg%2Cc-871%7C%E9%AB%98%E5%B0%94%E5%A4%AB%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg23%2FM03%2F3E%2FCA%2Fuserphotos%2F2016%2F02%2F04%2F19%2FwKgFV1azMeaAEInbAAHJkFVXPZU784_s.jpg%2Cc-519%7C%E6%98%8E%E9%94%90%7C%2F2012%2F12%2F3%2F60dd8e63-17d1-4b5e-b5a7-30dba14c0583_s.jpg%2Cc-614%7C%E6%9C%97%E9%80%B8%7C%2F2012%2F10%2F11%2Fd79c82d7-67de-4be4-b2f8-cffa87143e8e_s.jpg%2Cc-3751%7C%E5%A8%81%E6%9C%97%7Chttp%3A%2F%2Fimg.autohome.com.cn%2Falbum%2Fg17%2FM14%2F63%2F46%2Fuserphotos%2F2015%2F09%2F04%2F11%2FwKgH2FXpFyGAO10IAAMtKmsaqgk240_s.jpg%2Cc-3013%7CYeti%7C%2F2014%2F12%2F02%2F4830af1a-902a-4e9d-8467-81299a4baa9b_s.jpg; ASP.NET_SessionId=kb3nhrz4ojh3gg50zey33m11; pcpopclub=361BA91B77940E11291616054A1B628F4C347C8D1607936557E8FA654107F015E3958B4699DA42705FBCB67706A44E99D04DBE222C67B2E0111EF568856FA71978623B58B91DBC58241F41CB84175B1E7C6890607B33A90419139E4824282DF822B70609E0E54FA16CD10EA4292F5376A020856034B278249F2177C8EC19D26B0CB79BCB1C9F14E729BABFDB11374BDBEC6198BDE82F7738A1E8D817C05AF24D110728F2DF25BAFF45FCAF1F78277EA567B34D46083B55C6E4CD47B96C956830BB7B52DAD2672B9ABC44376E8E2C2084A888C5A8DB932D123E89B42B074494C9E85AB0C9B27071D44E97B46136BF0875D37C3E339722A1FFF2F2B0C1E4AFD934E4B270A95359792E486245E0578FAA29B75216115AF36E818EBCA8A4F667551880DDC0B45F34B2174807BD835AFFC8CA9396ECC2212AA883218C8CAB47BB2124D70CD741CED3DC2155180494; clubUserShow=26959260|2767|11|IWillFollow|0|0|0||2016-04-16 13:34:36|0; autouserid=26959260; __utma=1.163303314.1459911043.1460776791.1460783586.23; __utmb=1.0.10.1460783586; __utmc=1; __utmz=1.1460783586.23.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; sessionuserid=26959260; sessionlogin=3f0c5d0084da41d09d442d35be3830d4019b5d9c; sessionvid=864EDCA8-ACBD-96DC-F36B-936B69F6021F; ref=www.baidu.com%7C%7C0%7C8-1%7C2016-04-16+13%3A13%3A08.742%7C2016-04-06+10%3A50%3A45.156',
    'Host': 'club.autohome.com.cn',
    'Referer': 'http://www.autohome.com.cn/364/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
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
