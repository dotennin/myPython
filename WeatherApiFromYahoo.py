# -*-coding:UTF-8 -*-
import json, urllib2

url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=400040'
try:
    r = urllib2.urlopen(url)
    root = json.loads(r.read())
    print 'title=' + root['title']
    description = root['description']
    print 'publicTime=' + description['publicTime']

    forecasts = root['forecasts']
    for forecast in forecasts:
        print '    dateLabel=' + forecast['dateLabel'] + ',telop=' + forecast['telop'] + ',date=' + forecast['date']
finally:
    r.close()