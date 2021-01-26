# -*- coding: utf-8 -*-
"""
脚本是在python3下运行的
需要提前输入你的session值
以及你的key信息
"""

import requests
import base64
import re
import time
import sys
import urllib.parse
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


requests.packages.urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.40',
    'Cookie': '_fofapro_ars_session=3efdc87b14ec67721e9440dfb273fd77'  # 请输入你的session
}


def get_page(key):
    key_base64 = base64.b64encode(key.encode('utf-8')).decode()
    key_base64 = urllib.parse.quote(key_base64)
    url = f'https://fofa.so/result?page=1&qbase64={key_base64}'
    r = requests.get(url=url, headers=headers, verify=False)
    html = r.text
    response = HtmlResponse(html, body=html, encoding='utf-8')
    selector = Selector(response=response)
    for i in [7, 6, 5, 4, 3, 2, 1]:
        path_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[11]/div[2]/a[{i}])'
        page = selector.xpath(path_xpath).extract()
        page = " ".join(page)
        if page:
            break
    if not page:
        page = 1
    return page


def get_url(key, count):
    key_base64 = base64.b64encode(key.encode('utf-8')).decode()
    key_base64 = urllib.parse.quote(key_base64)
    scanurl = f'https://fofa.so/result?page={count}&qbase64={key_base64}'
    return scanurl


def get_data(xpath):
    result = selector.xpath(xpath).extract()
    data = " ".join(result)
    return data


def scan(target, host_lists):
    global count, page_count, selector
    host = ''
    count += 1
    leave_count = page_count - count - 1
    print(f'这是第{count}页的内容，还有{leave_count}页的内容：')
    result = ''
    r = requests.get(url=target, headers=headers, verify=False)
    if headers['Cookie'] in str(r.cookies):
        result = True
    html = r.text
    if '出错了' in html:
        print(html)
        print('某个地方出现了问题，请查看html代码')
        sys.exit()
    response = HtmlResponse(html, body=html, encoding='utf-8')
    selector = Selector(response=response)
    if result:
        for i in range(1, 11):
            for j in range(1, 3):
                host_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[{i}]/div[1]/div[1]/a[{j}])'
                host_result = get_data(host_xpath)
                if host_result:
                    host = host_result
            port_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[{i}]/div[2]/div[1]/a)'
            title_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[{i}]/div[1]/div[2])'
            header_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[{i}]/div[2]/div[2]/div/div[1])'
            certificate_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[{i}]/div[2]/div[4])'
            server_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[{i}]/div[1]/div[8]/a)'
            isp_xpath = f'normalize-space(/html/body/div[1]/div[6]/div[1]/div[2]/div[{i}]/div[1]/div[6]/a)'
            port = get_data(port_xpath)
            title = get_data(title_xpath)
            header = get_data(header_xpath)
            certificate = get_data(certificate_xpath)
            server = get_data(server_xpath)
            isp = get_data(isp_xpath)
            if port:
                port = int(port)
            ssl_domain = re.findall(r'(?<=CommonName: ).*(?=Subject Public)', certificate)
            ssl_domain = " ".join(ssl_domain).strip()
            language = re.findall(r'(?<=X-Powered-By: ).*(?=)', header)
            language = " ".join(language).strip()
            if 'PHPSESSID' in header and language == '':
                language = 'php'
            elif 'JSESSIONID' in header and language == '':
                language = 'jsp'
            try:
                ssl_domain = ssl_domain.split(' CommonName: ')[1]
            except:
                ssl_domain = ''
            if not ssl_domain and 'domain=' in header:
                ssl_domain = re.findall(r'(?<=domain=).*(?=;)', header)
                ssl_domain = " ".join(ssl_domain).strip()
                ssl_domain = ssl_domain.split(';')[0]
            try:
                status = int(header.split(' ')[1].strip())
                if status not in [200, 301, 302, 303, 304, 307, 400, 401, 403, 404, 405, 407,
                                  500, 501, 502, 503, 504, 508]:
                    status = ''
            except:
                status = ''
            if port == '' and status == '' and isp == '' and title == '':
                host = ''
                # print(f'{host}')
            print('host', host)
            host_lists.append(host)
            # print(f'{host} {port} {status} {ssl_domain} {language} {server} {title}')
            # print(certificate)
            # print(header)
    else:
        print('cookie无效，请重新获取cookie')


def main():
    host_lists = []
    global count, page_count
    count = 0
    key = 'port="8009" && protocol=="ajp"'
    page_count = get_page(key)
    page_count = int(page_count) + 1
    for page in range(1, page_count):
        url = get_url(key, page)
        print(url)
        scan(url, host_lists)
        time.sleep(6)

    with open('host_ip.txt', 'a+') as f:
        for host_list in host_lists:
            if 'http://' not in str(host_list) and 'https://' not in str(host_list):
                host_ = 'http://' + str(host_list)
                f.write(str(host_) + '\n')
                print(host_)
            else:
                f.write(str(host_list) + '\n')
                print(host_list)


if __name__ == '__main__':
    main()
