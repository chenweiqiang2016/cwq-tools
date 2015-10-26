# -*- coding: utf-8 -*-

#cost time: 2h

import sys
import os
import MySQLdb
import datetime
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("./config/all_dbs.cfg")

def get_config(section, option):
    result = ''
    try:
        result = cf.get(section, option)
    except:
        pass
    return result

class Db:
    def __init__(self, machine):
        self.conn = MySQLdb.connect(host=get_config(machine, 'host'),
                                    user=get_config(machine, 'user'),
                                    passwd=get_config(machine, 'passwd'),
                                    db=get_config(machine, 'db')
                                    )
        self.cursor = self.conn.cursor()
        self.conn.autocommit(False)
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

def export_from_products():
    db = Db('master')
    sql = '''select id, name, merchant_id, category_id, url, img_url, 
             price, reviews, category_index, sellstart_date, ct_status
             from
             products 
             where
             ct_status=11 and merchant_id = 'SD001'
    '''
    db.cursor.execute(sql)
    results = db.cursor.fetchall()
    filename = str(datetime.date.today()) + '_SD001.csv' #TypeError: unsupported operand type(s) for +: 'datetime.date' and 'str'
    fw = open(filename, 'w')
    headers = ['id', 'name', 'merchant_id', 'category_id', 'url', 'img_url', 'price', 'reviews', 'category_index', \
               'sellstart_date', 'ct_status', 'category_path']
    fw.write('\t'.join(headers) + '\n')
    for result in results: #每个result为一个商品信息
        categoye_path = compute_category_path(db, result[3], 'SD001') #默认为sammydress
        print categoye_path
        result_list = []
        for item in result:
            result_list.append(str(item))
        result_list.append(categoye_path)
        line = '\t'.join(result_list) + '\n'
        fw.write(line)
    fw.close()
    db.close()

def compute_category_path(db, category_id, merchant_id):
    sql = '''select 
             name, parent_id, level1_category_id, level from categories
             where id=%s
    '''
    sql1 = '''select name from categories where 
              id=%s
           '''
    db.cursor.execute(sql, category_id)
    result = db.cursor.fetchone()
    print category_id, result[3], result[1], result[2]
    
    if int(result[3]) == 1:
        return result[0]
    elif int(result[3]) == 2:
        db.cursor.execute(sql1, result[1])
        level1cateName = db.cursor.fetchone()[0]
        return level1cateName + ' > ' + result[0]
    elif int(result[3]) == 3:
        db.cursor.execute(sql1, result[1])
        level2cateName = db.cursor.fetchone()[0]
        db.cursor.execute(sql1, result[2])
        level1cateName = db.cursor.fetchone()[0]
        return level1cateName + ' > ' + level2cateName + ' > ' + result[0]
    else:
        print 'category level <1 or >3...'
        print result
        sys.exit(1)
    

def load_into_product_scores(filename):
    sql = '''insert into product_scores (product_id, merchant_id, category_id, category_path, price, reviews, category_idx,\
             product_name, product_url, img_url, ct_status, score, calc_date, score_type) values
             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          '''
    db = Db('52') #TypeError: not all arguments converted during string formatting
    fw = open(filename, 'r')
    headers = fw.readline().strip().split('\t')
    counter=0
    while True:
        line = fw.readline().strip().replace('\n', '')
        if not line:
            break
        datas = line.split('\t')
        if len(datas) != len(headers):
            print 'wrong line: ' + line
        datas_dic = {}
        for i, key in enumerate(headers):
            datas_dic[key] = datas[i]
        
        args = (int(datas_dic['id']), datas_dic['merchant_id'], int(datas_dic['category_id']), datas_dic['category_path'],\
                float(datas_dic['price']), int(datas_dic['reviews']), int(datas_dic['category_index']),\
                datas_dic['name'], datas_dic['url'], datas_dic['img_url'], 0, 0, str(datetime.date.today()), 'manual')
        print args
        db.cursor.execute(sql, args)
        counter += 1
        if counter % 500 ==0:
            db.conn.commit()
    db.conn.commit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python %s (export|load) [filename]' %(os.path.basename(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] == 'export':
        export_from_products()
    elif sys.argv[1] == 'load':
        filename = sys.argv[2]
        load_into_product_scores(filename)
    else:
        print 'please input correct args...'