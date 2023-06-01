# -*- encoding: utf-8 -*-
# Time: 2023/01/23 10:49:37
# Author: crow 
# 微信公众号：乌鸦安全
# 使用须知：请务必遵守网络安全法规！


import hashlib

def encrypt_password(password):
    salt = 'xxxxx'  # 替换为你自己的盐值
    hashed_password = hashlib.md5(hashlib.md5(hashlib.md5(password.encode()).hexdigest().encode() + '_bt.cn'.encode()).hexdigest().encode() + salt.encode()).hexdigest()
    return hashed_password

# 示例用法
password = 'admin'
encrypted_password = encrypt_password(password)
print(encrypted_password)
