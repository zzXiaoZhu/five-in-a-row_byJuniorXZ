"""
此信息需要保留！

作者:zzXiaoZhu
github主页:https://github.com/zzXiaoZhu
仓库地址:https://github.com/zzXiaoZhu/five-in-a-row_byJuniorXZ/
项目开发于2022年

"""

ServerHost = "127.0.0.1"
ServerPost = 33909

import socket

while True:
        UserInput = input("输入房间名:")
        Link = socket.socket()
        Link.connect((ServerHost, ServerPost))
        Link.send("KillRoom:{}".format(UserInput).encode())
        Link.close()

        print("指令已发送")
