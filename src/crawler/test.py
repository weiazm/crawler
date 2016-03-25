###-*-encoding:utf-8-*-
'''
Created on 2016年3月25日

@author: why
'''
import MySQLdb
db = MySQLdb.connect("localhost","root","1234","crawler" )
cursor = db.cursor()
cursor.execute("insert into test value(3,\"safaf\",1)")
db.commit()
db.close()
print "fuckyou"