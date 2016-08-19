#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib, re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.Utils import formatdate
from email.Header import Header
from email import encoders
#######################################################################################
# gmailにログインするときのメールアドレス
gmail_address = 'nochi0105@gmail.com'
# gmailにログインするときのパスワード
gmail_passwd = 'wh314751'

# gmailのSMTPサーバアドレス
gmail_smtp_address = 'smtp.gmail.com'
# gmailのSMTPサーバポート番号
gmail_smtp_port = 587

# 送信元メールアドレス
from_address = 'nochi0105@gmail.com'
# 送信先メールアドレスのリスト
to_address = ['wenhua4438@gmail.com', '314788851@qq.com', ]

# 件名 title
subject = u'日本語サブジェクト'

# うPするフャイル指定
file_path = "sample.png"

# メール本文
body = u'''
ボディも日本語だよ。
改行も大丈夫だよ。
汉语也是没问题的哟
'''
#######################################################################################

#本文処理
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = ', '.join(to_address)
msg['Date'] = formatdate()
msg['Subject'] = Header(subject.encode('UTF-8'), 'UTF-8')

msg.attach(MIMEText(body.encode('UTF-8'), 'plain', 'UTF-8'))

#フャイル処理
if re.search('^[^/]+$', file_path) is not None:
    filename = file_path
else:
    filename = file_path[file_path.rindex("/")+1:]

attachment = open(file_path, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

smtpobj = smtplib.SMTP(gmail_smtp_address, gmail_smtp_port)
smtpobj.ehlo()
smtpobj.starttls() # こっからSSL
smtpobj.ehlo()
smtpobj.login(gmail_address, gmail_passwd) # ログイン
smtpobj.sendmail(from_address, to_address, msg.as_string()) # 送信
smtpobj.close()