# -*- coding: utf-8 -*-
# 测试: #(1205, 'Lock wait timeout exceeded; try restarting transaction')
    #_mysql_exceptions.OperationalError: (2008, 'MySQL client ran out of memory')
    
#1. 在mysql中执行select @@autocommit查看autocommit的状态值
#   为1的话是默认值, 可以正常运转
#   为0的话不管程序是否commit都将引发(1205, 'Lock wait timeout exceeded; try restarting transaction')
#   使用set global autocommit=1 修改

#2. 使用show [full] processlist查看mysql运行的进程, 慢进程直接可以看到
#   使用SELECT * FROM information_schema.INNODB_TRX\G;查看所有锁进程
#   如果第二条命令的进程id对应在第一条中是sleep状态 则表示语句卡壳了 (没有commit或者roollback), 需要手动kill

import MySQLdb

conn = MySQLdb.connect(host="localhost",
                       user="root",
                       passwd="",
                       db="aims")
cursor = conn.cursor()

conn.autocommit(False)

cursor.execute("update products set reviews=1234 where id=88806389")

conn.commit()

cursor.execute("select * from products limit 100")

print 'OVER'

