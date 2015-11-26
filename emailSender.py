# -*-coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
# from email.utils import parseaddr, formataddr

###########################################################################
#Q1: unicode("中文字符") 与 u'中文字符' 意思是否一致
#A1: 不同, 初步验证unicode使用sys定义的编码, u''使用 # coding: 定义的编码
#Q2: unicode("中文字符") 与 unicode("中文字符", sys.getdefaultencoding()) 意思是否一致
#Q3: 为何抓取机上非要采用unicode("中文字符", 'GBK')这种形式
###########################################################################

#这个是配合unicode()方法, 否则报错, 抓取机上设置为GBK
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from_address = "chenweiqiang2016@163.com"
to_address = ["chenweiqiang@lightinthebox.com", "yanfushuang@lightinthebox.com"]

def email(message):
    #简单模式
    #1.邮件没有主题 2.发件人没有显示为友好的名字 3.没有显示收件人
    #可能造成发送失败, 报错:smtplib.SMTPDataError: (554, 'DT:SPM smtp1
    server = smtplib.SMTP('smtp.163.com', 25)
    server.set_debuglevel(1)
    server.login(from_address, '09151827283110')
    
    msg = MIMEText(message, 'plain', 'utf-8')
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
    
def email2(message):
    #完整的邮件 指定发件人的昵称, 收件人, 邮件主题
    server = smtplib.SMTP('smtp.163.com', 25)
    server.set_debuglevel(1)
    server.login(from_address, '09151827283110')
    
    msg = MIMEText(message, 'plain', 'utf-8')
    #之前使用u'中文字符'的方式, 本地运行没有问题, linux机子失败
    #SyntaxError: (unicode error) 'utf8' codec can't decode byte 0xd0 in position 4:
    msg['From'] = unicode('AIMS系统信息  <chenweiqiang2016@163.com>').encode('utf-8')
    msg['To'] = unicode('兰亭工作邮箱  <chenweiqiang@lightinthebox.com>').encode('utf-8')
    msg['Subject'] = Header("Crawl site notice", "utf-8")
    
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

if __name__ == '__main__':
    pass