# -*- coding: utf-8 -*-

#根据位置表中的商品位置来补充products表中的category_index字段

import MySQLdb

conn = MySQLdb.connect(host="10.5.17.188",
                       user="litb_merchadmin",
                       passwd="0643CABB-971E-47F1-9B09-6FAE2B1B5D2E",
                       db="aims")

cursor = conn.cursor()

sql = """select product_id, page, position from products_sammydress where product_id in 
         (select id from products where merchant_id='MN001' and latest_capture_date='2015-10-21')
      """
      
sql2 = """ update products set category_index =%s where id = %s
       """

cursor.execute(sql)

results = cursor.fetchall()

for t in results:
    product_id =int(t[0])
    category_idx = (int(t[1])-1) * 40 + int(t[2])
    #print product_id, category_idx
    #程序BUG 语义错误
    #category_idx, product_id位置写反 需要更改数据库中id小于50的商品的category_index
    cursor.execute(sql2, (category_idx, product_id))

cursor.close()
conn.close()