# -*- encoding: utf-8 -*-
import re 
import requests
import threading 
import queue
from bs4 import BeautifulSoup as bs
from argparse import ArgumentParser
"""
本程序可以实现百度url的获取，但是没有对url做过滤，一个网站中的url可能会多次被采集
程序中文件的位置需要自己修改，Windows下需要使用\\
使用方法：python3 BaiduSpider.py 关键字 -t 线程数   其中关键字不需要加引号
本程序只供学习，数据没有进行处理，比较杂乱
                        20191122
"""

class BaiduSpider(threading.Thread):
    def __init__(self,q):
        super(BaiduSpider, self).__init__()
        self._q = q
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        self.url_list = []
    def run(self):
        while not self._q.empty():
            urls = self._q.get()
            try:
                self.spider(urls)
            except:
                pass

    def spider(self,url):      
        r = requests.get(url=url, headers=self.headers, timeout=5)
        soup = bs(r.content, 'lxml')
        temp_urls = soup.find_all(name='a', attrs={'data-click':re.compile(('.')), 'class':None})
        for temp_url in temp_urls:
            real_url = requests.get(url=temp_url['href'], headers=self.headers, timeout=20)
            if real_url.status_code == 200:
                tmp = real_url.url
                print(tmp)
                with open('F:\\渗透\\0渗透\\0渗透ppt\\crow渗透测试课件\\09_百度采集url简单基础教程\\test_url.txt', 'a+') as f:
                    f.write(tmp + '\n')
                

def main(keywords,thread_nums):
    q = queue.Queue()
    thread_nums = thread_nums
    threads = []
    for i in range(0,760,10):
        baidu_url = ('https://www.baidu.com/s?wd=%s&pn=%s'%(keywords,str(i)))
        # print(baidu_url)
        q.put(baidu_url)
    for i in range(thread_nums):
        threads.append(BaiduSpider(q))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    crow = """
  ____        _     _       ____        _     _           
| __ )  __ _(_) __| |_   _/ ___| _ __ (_) __| | ___ _ __ 
|  _ \ / _` | |/ _` | | | \___ \| '_ \| |/ _` |/ _ \ '__|
| |_) | (_| | | (_| | |_| |___) | |_) | | (_| |  __/ |   
|____/ \__,_|_|\__,_|\__,_|____/| .__/|_|\__,_|\___|_|   
                                |_|       
                                            by crow V1.0
    """
    print(crow)
    print('\n'*2)
    arg = ArgumentParser(description='BaiduSpider')
    arg.add_argument('keywords',help='inurl:.asp?id=1')
    arg.add_argument('-t', '--thread', help='the thread_counts', dest='thread_counts', type=int, default=10)
    result = arg.parse_args()
    main(result.keywords,result.thread_counts)


