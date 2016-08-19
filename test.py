# -*-coding:UTF-8 -*-
#!/usr/bin/python

# ---------------------------------------
#  @program：cside作業一覧
#  @author：nochi
#  @data：2016-08-18
# ---------------------------------------
import datetime, os.path
import urllib, urllib2
import cookielib, json
import re
from xml.sax.saxutils import *

output = open('./output/txt/cside.txt', 'wb')
cookie_file = './output/cookie'
cookie_exists = os.path.exists(cookie_file)

cj = cookielib.MozillaCookieJar(cookie_file)

if cookie_exists:
    # cookieからファイルを読み取り
    try:
        cj.load(cookie_file, ignore_discard=True, ignore_expires=True)
    except:
        cookie_exists = False


opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36')]

urllib2.install_opener(opener)

if not cookie_exists:
    # 登陆获取cookies
    postdata = urllib.urlencode({
        'clientTimezoneOffset': '-540',
        'url': '/dashboard',
        'userId': 'wenhua4438@gmail.com',
        'password': 'woWvoLmN'})

    url = "https://nndo.backlog.jp/Login.action"

    rep = urllib2.Request(
        url,
        data=postdata
    )
    login = urllib2.urlopen(rep)
    cj.save(cookie_file, ignore_discard=True, ignore_expires=True)

project = urllib2.urlopen(urllib2.Request("https://nndo.backlog.jp/find/C_SIDE"))
regex = re.compile('(?#キー)"issueKey":"([\d\D]*?)"'
                   '[\d\D]*?(?#種別)"projectId":null,"name":"([\d\D]*?)"'
                   '[\d\D]*?"(?#件名)summary":"([\d\D]*?)"'
                   '[\d\D]*?(?#内容)"description":"([\d\D]*?)"'
                   '[\d\D]*?(?#優先度)"formattedDescription.*?"name":"([\d\D]*?)"'
                   '[\d\D]*?(?#担当者)"assignee":{"id":[\d\D]*?,"userId":"[\d\D]*?","name":"([\d\D]*?)"'
                   '[\d\D]*?(?#登録者)"createdUser":{"id":[\d\D]*?,"userId":"[\d\D]*?","name":"([\d\D]*?)"'
                   '[\d\D]*?(?#登録日)"created":"([\d\D]*?)T'
                   '[\d\D]*?(?#更新日)"updated":"([\d\D]*?)T[\d\D]*?'
                   , re.IGNORECASE)

for i in cj:
    print 'Name = ' + i.name
    print 'Value = ' + i.value


for i in regex.finditer(project.read()):

    output.write("キー: " + i.group(1) + "\n")
    output.write("種別: " + i.group(2) + "\n")
    output.write("件名: " + unescape(i.group(3)) + "\n")
    output.write("内容: \n" + unescape(i.group(4).decode('string_escape')) + "\n")
    output.write("優先度: " + unescape(i.group(5)) + "\n")
    output.write("担当者: " + unescape(i.group(6)) + "\n")
    output.write("登録者: " + unescape(i.group(7)) + "\n")
    output.write("登録日: " + i.group(8) + "\n")
    output.write("更新日: " + i.group(9) + "\n")
    output.write("-----------------------------------------------------------------------------\n\n")
output.close()

# 画像ゲッチャー
# regex = re.compile(r'<img src="([\d\D]*?)"')
# for i in regex.finditer(project.read()):
#
#     image_name = re.sub(r'(http://.*\.+.*/)|(.*\.+.*/)|(\{\{.*\}\}\.?.{0,3})|(/)|(.+=.+)', "", i.group(1))
#
#     if image_name:
#         image_data = urllib2.urlopen(i.group(1)).read()
#         output = open('.output/image/' + image_name, 'a+')
#         output.write(image_data)
#         output.close()


# cookie 出力
#print cj._cookies.values()

