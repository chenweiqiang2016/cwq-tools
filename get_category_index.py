import MySQLdb

conn = MySQLdb.connect(host='10.5.17.188',
                       user='litb_merchadmin',
                       passwd='0643CABB-971E-47F1-9B09-6FAE2B1B5D2E',
                       db='aims')

cursor = conn.cursor()

# sql="""select * from products_sammydress limit 1""" #(87889696L, datetime.date(2015, 7, 10), '11.46', '21.68', 0L, 0L, 0L, 44L, 1L, 2L)

sql = """select page, position from products_sammydress where product_id=%s and capture_date='2015-10-09'"""

fr = open("2015-10-13_productId.csv", 'r')
fw = open("2015-10-13_productId-results.csv", 'r')

while True:
    content = fr.readline().replace("\n", "").strip()
    if not content:
        break
    product_id = int(content)
    cursor.execute(sql, product_id)
    results = cursor.fetchall()
    if len(results) > 1:
        print 'check: product_id(%s)' %product_id
    page = int(results[0][0])
    position = int(results[0][1])
    
    category_index = (page - 1) * 60 + position #语义错误, 必须先减去1
    
    line = str(product_id) + "\t" + str(category_index) + '\n' #+ "\t" + str(page) + "\t" + str(position) + "\n"
    fw.write(line)

fr.close()
fw.close()
