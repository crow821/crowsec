# -*- encoding: utf-8 -*-
import re,urllib,requests,threading,queue
from bs4 import BeautifulSoup as bs 


class Movie_87_spider(threading.Thread):
    def __init__(self,q):
        super(Movie_87_spider, self).__init__()
        self.q = q
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    def run(self):
        while not self.q.empty():
            deal_url = self.q.get()
            try:
                self.spider(deal_url,self.headers)
            except:
                pass
    def spider(self,url,headers):
        r = requests.get(url=url, headers=headers)
        soup = bs(r.content, 'lxml')
        real_urls = soup.find_all(name='img', attrs={'class': re.compile(('.'))})
        for i in real_urls:
            real_url = re.findall(r'data-original="(.*?)"', str(i))
            real_urlname = re.findall(r'alt="(.*?)"', str(i))
            print(real_url[0],real_urlname[0])
            with open('F:\\渗透\\0渗透\\0渗透ppt\\crow渗透测试课件\\09_百度采集url简单基础教程\\img_87\\' + str(real_urlname[0]) + '.jpg', 'wb') as f:
                f.write((urllib.request.urlopen(real_url[0])).read())


def main():
    q = queue.Queue()
    thread_counts = 2 # 定义一个线程
    threads = []
    for i in range(1,256):
        temp_url = 'https://www.87kk.tv/vodtype/1-' + str(i) + '.html'
        q.put(temp_url)
    for i in range(thread_counts):
        threads.append(Movie_87_spider(q))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

