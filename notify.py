#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib
from email.mime.text import MIMEText

#要发给谁
mail_to="guozirong@mobike.com"

def notify(sub,content):
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.yeah.net"
    mail_user="guozirong"
    mail_pass="gzr,1029"
    mail_postfix="yeah.net"
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = mail_to
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, mail_to, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(e)        
        return False