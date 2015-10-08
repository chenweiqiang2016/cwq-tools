# -*- encoding: utf-8 -*-

import xlrd
import xlwt
import os
import httplib2
import re
from pyquery import PyQuery
from utils import save_images

def run(inputFile, outFile, dest_dir='.', mode="copy"):
    outfile_path = os.path.join(dest_dir, outFile)
    rb = xlrd.open_workbook(inputFile)
    rs = rb.sheets()[0]
    nrows = rs.nrows
    ncols = rs.ncols 
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet('sheet1')
    for col in range(ncols):
        value = rs.cell(0, col).value
        ws.write(0, col, value)
    if mode=='copy':
        for row in range(1, nrows):
            for col in range(0, ncols):
                ws.write(row, col, rs.cell(row, col).value)
    elif mode=='add':
        add(rs, ws, nrows, ncols)
            
    wb.save(outfile_path)

def add(rs, ws, nrows, ncols):
    site ='wayfair' #以后将变为接口参数
    if site=='wayfair':
        headers = rs.row_values(0)
        url_idx = headers.index('product_url')
        price_idx = headers.index('price')
        img_urls_idx = headers.index('img_urls')
        sku_id_idx = headers.index('sku_id')
        for row in range(1, nrows):
            if str(rs.cell(row, price_idx).value).strip() == '' or float(extractNum(str(rs.cell(row, price_idx).value).strip())) == -1:
                info_tuple = wayfair_crawl(rs.cell(row, url_idx).value)
                if info_tuple[0] and info_tuple[1]:
                    ws.write(row, price_idx, info_tuple[0])
                    ws.write(row, img_urls_idx, info_tuple[1])
                    save_images('./output', info_tuple[1].split(','), rs.cell(row, sku_id_idx).value.strip())
                    print row
                for col in range(0, ncols):
                    if col not in [price_idx, img_urls_idx]:
                        ws.write(row, col, rs.cell(row, col).value)
            else:
                for col in range(0, ncols):
                    ws.write(row, col, rs.cell(row, col).value)


def wayfair_crawl(url):
    h = httplib2.Http(timeout=30)
    h.folllow_redirects = False
    response, content = h.request(uri=url, method='GET', headers={})
    print response.status
    doc = PyQuery(content)
    price = re.sub('\s', '', doc('span.product_price').text())
    img_list = []
    nodeList = doc('div.js-slider-container > div > a > img')
    for node in nodeList:
        img_url = PyQuery(node).attr('src')
        if img_url:
            img_list.append(img_url)
    return price, ','.join(img_list)

def extractNum(text):
    result = re.findall('([-\d\. ]+)', text)
    if result:
        return result[0]

if __name__ == '__main__':
    run("c:/users/administrator/desktop/wayfair500.xls", 'ABCDEFG.xls','.', 'add')    