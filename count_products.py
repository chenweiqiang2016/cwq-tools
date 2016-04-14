# -*- coding: utf-8 -*-

"""statistic products count per category
   input: filename

2015/9/8 取消品类字段在字段前三位的限制
2015/9/9 格式化输出各个品类的产品数量

eclipse 当季流行>商场同款(长度为25)
'\xe5\xbd\x93\xe5\xad\xa3\xe6\xb5\x81\xe8\xa1\x8c>\xe5\x95\x86\xe5\x9c\xba\xe5\x90\x8c\xe6\xac\xbe'

k1:字符编码测试情况
str="中文test" 
'\xd6\xd0\xce\xc4test'
len(str)=8
c = unicode(str, "gb2312")
u'\u4e2d\u6587test'
len(c)=6
c.encode("utf-8")
10
'\xe4\xb8\xad\xe6\x96\x87test'
k2:
注意%40s的应用
"""

import codecs
import os

def stat(filename):
    f = open(filename, 'r')
    first_line = f.readline()
    if first_line.startswith(codecs.BOM_UTF8):
        first_line = first_line[len(codecs.BOM_UTF8):]
    headers = first_line.strip().split('\t')
    categoryList, countList = [], []
    for line in f.readlines():
        datas = line.strip().split('\t')
        categoryPath = ''
        if 'level1_category' in headers: #一级品类为空的情形没有做处理
            value = datas[headers.index('level1_category')].strip()
            categoryPath = value.strip()
        if 'level2_category' in headers:
            value = datas[headers.index('level2_category')].strip()
            if value:
                categoryPath = categoryPath + '>' + value
        if 'level3_category' in headers:
            value = datas[headers.index('level3_category')].strip()
            if value:
                categoryPath = categoryPath + '>' + value
        if categoryPath in categoryList:
            index = categoryList.index(categoryPath)
            countList[index] = countList[index] + 1
        else:
            categoryList.append(categoryPath)
            countList.append(1)
    formatStr = 'stat output(%s categories):\n' %len(categoryList) 
    formatStr2 = formatStr
#     everyRow = "%-" + str(evalLength(categoryList)+1) + "s %" + str(evalLength(countList)) + "s\n"  #everyRow = "%%ss: %%ss\n" %(evalLength(categoryList), evalLength(countList)) #技术上没有实现
    c_length = evalLength(categoryList)
    n_length = evalLength(countList)
    #仅仅用于写入文件
    for i, cate in enumerate(categoryList):
        formatStr = formatStr + cate + ":" + (c_length - len_str(cate)) * ":" + ":" + (n_length-len_str(str(countList[i]))) * ":" + str(countList[i]) + "\n"
        #formatStr = formatStr + everyRow %(cate+":", countList[i]) #错误, 因为中文字符被算作了3位
    if True:
        writeIntoFile(formatStr)
    #用于打印输出
    for i, cate in enumerate(categoryList):
        formatStr2 = formatStr2 + (n_length-len_str(str(countList[i]))) * " " + str(countList[i]) + " " + cate + "\n"
    print formatStr2

def evalLength(aList): 
    '''传入一个list, 求出该list中最长字符串的长度
    '''
    max_length = 0
    for element in aList:
        element = str(element) #数字转化为字符串
        if len_str(element) > max_length:
            print element
            max_length = len_str(element)
    return max_length

def len_str(str1):
    """求出字符串实际显示的长度"""
    u_str = unicode(str1, "utf-8")
    g_str = u_str.encode("gb2312") #实际显示中一个中文占2个位置 gb2312也是2个长度编码一个中文
    return len(g_str)

def writeIntoFile(content, filename = "cwq.txt"):
    path = "C:/users/chenweiqiang/desktop"
    fw = open(os.path.join(path, filename), "w")
    fw.write(content)
    fw.close()
        
if __name__ == '__main__':
    filename = 'E:1688_04-06-2016_productInfo.csv' #sys.argv[1]
    stat(filename)