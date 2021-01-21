# -*- coding: utf-8 -*-
# by crow   2020-09-21
import re, time, requests
from fake_useragent import UserAgent


ua = UserAgent()
# 如果遇到报错ssl证书833的情况，请使用以下
# ua = UserAgent(verify_ssl=False)

# ip138
headers_ip138 = {
    'Host': 'site.ip138.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://site.ip138.com/'}
# 爱站
headers_aizhan = {
    'Host': 'dns.aizhan.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://dns.aizhan.com/'}
# 中国站长
headers_chinaz = {
    'Host': 's.tool.chinaz.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    }  # 站长这边删除了一个referer

def ip138_spider(ip):
    ip138_url = 'https://site.ip138.com/' + str(ip) + '/'
    ip138_r = requests.get(url=ip138_url, headers=headers_ip138, timeout=3).text
    ip138_address = re.findall(r"<h3>(.*?)</h3>", ip138_r)   # 归属地
    # result = re.findall(r"<li>(.*?)</li>", ip138_r)
    if '<li>暂无结果</li>' in ip138_r:
        print('[+]ip:{}'.format(ip))
        print('归属地：{}'.format(ip138_address[0]))
        print('未查到相关绑定信息！')
    else:
        print('[+]ip:{}'.format(ip))
        print('归属地：{}'.format(ip138_address[0]))
        result_time = re.findall(r"""class="date">(.*?)</span>""", ip138_r)  # 绑定时间
        result_site = re.findall(r"""</span><a href="/(.*?)/" target="_blank">""", ip138_r)  # 绑定域名结果
        print('绑定信息如下：')
        for i, j in enumerate(result_time):
            print('{}-----{}'.format(j, result_site[i]))
    print('-'*25)




def chinaz_spider(ip):
    chinaz_url = 'http://s.tool.chinaz.com/same?s=' + str(ip) + '&page='
    chinaz_re = requests.get(chinaz_url, headers=headers_chinaz).text
    # print(chinaz_re)
    if '没有找到任何站点' in chinaz_re:
        print('没有找到任何站点')
    else:
        chinaz_nums = re.findall(r'''<i class="col-blue02">(.*?)</i>''', chinaz_re)  # 获得一共解析了多少个站点
        print('[+]一共解析了{}个ip地址'.format(chinaz_nums[0]))
        if int(chinaz_nums[0]) > 20:
            pages = (int(chinaz_nums[0]) % 20) + (int(chinaz_nums[0]) // 20)
            for page in range(1, pages+1):
                chinaz_page_url = chinaz_url + str(page)
                # print(chinaz_page_url)
                chinaz_page_r = requests.get(url=chinaz_page_url, headers=headers_chinaz, timeout=2).text
                # print(chinaz_page_r)
                # 取出该ip曾经解析过多少个域名
                chinaz_domains = re.findall(r'''\'\)\" target=_blank>(.*?)</a>''', chinaz_page_r)
                # print(chinaz_domains)
                # print(len(aizhan_domains))
                for chinaz_domain in chinaz_domains:
                    print(chinaz_domain)
                time.sleep(0.5)
        else:
            chinaz_address = re.findall(r'''\[(.*?)\]</a>''', chinaz_re)  # 获得域名地址
            print('[+]位于：{}'.format(chinaz_address[0]))
            chinaz_domains = re.findall(r'''\'\)\" target=_blank>(.*?)</a>''', chinaz_re)
            # print(chinaz_domains)
            for chinaz_domain in chinaz_domains:
                print(chinaz_domain)


def aizhan_spider(ip):
    aizhan_url = 'https://dns.aizhan.com/' + str(ip) + '/'
    aizhan_r = requests.get(url=aizhan_url, headers=headers_aizhan, timeout=2).text
    # print(aizhan_r)
    #  1. 取出该地址的真实地址
    aizhan_address = re.findall(r'''<strong>(.*?)</strong>''',  aizhan_r)
    # print(aizhan_address)
    # <strong>中国浙江</strong>
    print('[+]归属地：{}'.format(aizhan_address[0]))
    #  2. 取出该ip的解析过多少个域名
    aizhan_nums = re.findall(r'''<span class="red">(.*?)</span>''', aizhan_r)
    print('[+]该ip一共解析了：{}个域名'.format(aizhan_nums[0]))
    if int(aizhan_nums[0]) > 0:
        if int(aizhan_nums[0]) > 20:
            # 计算多少页
            pages = (int(aizhan_nums[0]) % 20) + (int(aizhan_nums[0]) // 20)
            # print('该ip一共解析了{}页'.format(pages))
            for page in range(1, pages+1):
                aizhan_page_url = aizhan_url + str(page) + '/'
                # print(aizhan_page_url)
                aizhan_page_r = requests.get(url=aizhan_page_url, headers=headers_aizhan, timeout=2).text
                # 取出该ip曾经解析过多少个域名
                aizhan_domains = re.findall(r'''rel="nofollow" target="_blank">(.*?)</a>''', aizhan_page_r)
                # print(aizhan_domains)
                # print(len(aizhan_domains))
                for aizhan_domain in aizhan_domains:
                    print(aizhan_domain)
                time.sleep(0.5)
        else:
            # 取出该ip曾经解析过多少个域名
            aizhan_domains = re.findall(r'''rel="nofollow" target="_blank">(.*?)</a>''', aizhan_r)
            # print(aizhan_domains)
            # print(len(aizhan_domains))
            for aizhan_domain in aizhan_domains:
                print(aizhan_domain)
    else:
        print('共有0个域名解析到该IP')








if __name__ == '__main__':
    ip = '220.181.38.148'
    # ip = '61.136.101.79'
    ip138_spider(ip)
    aizhan_spider(ip)
    chinaz_spider(ip)