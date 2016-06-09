#-------------------------------------------------------------------------------
# Name:
# Purpose:      calculate the ambiguity of the review
#               extract and store the POS Tags
#               store them into the database
#
# Author:      Xudong
#
# Created:     25/04/2015
# Copyright:   (c) Xudong 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def main():
#    svmtest()
    jieba_cut()
##    pynlpir_cut()
##    print sys.getfilesystemencoding(),sys.getdefaultencoding()
##    print "购买车型".decode("utf8").encode('gb2312')
##    print "凹凸有车".decode("utf8").encode('utf8').decode("utf8")
##    print "凹凸有车".decode("utf8")
##    print "凹凸有车"
##    print u"凹凸有车"
##    print "哈哈".decode("utf8")

def jieba_cut():
    import jieba.posseg as pseg
    import os
    cur_path=os.getcwd()
    fobj = open(cur_path+'\\carreview.txt', 'r')
    raw = fobj.read()
    words = pseg.cut(raw)
    i=0
    words_count=[0]*37
    for w in words:
##        print w.word,w.flag
        if (w.flag=='a'):
            words_count[0]+=1
        if (w.flag=='ad'):
            words_count[1]+=1
        if (w.flag=='an'):
            words_count[2]+=1
        if (w.flag=='b'):
            words_count[3]+=1
        if (w.flag=='c'):
            words_count[4]+=1
        if (w.flag=='d'):
            words_count[5]+=1
        if (w.flag=='e'):
            words_count[6]+=1
        if (w.flag=='f'):
            words_count[7]+=1
        if (w.flag=='g'):
            words_count[8]+=1
        if (w.flag=='h'):
            words_count[9]+=1
        if (w.flag=='i'):
            words_count[10]+=1
        if (w.flag=='j'):
            words_count[11]+=1
        if (w.flag=='k'):
            words_count[12]+=1
        if (w.flag=='l'):
            words_count[13]+=1
        if (w.flag=='m'):
            words_count[14]+=1
        if (w.flag=='n'):
            words_count[15]+=1
        if (w.flag=='nr'):
            words_count[16]+=1
        if (w.flag=='ns'):
            words_count[17]+=1
        if (w.flag=='nt'):
            words_count[18]+=1
        if (w.flag=='nz'):
            words_count[19]+=1
        if (w.flag=='o'):
            words_count[20]+=1
        if (w.flag=='p'):
            words_count[21]+=1
        if (w.flag=='q'):
            words_count[22]+=1
        if (w.flag=='r'):
            words_count[23]+=1
        if (w.flag=='s'):
            words_count[24]+=1
        if (w.flag=='t'):
            words_count[25]+=1
        if (w.flag=='u'):
            words_count[26]+=1
        if (w.flag=='v'):
            words_count[27]+=1
        if (w.flag=='vd'):
            words_count[28]+=1
        if (w.flag=='vn'):
            words_count[29]+=1
        if (w.flag=='w'):
            words_count[30]+=1
        if (w.flag=='x'):
            words_count[31]+=1
        if (w.flag=='y'):
            words_count[32]+=1
        if (w.flag=='z'):
            words_count[33]+=1
        #not belong to ICTPOS3.0
        if (w.flag=='uj'):
            words_count[34]+=1
        if (w.flag=='eng'):
            words_count[35]+=1
        words_count[36]+=1
##    print '-----',words_count


    #extract the characteristc terms
    import jieba.analyse
    topK=100
    tags = jieba.analyse.extract_tags(raw, topK=topK)
    character_terms = len(tags)
##    print(",".join(tags))

    #calculate the ambiguity of the review
    import math

    quantifer=words_count[14]
    noun=words_count[15]
    verb=words_count[27]
    allterms=words_count[36]
    ambiguity=((quantifer+1)*1.0/allterms)*(noun*1.0/(noun+verb))*math.log(1+character_terms)
##    print 'ambiguity=',quantifer,noun,verb,allterms,character_terms,math.log(1+character_terms),ambiguity
    print ambiguity
    pass


def svmtest():
    import sys

    sys.path.append('D:\libsvm-3.21\python')
    from svmutil import *

    y, x = svm_read_problem('D:\libsvm-3.21\heart_scale')
    m = svm_train(y[:200], x[:200], '-c 4')

    p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)
    print p_label
    print p_acc
    print p_val


def pynlpir_cut():
    import pynlpir

    pynlpir.open()
    s = u"我是工大计算机学院的老师,2000年留校,讲授软件体系结构和高级程序设计语言等课程"#.decode("utf8")
    import os
    cur_path=os.getcwd()
    #file should be stored in utf8 format
    fobj = open(cur_path+'\\newtext.txt', 'r')
    raw = fobj.read()
##    k=pynlpir.nlpir.FileProcess(cur_path+'\\carreview.txt','result.txt',True)
##    print k
##    print raw
    g=pynlpir.segment(raw)
##    print g[0][1]
    i=0
    for x in g:
        print x[0].encode('gb2312'),x[1]
        i=i+1
    print '-----',i
##        if x[1]==u'time word':
##            print x[0].encode('gb2312')

    pynlpir.close()



if __name__ == '__main__':
    main()
