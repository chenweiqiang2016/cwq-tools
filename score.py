# -*- coding: utf-8 -*-

#2015/11/29 作一次全面的修改 可以作为评分程序使用 选品时cm_pick_time > '2015-11-29'
#cost time: 2h

import sys
import os
import MySQLdb
import datetime
import ConfigParser
import re
import codecs

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
                                    db=get_config(machine, 'db'),
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.autocommit(False)
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

stats = {}
            
def get_file_name():
    machine = get_config('machines', 'dest.machine')
    db = Db(machine)
    merchants = getFormatMerchantList()
    arg_list = ','.join(['%s'] * len(merchants))
    sql = """SELECT
                p.merchant_id, count(*)
             FROM
                products p
             LEFT JOIN
                product_scores ps 
             ON 
                p.id = ps.product_id 
             WHERE
                p.merchant_id in (%s)
             AND
                cm_pick_time > '2015-11-29'
             AND 
                p.cm_picked = 1 
             AND
                ps.product_id is null
             GROUP BY
                p.merchant_id
          """
    db.cursor.execute(sql %arg_list, merchants)
    merchantList = db.cursor.fetchall()
    mainPart = ""
    for item in merchantList:
        mainPart += item[0].strip()
        stats[item[0].strip()] = int(item[1])
    prefix = str(datetime.date.today())
    suffix = '.csv'
    db.close()
    #没有要处理的商品, 直接退出
    if not mainPart:
        print 'No merchants, no products, to be added to product_scores, exit!'
        sys.exit(1)
    return prefix + '_' + mainPart + suffix
    
            
def getFormatMerchantList():
    result = []
    cf2 = ConfigParser.ConfigParser()
    cf2.read("./config/score_merchants.txt")
    kvs = cf2.items("merchants")
    for kv in kvs:
        result.append(kv[1])
    return result

def export_from_products():
    filename = get_file_name()
    #将文件名记录下来
    global saveFile
    saveFile = filename  #type: unicode
    merchants = getFormatMerchantList()
    args_list = ','.join(['%s'] * len(merchants))
    machine = get_config('machines', 'src.machine')
    db = Db(machine)
    sql = """SELECT 
                p.id, p.name, p.merchant_id, p.category_id, 
                p.url, p.img_url, p.price, p.reviews, p.category_index,
                p.sellstart_date, p.ct_status 
             FROM
                products p
             LEFT JOIN
                product_scores ps 
             ON 
                p.id = ps.product_id 
             WHERE
                p.merchant_id in (%s)
             AND
                cm_pick_time > '2015-11-29'
             AND 
                p.cm_picked = 1 
             AND
                ps.product_id is null"""
    db.cursor.execute(sql %args_list, merchants)
    results = db.cursor.fetchall()
    #filename = str(datetime.date.today()) + '_SD001.csv' #TypeError: unsupported operand type(s) for +: 'datetime.date' and 'str'
    fw = open(filename, 'w')
    fw.write(codecs.BOM_UTF8)
    headers = ['id', 'name', 'merchant_id', 'category_id', 'url', 'img_url', 'price', 'reviews', 'category_index', \
               'sellstart_date', 'ct_status', 'category_path']
    fw.write('\t'.join(headers) + '\n')
    for result in results: #每个result为一个商品信息
        categoye_path = compute_category_path(db, result[3])
        print categoye_path
        result_list = []
        for item in result:
            result_list.append(str(item))
        result_list.append(categoye_path)
        line = '\t'.join(result_list) + '\n'
        fw.write(line)
    fw.close()
    db.close()

def compute_category_path(db, category_id):
    sql = '''select 
             name, parent_id, level1_category_id, level from categories
             where id=%s
    '''
    sql1 = '''select name from categories where 
              id=%s
           '''
    db.cursor.execute(sql, category_id)
    result = db.cursor.fetchone()
    print '[%s](%s){level=%s, parent_id=%s, level1_category_id=%s}' %(result[0], category_id, result[3], result[1], result[2]), 
    
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
    sql = '''replace into product_scores (product_id, merchant_id, category_id, category_path, price, reviews, category_index,\
             product_name, product_url, img_url, ct_status, score, calc_date, score_type) values
             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          '''
    machine = get_config('machines', 'dest.machine')
    db = Db(machine) #TypeError: not all arguments converted during string formatting
    fw = open(filename, 'r')
    first_line = fw.readline().strip()
    if first_line.startswith(codecs.BOM_UTF8):
        first_line = first_line[len(codecs.BOM_UTF8):]
    headers = first_line.split('\t')
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
            if key=='price': #下面对price进行了float操作
                print "Origin price:", datas[i],
                if not re.findall("[\d\.]+", datas[i]):
                    datas[i] = 0
                else:
                    datas[i] = re.findall("[\d\.]+", datas[i])[0]
                print "Format price:", datas[i]
            datas_dic[key] = datas[i]
        if not datas_dic['category_index'] or datas_dic['category_index'].upper()=='NONE': #读出来的是None
            datas_dic['category_index'] = 0
        args = (int(datas_dic['id']), datas_dic['merchant_id'], int(datas_dic['category_id']), datas_dic['category_path'],\
                float(datas_dic['price']), int(datas_dic['reviews']), int(datas_dic['category_index']),\
                datas_dic['name'], datas_dic['url'], datas_dic['img_url'], 0, 0, str(datetime.date.today()), 'manual')
        print args
        db.cursor.execute(sql, args)
        counter += 1
        if counter % 500 ==0:
            db.conn.commit()
    db.conn.commit()

def mv(filename):
    import shutil
    saveDir = get_config('all', 'save.dir')
    srcPath = os.path.join(os.getcwd(), filename)
    print srcPath
    destPath = os.path.join(saveDir, filename)
    print destPath
    shutil.move(filename, destPath)

def print_stat():
    print "Statistics:"
    for k in stats.iterkeys():
        print " "*4 + k + ":", stats.get(k) 
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python %s (export|load|score) [filename]' %(os.path.basename(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] == 'export':
        export_from_products()
    elif sys.argv[1] == 'load':
        filename = sys.argv[2]
        load_into_product_scores(filename)
    elif sys.argv[1] == 'score':
        export_from_products()
        load_into_product_scores(saveFile)
        mv(saveFile)
        print_stat()
    else:
        print 'please input correct args...'

    print 'Successfully Done.'