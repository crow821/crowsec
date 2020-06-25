# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
import requests
import re

def ua():
    UA = UserAgent()
    return UA.random

#  http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=钢铁侠&pn=10

def check_pics_number(keywords):
    page_num = 1
    check_page = 0
    while True:
        check_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(keywords) + '&pn=' + str(
            check_page)
        check_content = requests.get(url=check_url, headers={'User-Agnet': ua()})
        print('[INFO]当前第{}页存在'.format(page_num))
        if '抱歉，没有找到与' in check_content.text:
            # print('')
            return page_num
            break
        page_num += 1
        check_page = ((page_num) * 20) - 20



# check_pics_number('crow')

def spider_pic_url(keywords):
    for j in range(0, 1720, 20):
        # print(j)
        spider_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(keywords) + '&pn=' + str(j)
        # print(spider_url)
        r_photos = requests.get(url=spider_url)
        urls_re = re.findall(r'"objURL":"(.*?)"', r_photos.text)
        for url_re in urls_re:
            # print(url_re)
            new_jpg = requests.get(url_re)
            if new_jpg.status_code == 200:
                print(url_re)
                # with open('images', 'wb') as f:
                    # f.write('')



spider_pic_url('corw')