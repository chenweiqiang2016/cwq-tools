# -*- coding: utf-8 -*-

import sys
import xlrd
import codecs

def convert(xlsFilename):
    filename = xlsFilename.replace('xlsx', 'csv').replace('xls', 'csv') #csv文件名
    
    wb = xlrd.open_workbook(xlsFilename)
    ws = wb.sheets()[0] #获取第一个表单
    rows = ws.nrows

    fw = open(filename, 'w')
    fw.write(codecs.BOM_UTF8)
    for row in range(rows):
        line = '\t'.join(ws.row_values(row)) + '\n'
        # 'ascii' codec can't encode character u'\u2264' in position 38: ordinal not in range(128)
        # line是unicode编码的, write默认进行了str操作, 需要转换为UTF-8编码
        # http://blog.csdn.net/panyanyany/article/details/17251225
        fw.write(line.encode('UTF-8'))
    fw.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s xlsFilename' %sys.argv[0]
        sys.exit(1)
    xlsFileName = sys.argv[1]
    convert(xlsFileName)