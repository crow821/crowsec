# -*- encoding: utf-8 -*-
# Time: 2021/10/16 15:44:37
# Author: crow 



import requests
import re 
import sys,random
requests.packages.urllib3.disable_warnings()
import threading
from queue import Queue
import time 

def title():
    print('+------------------------------------------')
    print('[+]  \033[34mGithub : https://github.com/crow821/                                \033[0m')
    print('[+]  \033[34m公众号 : 乌鸦安全(crowsec)                                                \033[0m')

    print('[+]  \033[34m功  能: 久草cms V1.9弱口令检测                        \033[0m')
    print('[+]  \033[34m注  意:仅供个人本地验证，禁止用于非法用途，请严格遵守网络安全法!!!           \033[0m')
    print('[+]  \033[34m注  意:仅限在本地自行测试，禁止用于非授权测试！！！                    \033[0m')
    print('[+]  \033[34m注  意:仅限在本地自行测试，禁止用于非授权测试！！！                    \033[0m')
    print('[+]  \033[34m注  意:仅限在本地自行测试，禁止用于非授权测试！！！                    \033[0m')
    print('[+]  \033[36m使用格式:  python3 jiucaocmsV1.9_check.py                        \033[0m')
    print('+------------------------------------------')

title()


def user_agent():
    
    user_agent_list = [
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 ',
             'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
             'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrow 20 ser/2.0 Safari/536.11',
             'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET',
             'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
         ]
    return random.choice(user_agent_list)



class Check_vuls(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):
        while not self._queue.empty():
            Ip = self._queue.get()
            print('[info] current left ', self._queue.qsize())
            try:
                self.Confluence_command(Ip)
            except Exception as e:
                pass
    def Confluence_command(self,host):
        if host:
                print("-"*50)
                if 'http' not in host[:-1]:
                    check_url = 'http://' + host
                else:
                    check_url = str(host)
             
        payload = ['/adminx/', '/adminz/']
        for i in range(0,2):
            deal_check_url = check_url + payload[i]
            print('此时需要检测的', deal_check_url)
            res_command = requests.get(url=deal_check_url, verify=False, timeout=5, headers={'User-Agent': user_agent()},allow_redirects=True)
            try:
                if res_command.status_code == 200 and "当前使用的是默认账号" in res_command.text:
                    print('[+] info\033[31m ' + check_url + '\033[0m') 
                    with open('vuls.txt', 'a+') as ff:
                        ff.write(deal_check_url + "\n")
                else:
                    print("[-] info: This is link is not vulnerable.")
            except Exception as e:
                print("[-] info: This link is not vulnerable")


def check_vuls():
    queue = Queue()
    with open('urls.txt', 'r') as f:
        for line in f.readlines():
            
            print('还未进入队列的url', line.strip())
            queue.put(line.strip())
        print('[+] Loading complite')
        threads = []
        thread_counts = 20  # 定义线程
        for i in range(thread_counts):
            threads.append(Check_vuls(queue))
        for t in threads:
            t.start()
        for t in threads:
            t.join()


if __name__ == '__main__':

    check_vuls()