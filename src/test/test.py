###-*-encoding:utf-8-*-
'''
Created on 2016年3月25日

@author: why
'''
import MySQLdb
from pyodbc import Row


conn = MySQLdb.connect("localhost", "root", "1234", "crawler")
cursor = conn.cursor()
cursor.execute("insert into test value(3,\"safaf\",1)")
conn.commit()
conn.close()

conn = MySQLdb.connect("localhost", "root", "1234", "crawler")
cursor = conn.cursor()
cursor.execute("select * from test")
for row in cursor.fetchall():
    print row
print cursor.fetchall
conn.commit()
conn.close()

conn = MySQLdb.connect("localhost", "root", "1234", "crawler")
cursor = conn.cursor()
n=cursor.execute("delete from test where id=%s","3")
print n
conn.commit()
conn.close()
