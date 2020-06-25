# -*- coding: utf-8 -*-
import requests
import re
# # url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1592879745611_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=crow'
# url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=crow&pn=1720'
# r = requests.get(url)
# print(r.text)
# # if '抱歉，没有找到' in r.text:
# #     print('bingo')
# # http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=钢铁侠&pn=10
# """
# # thumbURL":"https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=3332861793,494080402&fm=26&gp=0.jpg","""
# urls = re.findall(r'thumbURL":"(.*?)",', r.text)
# for u in urls:
#     print(u)
# 拿到原图数据之后
# 1. 遍历所有的页数，取出所有的图片
# 2. 下载图片
# 优化
# 以输入关键字作为文件夹的名字
# 输入txt，按照txt中的文字进行自动爬取
def read_file():
    read_txt = 'test.txt'
    with open(read_txt, 'r') as f:
        for i in f.readlines():
            print(i[:-1])
            print('*')

read_file()

"""
将每一个页面的数据都爬取下来
pic地址
将图片的地址里面的图片下载下来
    多线程的方法来下载
    队列来保证多线程下载
"""