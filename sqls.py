#-*- coding: utf-8 -*-

"""
    update stall_products set sku_size="iPhone5/5s一套", sku_color="橙（前+后膜）", sku_price="7.50 元", sku_amount=0 where merchant='1688' and sku_id='522157555897';
"""
fr = open('a.csv','r')
while True:
    line = fr.readline().strip()
    if not line:
        break
    fields = line.split('\t')
    part0 = "update stall_products set "
    part5 = " where merchant='1688' and sku_id=" + fields[0] + ";"
    part1, part2, part3, part4 = "", "", "", ""
    if fields[1].strip():
        part1 = "sku_size='" + fields[1].strip() + "', "
    if fields[2].strip():
        part2 = "sku_color='" + fields[2].strip() + "', "
    if fields[3].strip():
        part3 = "sku_price='" + fields[3].strip() + "', "
    if fields[4].strip():
        part4 = "sku_amount=" + fields[4].strip()
    
    sql = part0 + part1 + part2 + part3 + part4 + part5
    print sql
