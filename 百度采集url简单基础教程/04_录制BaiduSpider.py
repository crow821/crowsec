# -*- encoding: utf-8 -*-
import re 
import requests
import threading 
import queue
from bs4 import BeautifulSoup as bs
from argparse import ArgumentParser

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
        temp_urls = soup.find_all(name='a', attrs={'data-click': re.compile(('.')), 'class':None})
        for temp_url in temp_urls:
            real_urls = requests.get(url=temp_url['href'], headers=self.headers,timeout=10)
            if real_urls.status_code == 200:
                tmp = real_urls.url
                print(tmp)
                with open('F:\\渗透\\0渗透\\0渗透ppt\\crow渗透测试课件\\09_百度采集url简单基础教程\\test_url.txt', 'a+') as f:
                    f.write(tmp + '\n')
      

def main(keywords,thread_nums):
    q = queue.Queue()
    thread_nums = thread_nums
    threads = []
    for i in range(0,760,10):
        baidu_url = ('https://www.baidu.com/s?wd=%s&pn=%s'%(keywords,str(i)))
        q.put(baidu_url)
    for i in range(thread_nums):
        threads.append(BaiduSpider(q))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
   main('crow', 10)
