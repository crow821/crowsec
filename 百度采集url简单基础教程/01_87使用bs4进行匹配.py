# -*- encoding: utf-8 -*-
import re,requests,urllib,queue,threading
from bs4 import BeautifulSoup as bs

"""
程序可以运行，如果加上延时效果应该更加好一点的
本程序仅限学习，请勿他用   
                        by crow
"""

class Movie87_Spider(threading.Thread):
    def __init__(self,q):
        super(Movie87_Spider, self).__init__()
        self._q = q
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/35.0.1916.114 Safari/537.36',
        'Cookie': 'AspxAutoDetectCookieSupport=1'
    }
    def run(self):
        while not self._q.empty():
            deal_url = self._q.get()
            try:

               self.spider(deal_url,self.headers)
            except:
                pass
    def spider(self, url,headers):
        r = requests.get(url=url, headers=headers)
        soup = bs(r.content, 'lxml')
        # print(soup)
        real_urls = soup.find_all(name='img', attrs={'class':re.compile(('.'))})
        for real_url in real_urls:
            real_url_content = re.findall(r'alt="(.*?)"', str(real_url))
            real_url_all = re.findall(r'data-original="(.*?)"', str(real_url))
            print(real_url_all[0],real_url_content[0])
            with open('F:\\渗透\\0渗透\\0渗透ppt\\crow渗透测试课件\\09_百度采集url简单基础教程\\img_87\\' + str(real_url_content[0]) + '.jpg', 'wb') as f:
                f.write((urllib.request.urlopen(real_url_all[0])).read())

       
def main():
    thread_counts = 2 # 定义线程数
    threads = []
    q = queue.Queue()
    for i in range(1,225):
            origin_url = 'https://www.87kk.tv/vodtype/1-' + str(i) + '.html'
            q.put(origin_url)
    for i in range(thread_counts):
        threads.append(Movie87_Spider(q))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()







