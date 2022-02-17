# -*- encoding: utf-8 -*-
# Time : 2022/02/17 10:04:39
# Author: crow
# 微信公众号：乌鸦安全
'''
不好用哦，不建议用这个
最新消息说低版本向日葵可能会有10000多的端口
所以在这里要从10000-65535扫描，推荐使用其他的
这个不好用，我自己都不用
'''

import random
import requests
import threading
from queue import Queue
from socket import *
import time 



class Check_Ports(threading.Thread):
    def __init__(self, queue, host):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while not self._queue.empty():
            Port = self._queue.get()
            # host = self._host
            try:
                self.portScanner(host, Port)
            except Exception as e:
                # print(e)
                pass
    

    def portScanner(self,host,port):
        setdefaulttimeout(1)
        try:
            s = socket(AF_INET,SOCK_STREAM)
            s.connect((host,port))
            print('[+] %d open' % port)
            s.close()
        except:
            # print("", port)
            pass
            # print('[-] %d close' % port)


def check_ip(host):
    # path = host
    queue = Queue()
    for port in range(10000,65535):    
        queue.put(port)
    print('[+] Loading complite')
    threads = []
    thread_counts = 200  # 定义线程
    for i in range(thread_counts):
        threads.append(Check_Ports(queue, host))
    for t in threads:
        t.start()
    for t in threads:
        t.join()



def title():
    print('+------------------------------------------')
    print('[+]  \033[34mGithub : https://github.com/crow821/                                \033[0m')
    print('[+]  \033[34m公众号 : 乌鸦安全                                                     \033[0m')
    print('[+]  \033[34m功  能:  端口扫描(仅作参考,不要用这个，太难用了，狗都不用)                  \033[0m')
    print('[+]  \033[36m使用格式:  python3 xrk_PortScan.py + ip                               \033[0m')
    # print('[+]  \033[36m使用格式:  python3 xrk_PortScan.py                                \033[0m')
    print('+------------------------------------------')


if __name__ == "__main__":
    title()
    start = time.time()
    
    # print('[+] info: please input your host ')
    # print('[+] for example: 127.0.0.1 ')
    host = input("[+] host: ")
    check_ip(host)
    print('[+] check complete, Scan time {}'.format(time.time- start))
