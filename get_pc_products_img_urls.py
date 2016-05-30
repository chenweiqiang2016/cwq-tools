# -*- coding: utf-8 -*-

import MySQLdb
import xlrd
# import xlwt

class Db:
    def __init__(self):
        self.connect = MySQLdb.connect(host="172.16.0.149",
                                       user="v3tpm",
                                       passwd="pm7_l1e98",
                                       db="products_center_v1")
        self.cursor = self.connect.cursor()
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
            

def main():
    rb = xlrd.open_workbook("C:/users/chenweiqiang/desktop/productslist.xlsx")
    rs = rb.sheets()[0]
    rs_nrows, rs_ncols = rs.nrows, rs.ncols
#     rs_headers = rs.
    db = Db()
    db.cursor.execute("select * from products_images limit 1")
    print db.cursor.fetchone()


if __name__ == '__main__':
    main()