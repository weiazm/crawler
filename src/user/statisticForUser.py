# -*-coding:utf-8-*-
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
