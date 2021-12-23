# -*- encoding: utf-8 -*-
# Time : 2021/12/21 21:07:19
# Author: crow

import argparse
import requests
import random
import string
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header


parser = argparse.ArgumentParser(description='Beacon Info')
parser.add_argument('--computername')
parser.add_argument('--internalip')
parser.add_argument('--username')
args = parser.parse_args()

internalip = args.internalip
computername = args.computername
username = args.username
ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
t_time = time.ctime()

content = """

您有霉国-2新主机上线啦

主机名: {}
IP: {}
用户名: {}
Token: {}
上线时间：{}
请注意查收哦~
""".format(internalip, computername, username, ran_str, t_time)



#1. 发送文本文件

sender = 'xxxxxxxx@qq.com' #发件人邮箱
receiver = 'YYYYYYYYYYYYY@qq.com' #收件人邮箱
mail_pass = 'cccccccccccccccc' #qq邮箱授权码

#text为邮件正文内容，plain为文本格式，'utf-8'为编码格式
# text = '您有新主机上线。。。'
# content
message = MIMEText(content, 'plain', 'utf-8')

#添加Header信息，From，To，Subject分别为发送者信息，接收者消息和邮件主题
message['From'] = Header(sender, 'utf-8')
message['To'] = Header(receiver, 'utf-8')

subject = 'Cobalt Strike上线提醒'
message['Subject'] = Header(subject, 'utf-8')


try:
    #smtp.xxx.com为邮箱服务类型，25为STMP的端口
    smtpObj = smtplib.SMTP('smtp.qq.com', 25)#smtp.xxx.com为邮箱服务类型，25为STMP
    #smtpObj = smtplib.SMTP_SSL('smtp.xxx.com', 'xxx邮件服务的端口号')     
    
    smtpObj.login(sender, mail_pass)#登录
    smtpObj.sendmail(sender, receiver, message.as_string())#发送
    print ("邮件发送成功")
except smtplib.SMTPException as e:
    print(e)
    print ("Error: 邮件发送失败")


