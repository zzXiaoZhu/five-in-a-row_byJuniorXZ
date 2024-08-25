"""
此信息需要保留！

作者:zzXiaoZhu
github主页:https://github.com/zzXiaoZhu
仓库地址:https://github.com/zzXiaoZhu/five-in-a-row_byJuniorXZ/
项目开发于2022年

"""



import time
import socket
import tkinter
import pygame
import threading
import subprocess
import tkinter.messagebox
import sys

pygame.init()

# 是否为房主
RoomHost = False

# 模式(0单机,1联机)和服务器域名与端口
# 为啥这么写呢，因为可以直接if判断，嘿嘿
Mode = None

# Server信息 Host为ip或域名，Post为端口号
ServerHost = "127.0.0.1"
ServerPost = 33909

Fps = 60  # 帧率
Clock = pygame.time.Clock()

# 本轮玩家(1为黑，2为白)
ThisRound = 1

# 颜色
ButtonTextColor = (147, 112, 219)
TextColor = (138, 43, 226)

# 棋盘
ChessBoard = []

# 单个左上点坐标
Left_Up = []
for i in range(15):
    TempList = []
    for r in range(15):
        TempList.append((40 * r, 40 * i))
    Left_Up.append(TempList)

# 单个右下点坐标
Right_Down = []
for i in range(15):
    i += 1
    TempList = []
    for r in range(15):
        r += 1
        TempList.append((40 * r, 40 * i))
    Right_Down.append(TempList)
del TempList


# 清空棋盘
def CleanBoard():
    global ChessBoard
    global ThisRound
    ThisRound = 1
    ChessBoard = [[0 for _ in range(15)] for _ in range(15)]


# 退出程序
def Exit():
    try:
        # 退出前先关闭房间
        if Mode:
            if RoomHost:
                Tcplink = socket.socket()
                Tcplink.connect((ServerHost, ServerPost))
                Tcplink.send("KillRoom:{}".format(RoomList[RoomSerialNumber]).encode())
                Tcplink.close()
            else:
                Tcplink = socket.socket()
                Tcplink.connect((ServerHost, ServerPost))
                Tcplink.send("ExitRoom:{}".format(RoomList[RoomSerialNumber]).encode())
                Tcplink.close()
    except:
        pass
    sys.exit()
    exit()


# 获得事件
def GetEvent():
    Event = pygame.event.get()
    for event in Event:
        if event.type == pygame.QUIT:
            Exit()
    return Event


# 赢了的消息框
def WinMsgBox(WinUser):
    if WinUser == 2:
        tkinter.messagebox.showinfo("赢了", "白棋赢了")
        CleanBoard()
    elif WinUser == 1:
        tkinter.messagebox.showinfo("赢了", "黑棋赢了")
        CleanBoard()


# 素材路径
FilePath = "Files\\"

# 创建窗口
pygame.display.set_caption("五子棋")
pygame.display.set_icon(pygame.image.load("{}logo.ico".format(FilePath)))
sc = pygame.display.set_mode((600, 600))
tk = tkinter.Tk()
tk.iconbitmap("{}\logo.ico".format(FilePath))
tk.withdraw()

# 加载图片和文字
GameFont = pygame.font.Font("{}Misans.ttf".format(FilePath), 20)
BackgroundImage = pygame.image.load("{}Background.jpg".format(FilePath))
WhiteButton = pygame.image.load("{}WhiteButton.png".format(FilePath))
BlackButton = pygame.image.load("{}BlackButton.png".format(FilePath))
ChessBoardImage = pygame.image.load("{}Board.png".format(FilePath))
White = pygame.image.load("{}White.png".format(FilePath))
Black = pygame.image.load("{}Black.png".format(FilePath))


# 按钮
def Button(XY, Word, Event, TextColor, ButtonImage, Font):
    sc.blit(ButtonImage, (XY[0], XY[1]))
    WordLen = len(Word)
    Word = Font.render(Word, True, TextColor)
    sc.blit(Word, (XY[0] + 50 - Word.get_size()[0] / 2, XY[1] + 40))
    MousePos = pygame.mouse.get_pos()
    for event in Event:
        if XY[0] < MousePos[0] < XY[0] + 100 and XY[1] < MousePos[1] < XY[1] + 100:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True


