# -*- coding: utf-8 -*-

import xlwt
import sys
import codecs
import os

def convert(filename):
    fr = open(filename, 'r')
    first_line = fr.readline().strip()
    if first_line.startswith(codecs.BOM_UTF8):
        first_line = first_line[len(codecs.BOM_UTF8):]
    headers = first_line.split('\t')
    
    wb = xlwt.Workbook('utf-8')
    ws = wb.add_sheet('sheet1')
    for col in range(len(headers)):
        ws.write(0, col, headers[col])
    
    row = 1
    while True:
        line = fr.readline().replace('\n', '').strip()
        if not line: #如果存在空行 将会退出程序
            break
        datas = line.split('\t')
        for col in range(len(datas)):
            ws.write(row, col, datas[col])
        row += 1
    
    xlsName = os.path.splitext(os.path.split(filename)[1])[0] + '.xls'
    wb.save('./output/' + xlsName) #默认生成的excel在output文件夹下面

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python %s filename' %sys.argv[0]
        sys.exit(1)
    filename = sys.argv[1]
    convert(filename)