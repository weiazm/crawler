#-*-coding:utf-8-*-
print 'this is a test','a','b'
#name=raw_input('please input something:')
#print 'you just input:',name
a =100
if a<100:
    print 'a<100'
elif a==100:
    print 'a=100'
else:
    print 'a>=100'
print r'"this donot need\"'
print '''两
行'''
lis=['fucking','asshole','shabi']
print lis
lis.insert(1 , 'd55')
print lis
for li in lis:
    print li
tupl=('fucking','asshole','shabi')
print tupl
dic={'s':1,'a':2,'f':3}
print dic['s']
s=set([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,12])
print s
s_2=set([1,2,5])
print s|s_2
print abs(-2.5),cmp(1, 5),int(55.8),unicode(100),float(1),bool(0)
a=abs
print a(-5)

def fuck(x):
    if not isinstance(x , (int,float)):
        raise TypeError("他妈的类型不对")
    if x>0:
        return x
    elif x==0:
        return x
    else:
        return -x
print fuck(-8.8)
#print fuck("2")

def no():
    pass
print no()

def power(x,n=2):
    if not isinstance(x, (int,float)):
        raise TypeError("他妈的类型不对")
    res=1
    while n>0:
        res=res*x
        n-=1
    return res

print power(2),power(2, 3),power(55,13131)

def func(a,b,*c,**d):
    print(a,b,c,d)
func("x","a","a","d","sdfs",s="5555ls",f="48565")

def fact(a):
    if a==1:
        return 1
    else:
        return a*fact(a-1)
print fact(10)
#尾递归优化 然并卵
def fac_t(n):
    return wdg_fact(n,1)
def wdg_fact(n,temp):
    if n==1:
        return temp
    else:
        return wdg_fact(n-1, n*temp)
print fac_t(10)
#切片
L=range(100)
print L[0:10:3]
#迭代
dick={'a':"aaa",'b':'bbb','d':"ddd"}
print dick
for key in dick:
    print key
for key in dick.itervalues():
    print key
for key,value in dick.iteritems():
    print key+':'+value
#列表生成器
print [x*x for x in range(1,11)]
#全排列呦
print [m+n for m in "abcde" for n in "1234"]
#列出文件名
import os
print [d for d in os.listdir('/home/why/workspace/crawler')]
g=(x*x for x in range(20))
print g
print g.next()
print g.next()
for n in g:
    print n

































































































