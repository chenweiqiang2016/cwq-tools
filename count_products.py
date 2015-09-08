# -*- coding: utf-8 -*-

"""statistic products count per category
   input: filename
"""

import codecs

def stat(filename):
    f = open(filename, 'r')
    first_line = f.readline()
    if first_line.startswith(codecs.BOM_UTF8):
        first_line = first_line[len(codecs.BOM_UTF8):]
    headers = first_line.strip().split('\t')
    categoryList = []
    countList = []
    for line in f.readlines():
        datas = line.strip().split('\t')
        categoryName = ''
        if 'level1_category' in headers and headers.index('level1_category') == 0:
            categoryName = datas[0].strip()
        if 'level2_category' in headers and headers.index('level2_category') == 1:
            if datas[1].strip():
                categoryName = categoryName + '>' + datas[1].strip()
        if 'level3_category' in headers and headers.index('level3_category') == 2:
            if datas[2].strip():
                categoryName = categoryName + '>' + datas[2].strip()
        if categoryName in categoryList:
            index = categoryList.index(categoryName)
            countList[index] = countList[index] + 1
        else:
            categoryList.append(categoryName)
            countList.append(1)
    formatStr = 'stat output:\n'
    for i, cate in enumerate(categoryList):
        formatStr = formatStr + '%45s: %10s\n' % (cate, countList[i])
    print formatStr
        

if __name__ == '__main__':
    filename = 'datas/nanzhuang-tmall_09-07-2015_productInfo.csv' #sys.argv[1]
    stat(filename)
    


