# -*- coding: utf-8 -*-
# by crow 2020-09-28
# 批量测试的时候： fofa/shodan -->ip地址-->验证ip是否存在某个漏洞：poc/exp-->验证该站的反查域名-->域名反查权重-->补天 >1 , 漏洞盒子  gov,edu
#  fofa  100--> 50 --> 20 --> 5
# 测试的站点： 爱站 中国站长
import re, requests
from fake_useragent import UserAgent


ua = UserAgent()

def domain_level(domain):
    # https://www.aizhan.com/cha/www.crowsec.cn/
    url = 'https://www.aizhan.com/cha/' + str(domain) + '/'
    domain_r = requests.get(url=url, headers={'User-Agent': ua.random}, timeout=10).text
    '''
     百度权重： <img src="//statics.aizhan.com/images/br/1.png" alt="1">
     #        <img src="//statics.aizhan.com/images/br/0.png" alt="0">
     移动权重   <img src="//statics.aizhan.com/images/mbr/0.png" alt="0">
     360权重   <img src="//statics.aizhan.com/images/360/0.png" alt="0">
     搜狗权重   <img src="//statics.aizhan.com/images/sr/1.png" alt="1">
     神马权重   <img src="//statics.aizhan.com/images/sm/0.png" alt="0">
     谷歌权重   <img src="//statics.aizhan.com/images/pr/7.png" alt="7">
    '''
    # 百度权重
    baidu_rank = re.findall(r'<img src="//statics.aizhan.com/images/br/(.*?).png', domain_r)
    # 百度移动权重
    baidu_rank_mbr = re.findall(r'<img src="//statics.aizhan.com/images/mbr/(.*?).png', domain_r)
    # 360权重
    san_360_rank= re.findall(r'<img src="//statics.aizhan.com/images/360/(.*?).png', domain_r)
    # 搜狗权重
    sougou_rank = re.findall(r'<img src="//statics.aizhan.com/images/sr/(.*?).png', domain_r)
    # 神马权重
    sm_rank = re.findall(r'<img src="//statics.aizhan.com/images/sm/(.*?).png', domain_r)
    # 谷歌权重
    google_rank= re.findall(r'<img src="//statics.aizhan.com/images/pr/(.*?).png', domain_r)
    # print(baidu_rank[1])
    print('百度权重：{}'.format(baidu_rank[0]))
    print('百度移动权重：{}'.format(baidu_rank_mbr[0]))
    print('360权重：{}'.format(san_360_rank[0]))
    print('搜狗权重：{}'.format(sougou_rank[0]))
    print('神马权重：{}'.format(sm_rank[0]))
    print('谷歌权重：{}'.format(google_rank[0]))

if __name__ == '__main__':
    # domain = 'www.crowsec.cn'
    # domain = 'www.butian.net'
    domain = 'www.google.com'
    domain_level(domain)



