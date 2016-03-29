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
list=['fucking','asshole','shabi']
print list
list.insert(1 , 'd55')
print list
for li in list:
    print li
tuple=('fucking','asshole','shabi')
print tuple
dict={'s':1,'a':2,'f':3}
print dict['s']
s=set([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,12])
print s
s_2=set([1,2,5])
print s|s_2
print abs(-2.5),cmp(1, 5),int(55.8),unicode(100),float(1),bool(0)
a=abs
print a(-5)

def fuck(x):
    if x>0:
        return x
    elif x==0:
        return x
    else:
        return -x
print fuck(-8.8)

def no():
    pass
print no()
        


































































