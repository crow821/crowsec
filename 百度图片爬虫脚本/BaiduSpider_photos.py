# coding: utf-8
# by crow 2020-06-24
# 使用方法：只需要新建一个spider.txt文件，然后将需要爬取的关键字写入就可以了，具体的速度可以通过线程数进行调节
import re  # 正则匹配数据的模块
import requests  # 请求数据的模块
import time  # 时间模块
import os
import threading  # 多线程模块
from fake_useragent import UserAgent  # 作为请求头的一部分信息
from queue import Queue  # 队列，针对多线程使用
import hashlib   # 将数据转化为hash，用来jpg文件的命名

# pip|pip3 install *****

# 定义一个临时的user-agent,用来请求数据使用的
def ua():
    UA = UserAgent()
    return UA.random


# 先测试下一共有多少页图片
def check_pics_number(keywords):
    """
    检查一共有多少张图的
    第i页 =  i * 20 -20
    :return: page 一共有多少页
    """
    page_num = 1
    check_page = 0
    while True:
        check_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(keywords) + '&pn=' + str(check_page)
        check_content = requests.get(url=check_url, headers={'User-Agnet': ua()})
        print('[INFO]当前第{}页存在'.format(page_num))
        if '抱歉，没有找到与' in check_content.text:
            # print('')
            return page_num
            break
        page_num += 1
        check_page = ((page_num) * 20) - 20


# 接收图片页数，因为一页大概是20张，所以总的张数等于 页数 * 20 但是因为有打不开，最后一页小于20张的原因，最终爬下来的图片都会小于总张数
# check_time_start = time.time()
# print(check_pics_number('钢铁侠'))
class BaiduSpider_photos(threading.Thread):
    def __init__(self, queue, keywords):
        threading.Thread.__init__(self)
        self._queue = queue
        self._keywords = keywords

    def run(self):
        while not self._queue.empty():
            url = self._queue.get()
            # self.spider(url)
            try:
                self.spider(url, self._keywords)
            except Exception as e:
                # print('目前有些错误')
                # print(e)
                pass
    def spider(self, url, keywords):
        r_photos = requests.get(url=url, headers={'User-Agent':ua()}, timeout=2)
        # r_photos = requests.get(url=url,timeout=1)
        r_urls = re.findall(r'"objURL":"(.*?)"', r_photos.text)
        for r_url in r_urls:
            # print('r_url的值\n{}'.format(r_url))
            try:
                r_url_get = requests.get(url=r_url, headers={'User-Agent':ua()}, timeout=2)
                # r_url_get = requests.get(url=r_url, timeout=3)
                # print('此时r的值是：{}'.format(r_url_get.text))
                if r_url_get.status_code == 200:
                    print('[INFO]当前正在下载的url链接为：', r_url)
                    # time.sleep(1)
                    m = hashlib.md5()
                    m.update(r_url.encode())
                    name = m.hexdigest()
                    print('[INFO]正在保存图片')
                    # res = requests.get(url=r_url, timeout=3)

                    res = requests.get(url=r_url, headers={'User-Agent':ua()}, timeout=3)
                    image_content = res.content
                    # filename = 'image/' + name + '.jpg'
                    filename = keywords + '/' + name + '.jpg'

                    with open(filename, 'wb') as f:
                        f.write(image_content)
                    print('[INFO]保存成功，图片名为：{}.jpg'.format(name))
            except Exception as e:
                # print(e)
                # print('有错误')
                pass


def deal_url(keywords, maxpage):
    queue = Queue()  # 使用队列存放url
    for j in range(0, maxpage, 20):
        spider_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(keywords) + '&pn=' + str(j)
        print('当前要访问的url是：', spider_url)
        queue.put(spider_url)
    threads = []
    thread_count = 30  # 定义爬虫线程，这里可以自定义
    for i in range(thread_count):
        # print('当前i的值是:',i)
        threads.append(BaiduSpider_photos(queue, keywords))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def create_file(keywords):
    # 新建以关键字为文件夹的操作
    create_path = keywords
    if not os.path.exists(create_path):
        os.mkdir(create_path)
    else:
        print('[INFO]已存在以{}关键字命名的文件夹'.format(keywords))

def read_file():
    # spider.txt文件为爬取的对象
    read_list = []
    read_txt = 'spider.txt'
    with open(read_txt, 'r') as f:
        for i in f.readlines():
            # print(i[:-1])
            read_list.append(i[:-1])
        # print(read_list)
        return read_list



def main():
    read_list = read_file()
    for read in read_list:
        keywords = str(read)
        create_file(keywords)
        print('[INFO]正在搜索关键字：{}一共有多少张图，请稍等。。。'.format(keywords))  # 因为这个页面防止被ban掉，所以没有使用多线程
        search_time_start = time.time()
        page_num = check_pics_number(keywords)
        print('[INFO]关键字{}大约有{}张图左右'.format(keywords, (page_num * 20)))
        print('[INFO]搜索本关键字一共花费{:.3f} s'.format(time.time() - search_time_start))
        print('[INFO]正在下载...')
        # keywords = 'crow'
        # page_num = 10
        download_time = time.time()
        deal_url(keywords, page_num)
        print('下载这些图片一共用时:{:.3f} s'.format(time.time() - download_time))








if __name__ == '__main__':
    main()



