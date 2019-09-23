net user 
net user crow2 123 /add
net localgroup administrators crow2 /add
net user 
msg crow "我已经创建了一个新的用户"
shutdown /s /t 500 /c "系统将在5min之后关闭"