# 玩法选择按钮位置
ModeButtonX = (250, 250)
ModeButtonY = (100, 350)

# 文字内容
ModeButtonWord = ("单机双人", "联机双人")

# 模式选择进入动画
for i in range(130):
    if i > 115:
        i = i - 115
        i = 115 - i
    sc.blit(BackgroundImage, (0, 0))
    event = pygame.event.get()
    Button(XY=(ModeButtonX[0], ModeButtonY[0] * i / 100),
           Word=ModeButtonWord[0][0:int(len(ModeButtonWord[0]) * i / 100 // 1)], Event=event,
           TextColor=ButtonTextColor, ButtonImage=WhiteButton, Font=GameFont)
    Button(XY=(ModeButtonX[1], ModeButtonY[1] * i / 100),
           Word=ModeButtonWord[1][0:int(len(ModeButtonWord[1]) * i / 100 // 1)], Event=event,
           TextColor=ButtonTextColor, ButtonImage=BlackButton, Font=GameFont)
    pygame.display.update()
    time.sleep(0.003)

# 模式选择
while True:
    Clock.tick(Fps)  # 限制帧率
    event = GetEvent()
    sc.blit(BackgroundImage, (0, 0))
    # 单机模式
    if Button(XY=(ModeButtonX[0], ModeButtonY[0]), Word=ModeButtonWord[0], Event=event, TextColor=ButtonTextColor,
              ButtonImage=WhiteButton, Font=GameFont):
        Mode = 0
        break
    # 联机模式
    elif Button(XY=(ModeButtonX[1], ModeButtonY[1]), Word=ModeButtonWord[1], Event=event, TextColor=ButtonTextColor,
                ButtonImage=BlackButton, Font=GameFont):
        Mode = 1
        break
    pygame.display.update()

# 模式选择退出动画
for i in range(100):
    i = 100 - i
    sc.blit(BackgroundImage, (0, 0))
    event = pygame.event.get()
    Button(XY=(ModeButtonX[0], ModeButtonY[0] * i / 100),
           Word=ModeButtonWord[0][0:int(len(ModeButtonWord[0]) * i / 100 // 1)], Event=event,
           TextColor=ButtonTextColor, ButtonImage=WhiteButton, Font=GameFont)
    Button(XY=(ModeButtonX[1], ModeButtonY[1] * i / 100),
           Word=ModeButtonWord[1][0:int(len(ModeButtonWord[1]) * i / 100 // 1)], Event=event,
           TextColor=ButtonTextColor, ButtonImage=BlackButton, Font=GameFont)
    pygame.display.update()
    time.sleep(0.003)

# 彻底让最上层按钮走出屏幕
for i in range(100):
    sc.blit(BackgroundImage, (0, 0))
    Button(XY=(ModeButtonX[1], -i),
           Word="", Event=event,
           TextColor=ButtonTextColor, ButtonImage=BlackButton, Font=GameFont)
    pygame.display.update()
    time.sleep(0.001)

# 联机与服务器通信并生成房间列表
if Mode:
    # 向用户展示信息
    sc.blit(GameFont.render("正在尝试连接服务器......", True, TextColor), (200, 250))
    pygame.display.update()


    def GetRoomList():
        global RoomList
        global RoomNum


        
        try:
            # 建立链接
            Tcplink = socket.socket()
            Tcplink.connect((ServerHost, ServerPost))

            # 获取房间列表
            Tcplink.send("GetRoomList".encode())  # 向服务器申请
            RoomLen = int(str(Tcplink.recv(102400), encoding="UTF-8"))  # 获取房间信息长度

            # 获取房间名、生成列表
            RoomList = []
            if RoomLen != 0:
                TempText = ""
                while len(TempText) != RoomLen:
                    TempText += str(Tcplink.recv(102400), encoding="UTF-8")
                Tcplink.close()
                RoomList = TempText.split("|")
            RoomNum = len(RoomList)
            RoomList.append("创建新房间")
        except:
            tkinter.messagebox.showerror("错误", "与服务器通信时出现问题")
            Exit()
        


    # 显示按钮和背景
    def TempShowButton():
        global PressKey
        global CanDown
        global TempButtonX
        sc.blit(BackgroundImage, (0, 0))
        TempButtonY = AllRoomButtonY
        TempButtonX = 0
        PressKey = None
        CanDown = False
        try:
            for i in range(RoomNum + 1):
                if TempButtonY >= 600:
                    CanDown = True
                if Button(XY=(TempButtonX, TempButtonY), Word=RoomList[i], Event=event, TextColor=ButtonTextColor,
                          ButtonImage=RoomButtonImageModeList[i], Font=GameFont):
                    PressKey = i
                TempButtonX += 125
                if TempButtonX >= 600:
                    TempButtonX = 0
                    TempButtonY += 125
        except:
            pass
        pygame.display.update()


    # 新建房间
    def NewRoom():
        global RoomSerialNumber
        global TempBool
        global RoomHost
        global RoomNum
        global BreakBool
        # 获取输入内容
        RoomName = NewRoomEntry.get()
        # 判定输入内容
        if len(RoomName) == 0 or RoomName in RoomList:
            tkinter.messagebox.showinfo("提示信息", "空名称或名称重复")
        elif "|" in RoomName:
            tkinter.messagebox.showinfo("提示信息", "名称内含有禁用的字符")
        else:
            try:
                # 把信息发送至服务器并接受房间编号
                SendRequest = "NewRoom:" + RoomName
                Tcplink = socket.socket()
                Tcplink.connect((ServerHost, ServerPost))
                Tcplink.send(SendRequest.encode())
                RoomSerialNumber = int(str(Tcplink.recv(1024), encoding="UTF-8"))
                Tcplink.close()
            except:
                tkinter.messagebox.showerror("错误", "与服务器通信时出现问题")
                Exit()
            # 把新房间加入列表
            TempBool = False
            tk.withdraw()
            del RoomList[-1]
            RoomList.append(RoomName)
            RoomList.append("创建新房间")
            RoomNum += 1
            RoomButtonImage()
            # 确认用户为房主并跳出循环
            RoomHost = True
            BreakBool = True


    def RoomButtonImage():
        global RoomButtonImageModeList
        # 显示列表
        RoomButtonImageModeList = []  # 按钮样式列表
        Temp = BlackButton
        for i in range(RoomNum + 1):
            RoomButtonImageModeList.append(Temp)
            if Temp == BlackButton:
                Temp = WhiteButton
            else:
                Temp = BlackButton
        del Temp


    GetRoomList()
    RoomButtonImage()

    AllRoomButtonY = 0
    Space = 25
    time1 = time.time()
    while True:
        Clock.tick(Fps)  # 限制帧率

        # 刷新房间列表
        if time.time() - time1 > 60:
            time1 = time.time()
            GetListThread = threading.Thread(target=GetRoomList)
            GetListThread.start()
            RoomButtonImage()
        # 获得事件、显示背景\按钮
        event = GetEvent()
        TempShowButton()

        # 下滑列表
        if CanDown or AllRoomButtonY < 0:
            for e in event:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN and CanDown:
                        Temp = AllRoomButtonY - 125
                        # 下滑动画
                        for i in range(125):
                            AllRoomButtonY -= 1
                            TempShowButton()
                        AllRoomButtonY = Temp
                    elif e.key == pygame.K_UP and AllRoomButtonY < 0:
                        Temp = AllRoomButtonY + + 125
                        # 下滑动画
                        for i in range(125):
                            AllRoomButtonY += 1
                            TempShowButton()
                        AllRoomButtonY = Temp

        # 按钮
        if PressKey is not None:
            # 创建新房间按钮
            if PressKey == len(RoomList) - 1:
                tk.destroy()  # 销毁之前的窗口
                # 创建新窗口
                tk = tkinter.Tk()
                tk.title("创建新房间")
                tk.geometry("240x100")
                tk.iconbitmap("{}logo.ico".format(FilePath))
                tk.resizable(0, 0)


                # 关闭窗口
                def offwindow():
                    global TempBool
                    TempBool = False
                    tk.withdraw()


                tk.protocol('WM_DELETE_WINDOW', offwindow)

                # 按钮
                UpLoadButton = tkinter.Button(tk, text="确认创建", command=NewRoom)
                UpLoadButton.place(x=90, y=50)
                # 提示信息
                TextLabel = tkinter.Label(tk, text="输入房间名")
                TextLabel.place(x=40, y=0)
                # 输入框
                NewRoomEntry = tkinter.Entry(tk, text="输入房间名")
                NewRoomEntry.place(x=40, y=20)
                # 更新小窗口
                TempBool = True
                BreakBool = False
                while TempBool:
                    tk.update()
                if BreakBool:
                    break
            else:
                try:
                    # 建立连接
                    Tcplink = socket.socket()
                    Tcplink.connect((ServerHost, ServerPost))
                    Tcplink.send("JoinRoom:{} {}".format(str(PressKey), RoomList[PressKey]).encode())
                    ReturnCode = str(Tcplink.recv(1024), encoding="UTF-8")
                    Tcplink.close()
                except:
                    tkinter.messagebox.showerror("错误", "与服务器通信时出现问题")
                    Exit()
                if ReturnCode == "Success":
                    RoomSerialNumber = PressKey
                    break
                elif ReturnCode == "Error_1":
                    tkinter.messagebox.showerror("五子棋", "房间被关闭")
                    Exit()
                elif ReturnCode == "Error_2":
                    tkinter.messagebox.showerror("五子棋", "房间人数已满")
                    Exit()

# 显示棋盘
for i in range(8, 255, 8):
    sc.blit(pygame.image.load("{}BoardFrame\\BoardFrame{}.png".format(FilePath, i)), (0, 0))
    pygame.display.update()
    time.sleep(0.02)
for i in range(248, 8, -8):
    sc.blit(ChessBoardImage, (0, 0))
    sc.blit(pygame.image.load("{}BoardFrame\\BoardFrame{}.png".format(FilePath, i)), (0, 0))
    pygame.display.update()
    time.sleep(0.0001)

# 定义上传和下载函数
if Mode:
    def UploadBoard(TempInput1, TempInput2, TempInput3):
        try:
            Tcplink = socket.socket()
            Tcplink.connect((ServerHost, ServerPost))
            # UploadBoard:{房间名}:{行}:{列}:{修改值}
            Tcplink.send("UploadBoard:{}:{}:{}:{}".format(RoomList[RoomSerialNumber], TempInput1, TempInput2,
                                                          TempInput3).encode())
            Tcplink.close()
        except:
            pass


    def DownloadBoard():
        global ChessBoard
        global ThisRound
        # 获得指令
        try:
            Tcplink = socket.socket()
            Tcplink.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1000)
            Tcplink.connect((ServerHost, ServerPost))
            Tcplink.send("DownloadBoard:{}:{}".format(RoomList[RoomSerialNumber], str(RoomHost)).encode())
            TempReturn = str(Tcplink.recv(1024), encoding="UTF-8")
            # 房间被关闭
            if TempReturn == "Error_1":
                tkinter.messagebox.showinfo("信息", "房间已被关闭")
                Exit()
            # 玩家退出游戏后清盘
            elif TempReturn == "AllClean":
                CleanBoard()
            # 解析服务器返回指令
            elif "None" not in TempReturn:
                TempReturn = TempReturn.split(":")
                # 删除服务器的定位信息
                del TempReturn[0]
                del TempReturn[0]
                # 把信息转化为数字并生成列表（前两个为索引，第三个为修改内容）
                TempIndexList = [int(TempReturn[0]), int(TempReturn[1]), int(TempReturn[2])]
                # 修改棋盘
                ChessBoard[TempIndexList[0]][TempIndexList[1]] = int(TempReturn[2])
                ShowBoard()

                # 修改本轮玩家
                if ThisRound == 1:
                    ThisRound = 2
                else:
                    ThisRound = 1
        except:
            pass


# 显示棋子
def ShowBoard():
    Indexi = 0
    for i in ChessBoard:
        Indexj = 0
        for j in i:
            if j == 2:
                sc.blit(White, (Left_Up[Indexi][Indexj][0], Left_Up[Indexi][Indexj][1]))
            elif j == 1:
                sc.blit(Black, (Left_Up[Indexi][Indexj][0], Left_Up[Indexi][Indexj][1]))
            Indexj += 1
        Indexi += 1
    pygame.display.update()


# 游戏功能
CleanBoard()
time1 = time.time()
while True:
    Clock.tick(Fps)  # 限制帧率
    event = GetEvent()
    Mouse_pos = pygame.mouse.get_pos()
    sc.blit(ChessBoardImage, (0, 0))

    if Mode:
        # 下载棋盘（1秒一次）
        if time.time() - time1 > 1:
            if (RoomHost and not ThisRound == 1) or (not RoomHost and ThisRound == 1):
                time1 = time.time()
                DownloadBoard()

    # 检测用户按下鼠标并修改棋盘
    for e in event:
        if e.type == pygame.MOUSEBUTTONDOWN:
            for i in range(15):
                for j in range(15):
                    if Left_Up[i][j][0] < Mouse_pos[0] < Right_Down[i][j][0] and Left_Up[i][j][1] < Mouse_pos[1] < \
                            Right_Down[i][j][1]:
                        # 联网模式
                        if Mode:
                            if RoomHost:
                                if ChessBoard[i][j] == 0:
                                    if ThisRound == 1:
                                        ChessBoard[i][j] = 1
                                        UploadBoard(str(i), str(j), "1")
                                        ThisRound = 2
                                        time1 = time.time()
                            else:
                                if ChessBoard[i][j] == 0:
                                    if ThisRound == 2:
                                        ChessBoard[i][j] = 2
                                        UploadBoard(str(i), str(j), "2")
                                        ThisRound = 1
                                        time1 = time.time()

                        # 非联网模式
                        else:
                            if ChessBoard[i][j] == 0:
                                if ThisRound == 1:
                                    ChessBoard[i][j] = 1
                                    ThisRound = 2
                                else:
                                    ChessBoard[i][j] = 2
                                    ThisRound = 1

    ShowBoard()

    # 检测赢者
    for i in range(15):
        for j in range(15):
            # 这个try是为了防止用户把棋子放在边界导致的列表索引溢出
            try:
                # 横向
                if ChessBoard[i][j] != 0 and ChessBoard[i][j] == ChessBoard[i][j + 1] == ChessBoard[i][j + 2] == \
                        ChessBoard[i][j + 3] == ChessBoard[i][j + 4]:
                    WinMsgBox(ChessBoard[i][j])
            except:
                pass

            try:
                # 竖向
                if ChessBoard[i][j] != 0 and ChessBoard[i][j] == ChessBoard[i + 1][j] == ChessBoard[i + 2][j] == \
                        ChessBoard[i + 3][j] == ChessBoard[i + 4][j]:
                    WinMsgBox(ChessBoard[i][j])
            except:
                pass

            try:
                # 从左上到右下
                if ChessBoard[i][j] != 0 and ChessBoard[i][j] == ChessBoard[i + 1][j + 1] == ChessBoard[i + 2][j + 2] == \
                        ChessBoard[i + 3][j + 3] == ChessBoard[i + 4][j + 4]:
                    WinMsgBox(ChessBoard[i][j])
            except:
                pass

            try:
                # 从左下到右上
                # 防bug
                if ChessBoard[i][j] != 0 and ChessBoard[i][j] == ChessBoard[i - 1][j + 1] == ChessBoard[i - 2][
                    j + 2] == \
                        ChessBoard[i - 3][j + 3] == ChessBoard[i - 4][j + 4]:
                    WinMsgBox(ChessBoard[i][j])
            except:
                pass

    pygame.display.update()
