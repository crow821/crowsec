# -*- encoding: utf-8 -*-
# Time : 2021/08/30 22:10:54
# Author: crow
# 微信公众号：乌鸦安全

import re 
new_md = []


def title():
    print('+------------------------------------------')
    print('[+]  \033[34mGithub : https://github.com/crow821/                                \033[0m')
    print('[+]  \033[34m公众号 : 乌鸦安全                                                     \033[0m')
    print('[+]  \033[34m功  能: 语雀文档导出md文件后图片修复                                   \033[0m')
    print('[+]  \033[36m使用格式:  python3 deal_yuque.py                                     \033[0m')
    print('+------------------------------------------')


def deal_yuque(new_md,old_path):
    
    with open(old_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            line = re.sub(r'png#(.*)+', 'png)', line)
            # print(line)
            new_md.append(line)
            

    with open(new_path, 'w',encoding='utf-8', errors='ignore') as f:
        for new_md in new_md:
            f.write(str(new_md))


if __name__ == '__main__':
    title()
    print('[+]  \033[36m请输入您的文件路径, 如：乌鸦安全.md\033[0m')
    old_path = input('[+]  \033[35m路径：\033[0m')
    new_path = 'new_' + old_path
    deal_yuque(new_md, old_path)  
    print('[+]  \033[36m修复完成，图片修复后文件路径:\033[0m', new_path)