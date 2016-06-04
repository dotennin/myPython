#coding:utf-8
import urllib2, re
url = "http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId=40"
response = urllib2.urlopen(url)
response.getcode()

html = response.read()
print re.findall("http://\w*?\.yinyuetai\.com/uploads/videos/common/.*?(?=&br)",html)