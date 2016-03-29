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
func("x","a","a","d",s="5555")


































































