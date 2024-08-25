"""
此信息需要保留！

作者:zzXiaoZhu
github主页:https://github.com/zzXiaoZhu
仓库地址:https://github.com/zzXiaoZhu/five-in-a-row_byJuniorXZ/
项目开发于2022年

"""


ServerPost = 33909


import threading
import socket
import time

# 完成是否关闭连接
Close = True

RoomNameList = []
RoomChessBoardCommandList = []
RoomFullBoolList = []

# 回复信息
NewDone = "SuccessNewRoom"

# 建立连接
Tcplink = socket.socket()
Tcplink.bind(("", ServerPost))
Tcplink.listen(5)


# 服务程序
def Server():
    global RoomNameList
    global RoomChessBoardCommandList
    global RoomFullBoolList
    while True:
        try:  # 防崩溃
            if Close:
                UserConnect, UserIp = Tcplink.accept()
            UserRequest = UserConnect.recv(2048)

            # 新房间
            if "NewRoom:" in str(UserRequest, encoding="UTF-8"):
                UserRequest = str(UserRequest, encoding="UTF-8").split(":")
                UserConnect.sendall(str(len(RoomNameList)).encode())
                RoomNameList.append(UserRequest[1])
                RoomChessBoardCommandList.append("None")
                RoomFullBoolList.append(False)

            # 关闭房间
            elif "KillRoom:" in str(UserRequest, encoding="UTF-8"):
                UserRequest = str(UserRequest, encoding="UTF-8").split(":")
                Temp = RoomNameList.index(UserRequest[1])
                del RoomNameList[Temp]
                del RoomChessBoardCommandList[Temp]
                del RoomFullBoolList[Temp]

            # 退出房间
            elif "ExitRoom:" in str(UserRequest, encoding="UTF-8"):
                UserRequest = str(UserRequest, encoding="UTF-8").split(":")
                Temp = RoomNameList.index(UserRequest[1])
                RoomFullBoolList[Temp] = False

            # 加入房间
            elif "JoinRoom:" in str(UserRequest, encoding="UTF-8"):
                UserRequest = str(UserRequest, encoding="UTF-8").split(":")
                Temp = UserRequest[1].split(" ")
                # 房间被关闭
                if len(RoomNameList) == 0 or Temp[1] != RoomNameList[int(Temp[0])]:
                    UserConnect.sendall("Error_1".encode())
                # 满员
                elif RoomFullBoolList[int(Temp[0])]:
                    UserConnect.sendall("Error_2".encode())
                # 正常加入
                else:
                    UserConnect.sendall("Success".encode())
                    RoomFullBoolList[int(Temp[0])] = True

            # 获得房间列表
            elif str(UserRequest, encoding="UTF-8") == "GetRoomList":
                # 打包
                TempText = ""
                for i in RoomNameList:
                    TempText += i
                    TempText += "|"
                if not len(TempText) == 0:
                    TempText = TempText[0:len(TempText) - 1]
                UserConnect.sendall(str(len(TempText)).encode())
                time.sleep(1)
                UserConnect.sendall(TempText.encode())
                UserConnect.close()

            # 上传
            elif "UploadBoard:" in str(UserRequest, encoding="UTF-8"):
                Temp = str(UserRequest, encoding="UTF-8").split(":")
                TempIndex = RoomNameList.index(Temp[1])
                RoomChessBoardCommandList[TempIndex] = str(UserRequest, encoding="UTF-8")

            # 下载
            elif "DownloadBoard" in str(UserRequest, encoding="UTF-8"):
                Temp = str(UserRequest, encoding="UTF-8").split(":")
                if Temp[1] in RoomNameList:
                    TempIndex = RoomNameList.index(Temp[1])
                    Temp1 = RoomChessBoardCommandList[TempIndex]
                    Temp1 = Temp1.split(":")
                    # 游客退出发送全清
                    if not RoomFullBoolList[TempIndex]:
                        UserConnect.sendall("AllClean".encode())
                    elif Temp1[-1] == "1":  # 上次由房主传入（游客下载）
                        if Temp[2] == "False":
                            UserConnect.sendall(RoomChessBoardCommandList[TempIndex].encode())
                        else:
                            UserConnect.sendall("None".encode())
                    elif Temp1[-1] == "2":  # 上次由游客传入(房主下载)
                        if Temp[2] == "True":
                            UserConnect.sendall(RoomChessBoardCommandList[TempIndex].encode())
                        else:
                            UserConnect.sendall("None".encode())
                    else:
                        UserConnect.sendall("None".encode())
                # 房间被关闭
                else:
                    UserConnect.sendall("Error_1".encode())


            if Close:
                UserConnect.close()
        except:
            pass


# 拿出50个线程跑服务器
for i in range(50):
    threading.Thread(target=Server).start()
