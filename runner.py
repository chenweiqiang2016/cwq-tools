# -*- coding: utf-8 -*-

import lockfile
import sys
import os
import glob
import re
import datetime

excludedFiles = ['crawler2.py', 'utils.py', 'runner.py', 'csv2xls.py', 'stats_data.py']

crawledFilePath = '/home/lishangqiang/output/bak'

GLOB_FILE_PATTERN = '*productInfo.csv'
DATE_PATTERN = '(\d\d)-(\d\d)-(\d\d\d\d)'

DAYS_DICT = {'WEEK': 7,
             "FORTNIGHT": 15,
             "MONTH": 30}

def schedule_crawl(aims_dir, interval):
    fileList = os.listdir(aims_dir) #列出全部文件
    #得出商户对应的脚本文件
    scriptList = []
    for filename in fileList:
        if filename.endswith('.py') and filename not in excludedFiles:
            scriptList.append(filename)
    #获得在指定时间间隔内没有被执行的商户
    merchantList = []
    for scriptFile in scriptList:
        merchantName = scriptFile.replace('.py', '')
        crawledHistoryFile = glob.glob(crawledFilePath + merchantName + GLOB_FILE_PATTERN)
        #获取最新抓取时间
        latestCrawlDate = None
        for filename in crawledHistoryFile:
            results = re.findall(DATE_PATTERN, filename)
            thisCawlDate = datetime.date(int(results[0][2]), int(results[0][0]), int(results[0][1]))
            if latestCrawlDate is None or thisCawlDate > latestCrawlDate:
                latestCrawlDate = thisCawlDate
        #是否在要求的间隔内抓取过
        nowDate = datetime.date.today()
        if not latestCrawlDate or (nowDate-latestCrawlDate).days >= DAYS_DICT[interval]:
            merchantList.append(merchantName)
    
    for merchant in merchantList:
        cmd = "cd %s; python crawler2.py %s" % (aims_dir, merchant)
        print "execute cmd: '%s'" %cmd
        email("["+ getNowTimeFormatStr() +"] Begin to crawl merchant [" + merchant + "]")
        rc = os.system(cmd)
        status = 'succeed' if rc==0 else "failed"
        email("["+ getNowTimeFormatStr() +"] Crawl %s %s" %(merchant, status))

def email(message):
    #报错:smtplib.SMTPDataError: (554, 'DT:SPM smtp1 因为没有设置主题和收件人
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    
    smtp = smtplib.SMTP("smtp.163.com", 25)
#     smtp.set_debuglevel(1)

    msg = MIMEText('<html><h1>' + message + '</h1></html>', 'html', 'utf-8')
    msg['Subject'] = Header(u'Crawl site notice', 'utf-8')
    msg['To'] = u"工作邮箱 <chenweiqiang@lightinthebox.com>".encode("utf-8")
    msg['From'] = u"AIMS系统信息 <chenweiqiang2016@163.com>".encode("utf-8")
#     smtp.connect('smtp.163.com')
    smtp.login('chenweiqiang2016@163.com', '09151827283110')
    smtp.sendmail('chenweiqiang2016@163.com', 'chenweiqiang@lightinthebox.com', msg.as_string())
    smtp.quit()
    
def getNowTimeFormatStr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
if __name__ == '__main__':

    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: python runner.py <dir> <WEEK|MONTH|FORTNIGHT>"
        sys.exit(1)
    scriptsDir = sys.argv[1]
    interval = sys.argv[2].upper()
    lock = lockfile.FileLock("runner")
    try:
        lock.acquire(10)
        schedule_crawl(scriptsDir, interval)
    except Exception, e:
        print >> sys.stderr, e
        print >> sys.stderr, "runner.py is executing now..."
    finally:
        lock.release()