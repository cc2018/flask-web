# -*- coding: utf-8 -*-

import urllib.request

url = "http://www.yideschool.com/peier/index.php?g=Html&m=Vote&a=dovote&token=ztes916&openid=oKrcTwZ_YeexNR_WrATrwBRBuqbI&id=3"

postdata = urllib.parse.urlencode({
    "voter_id":"999"
}).encode('utf-8')

header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-cn",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://www.yideschool.com",
    "Connection":"keep-alive",
    "Host":"c.highpin.cn",
    "Referer":"http://www.yideschool.com/peier/index.php?g=Html&m=Vote&a=vote&token=ztes916&openid=oKrcTwZ_YeexNR_WrATrwBRBuqbI&id=3&vid=999",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.8 NetType/WIFI Language/zh_CN"
}

req = urllib.request.Request(url, postdata, header)
r = urllib.request.urlopen(req)
print(r.read().decode('utf-8'))
