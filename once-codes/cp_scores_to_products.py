# -*- coding: utf-8 -*-
# 解决load程序留下的bug

import MySQLdb
import re

sql1 = """select id from products where merchant_id is null
      """
      
sql2 = """select merchant_id, product_url, product_name
          from product_scores
          where product_id = %s
      """

sql3 = """update products set merchant_id=%s, url=%s, name=%s, sku_id=%s
          where id = %s
      """

class Db:
    def __init__(self):
        self.conn = MySQLdb.connect(host="10.5.17.188",
                                    user="litb_merchadmin",
                                    passwd="0643CABB-971E-47F1-9B09-6FAE2B1B5D2E",
                                    db="aims")
        self.cursor = self.conn.cursor()
        self.conn.autocommit(True)
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

def run():
    db = Db()
    db.cursor.execute(sql1)
    up_ids = []
    ids = db.cursor.fetchall()
    print 'total (merchant_is null) count: ' + str(len(ids))
    for id_tuple in ids:
        id = id_tuple[0]
        db.cursor.execute(sql2, id)
        result = db.cursor.fetchone()
        if result:
            merchant_id = result[0]
            product_url = result[1]
            product_name = result[2]
            sku_id = get_sku_id(merchant_id, product_url)
            if sku_id:
#                 print (merchant_id, product_url, product_name,sku_id)
                db.cursor.execute(sql3, (merchant_id, product_url, product_name, sku_id, id))
                up_ids.append(id)
            else:
                print merchant_id
    print 'total to be fixed count: ' + str(len(up_ids))
    print up_ids
    db.close()

def get_sku_id(merchant_id, product_url):
    if merchant_id=='MN001':
        return re.findall("-([\d]+)$", product_url)[0]  
    elif merchant_id=='MN010':
        return re.findall("-p-([\d]+)\.html", product_url)[0]
    elif merchant_id=='MN004':
        return re.findall("_p([\d]+)\.html", product_url)[0]  

if __name__ == '__main__':
    run()
        