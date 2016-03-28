# -*- coding: utf-8 -*-

import xlwt
import re
import httplib2
from pyquery import PyQuery

'''根据图片比对log, 整理信息
   litb_id litb_url litb_price
   1688_url 1688_img 1688_price
'''

def process():
    fw = open("1688_match.log")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    ws.write(0, 0, 'litb_id')
    ws.write(0, 1, 'litb_url')
    ws.write(0, 2, '1688_url')
    ws.write(0, 3, '1688_price')
    ws.write(0, 4, '1688_img')
    ws.write(0, 5, 'litb_price')
    count = 0
    while True:
        line = fw.readline()
        if not line:
            break
        result = re.findall('of (\d+) matched (\S+) of (\S+)', line)
        if not result:
            break
        count += 1
        print count
        ws.write(count, 0, result[0][0])
        litb_url = 'http://lightinthebox.com/_p' + result[0][0] + '.html'
        ws.write(count, 1, litb_url)
        ws.write(count, 3, get_price(result[0][2]))
        ws.write(count, 4, result[0][1])
        ws.write(count, 2, result[0][2])
        ws.write(count, 5, get_litb_price(litb_url))
    wb.save('test.xls')

def get_price(url):
    result = ''
    h = httplib2.Http()
    response, content = h.request(url)
    if response.status == 200:
        doc = PyQuery(content)
        result = doc('tr.price').text()
    return result

def get_litb_price(url):
    result = ''
    h = httplib2.Http()
    response, content = h.request(url)
    if response.status == 200:
        doc = PyQuery(content)
        result = doc('strong.sale-price ').text()
    return result
    

if __name__ == '__main__':
    process()