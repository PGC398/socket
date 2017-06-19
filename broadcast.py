# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\PyQtCode\broadcast\IP组播.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!
from socket import *
from datetime import datetime
from decimal import Decimal
import socket ,platform,ctypes,psutil,time,threading,re,atexit,os,sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMessageBox, QGridLayout, QLabel, QPushButton, QFrame

#function of Get CPU State;
def getCPUstate(interval=1):
    return (str(psutil.cpu_percent(interval)) + "%")

#function of Get Memory
def getMemorystate():
        phymem = psutil.virtual_memory()
        line = "%s%%"%(phymem.percent)
        return line

#磁盘空间
def get_free_space_mb(folder):
        """ Return folder/drive free space (in bytes)
        """
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
            return Decimal(free_bytes.value/1024/1024/1024).quantize(Decimal('0.00'))
        else:
            st = os.statvfs(folder)
            return Decimal(st.f_bavail * st.f_frsize/1024/1024).quantize(Decimal('0.00'))

ANY = '0.0.0.0'
MCAST_ADDR = '224.168.2.9'#多播地址
MCAST_PORT = 1600 #多播端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #允许端口复用
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) #告诉内核这是一个多播类型的socket
sock.bind((ANY,MCAST_PORT))
status = sock.setsockopt(socket.IPPROTO_IP,  #告诉内核把自己加入指定的多播组，组地址由第三个参数指定
socket.IP_ADD_MEMBERSHIP,
socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))
sock.setblocking(0)
ts = time.time()

def receive():
    while 1:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            print(message)
        except :
            pass
        else:
            try:
                #判断是否已经选完网卡，进入通信页面
                if ui.listWidget.item(0).text() == "ip地址" +"                          " + "主机名":
                    #接收到登录请求
                    if message[0] == '#':
                        for i in range(1,(ui.listWidget.count())):
                            if ui.listWidget.item(i).text() == addr[0]+"  " + message.split('#')[1]:
                                receive()

                        ui.listWidget.addItem(addr[0]+"  " + message.split('#')[1])
                        ui.listWidget_3.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        ui.listWidget_3.addItem("您的好友"+ message.split('#')[1]+"已上线！")
                        myinfo='#'+socket.gethostname()
                        sock.sendto(myinfo.encode(), (MCAST_ADDR,MCAST_PORT) )
                    #接收到登出请求
                    if message[0] == '!':
                        for i in range(1,(ui.listWidget.count())):
                            if ui.listWidget.item(i).text() == addr[0]+"  " + message.split('!')[1]:
                                ui.listWidget.takeItem(i)
                                ui.listWidget_3.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                ui.listWidget_3.addItem("您的好友"+ message.split('!')[1]+"下线了！")
                                receive()

                    #接收到其他主机向本机请求命令
                    if message[0] == '@':
                        info = '$ '
                        for i in message.split():
                            if i == '1':
                                info += '1'+getCPUstate()+' '
                            if i == '2':
                                info += '2'+getMemorystate()+' '
                            if i == '3':
                                info += '3'+str(get_free_space_mb('C:\\'))+' '
                            if i == '4':
                                info += '4'+str(get_free_space_mb('D:\\'))+' '
                            if i == '5':
                                info += '5'+str(get_free_space_mb('E:\\'))+' '
                            if i == '6':
                                info += '6'+str(get_free_space_mb('F:\\'))+' '
                        sock.sendto(info.encode(), (addr[0],MCAST_PORT) )

                    #接收到其他主机返回命令
                    if message[0] == '$':
                        ui.listWidget_2.addItem("接收到来自IP地址为："+addr[0]+"的信息：")
                        for i in message.split():
                            try:
                                if i[0] == '1':
                                    ui.listWidget_2.addItem("CPU利用率为："+i[1:len(i)])
                                if i[0] == '2':
                                    ui.listWidget_2.addItem("内存利用率为："+i[1:len(i)])
                                if i[0] == '3':
                                    ui.listWidget_2.addItem("C盘剩余空间为："+i[1:len(i)]+"GB")
                                if i[0] == '4':
                                    ui.listWidget_2.addItem("D盘剩余空间为："+i[1:len(i)]+"GB")
                                if i[0] == '5':
                                    ui.listWidget_2.addItem("E盘剩余空间为："+i[1:len(i)]+"GB")
                                if i[0] == '6':
                                    ui.listWidget_2.addItem("F盘剩余空间为："+i[1:len(i)]+"GB")
                            except:
                                pass
                            '''if i.spilt('1') == '1':
                                ui.listWidget_2.addItem("CPU利用率为："+addr[0])'''

            except:
                pass




class Ui_MainWindow(QWidget):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(924, 672)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 291, 491))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_join = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_join.setGeometry(QtCore.QRect(40, 430, 93, 28))
        self.pushButton_join.setObjectName("pushButton_join")
        self.pushButton_quit = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_quit.setGeometry(QtCore.QRect(170, 430, 93, 28))
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(20, 30, 256, 381))
        self.listWidget.setObjectName("listWidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(500, 20, 391, 301))
        self.groupBox_2.setObjectName("groupBox_2")
        self.listWidget_2 = QtWidgets.QListWidget(self.groupBox_2)
        self.listWidget_2.setGeometry(QtCore.QRect(20, 20, 351, 261))
        self.listWidget_2.setObjectName("listWidget_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(500, 380, 391, 131))
        self.groupBox_3.setObjectName("groupBox_3")
        self.listWidget_3 = QtWidgets.QListWidget(self.groupBox_3)
        self.listWidget_3.setGeometry(QtCore.QRect(20, 30, 351, 91))
        self.listWidget_3.setObjectName("listWidget_3")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(330, 20, 151, 351))
        self.groupBox_4.setObjectName("groupBox_4")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox.setGeometry(QtCore.QRect(20, 30, 91, 19))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 70, 111, 19))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 110, 111, 19))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_4.setGeometry(QtCore.QRect(20, 150, 111, 19))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_5.setGeometry(QtCore.QRect(20, 189, 111, 20))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_6.setGeometry(QtCore.QRect(20, 230, 111, 19))
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_9 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_9.setGeometry(QtCore.QRect(20, 270, 111, 19))
        self.checkBox_9.setObjectName("checkBox_9")
        self.checkBox_10 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_10.setGeometry(QtCore.QRect(20, 310, 111, 19))
        self.checkBox_10.setObjectName("checkBox_10")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(500, 530, 391, 80))
        self.groupBox_5.setObjectName("groupBox_5")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 30, 121, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(20, 530, 371, 81))
        self.groupBox_6.setObjectName("groupBox_6")
        self.label = QtWidgets.QLabel(self.groupBox_6)
        self.label.setGeometry(QtCore.QRect(20, 30, 171, 32))
        self.label.setObjectName("label")
        self.pushButton_send = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_send.setGeometry(QtCore.QRect(230, 30, 111, 28))
        self.pushButton_send.setObjectName("pushButton_send")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 340, 121, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 340, 121, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.groupBox_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_7.setGeometry(QtCore.QRect(330, 390, 151, 121))
        self.groupBox_7.setObjectName("groupBox_7")
        self.checkBox_7 = QtWidgets.QCheckBox(self.groupBox_7)
        self.checkBox_7.setGeometry(QtCore.QRect(20, 40, 111, 19))
        self.checkBox_7.setObjectName("checkBox_7")
        self.checkBox_8 = QtWidgets.QCheckBox(self.groupBox_7)
        self.checkBox_8.setGeometry(QtCore.QRect(20, 80, 111, 19))
        self.checkBox_8.setObjectName("checkBox_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 924, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton_quit.clicked.connect(self.logout)
        self.pushButton_join.clicked.connect(self.slot1)
        self.listWidget.doubleClicked.connect(self.login)
        self.pushButton_send.clicked.connect(self.send)
        self.pushButton_3.clicked.connect(self.clear)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "组员信息区"))
        self.pushButton_join.setText(_translate("MainWindow", "加入组"))
        self.pushButton_quit.setText(_translate("MainWindow", "退出组"))
        self.groupBox_2.setTitle(_translate("MainWindow", "信息显示区"))
        self.groupBox_3.setTitle(_translate("MainWindow", "命令显示区"))
        self.groupBox_4.setTitle(_translate("MainWindow", "选择区"))
        self.checkBox.setText(_translate("MainWindow", "CPU利用率"))
        self.checkBox_2.setText(_translate("MainWindow", "内存利用率"))
        self.checkBox_3.setText(_translate("MainWindow", "C盘可用空间"))
        self.checkBox_4.setText(_translate("MainWindow", "D盘可用空间"))
        self.checkBox_5.setText(_translate("MainWindow", "E盘可用空间"))
        self.checkBox_6.setText(_translate("MainWindow", "F盘可用空间"))
        self.checkBox_9.setText(_translate("MainWindow", "磁盘写入速率"))
        self.checkBox_10.setText(_translate("MainWindow", "磁盘读取速率"))
        self.groupBox_5.setTitle(_translate("MainWindow", "特权操作"))
        self.pushButton.setText(_translate("MainWindow", "关闭计算机"))
        self.pushButton_2.setText(_translate("MainWindow", "重启计算机"))
        self.groupBox_6.setTitle(_translate("MainWindow", "操作区"))
        self.label.setText(_translate("MainWindow", "提示：请先选择指定主机"))
        self.pushButton_send.setText(_translate("MainWindow", "发送命令"))
        self.pushButton_3.setText(_translate("MainWindow", "清除列表信息"))
        self.pushButton_4.setText(_translate("MainWindow", "信息另存为"))
        self.groupBox_7.setTitle(_translate("MainWindow", "进程操作"))
        self.checkBox_7.setText(_translate("MainWindow", "进程列表"))
        self.checkBox_8.setText(_translate("MainWindow", "启动记事本"))

    #加入组按钮触发事件
    def slot1(self):
        if self.listWidget.item(1) != None:
            if self.listWidget.item(0).text() == "请选择网卡":
                QMessageBox.information(self,"提示","请双击选择网卡！")
            else:
                QMessageBox.critical(self,"警告","您已加入组，请勿重复加入！")
            return
        def get_netcard():
            netcard_info = []
            info = psutil.net_if_addrs()
            for k,v in info.items():
                for item in v:
                    if item[0] == 2 and not item[1]=='127.0.0.1':
                        netcard_info.append((k,item[1]))
            return netcard_info

        ipList=get_netcard()
        self.listWidget.addItem("请选择网卡")
        j=0
        asd=[]
        for i in ipList:
            self.listWidget.addItem(':'+str(j)+str(i))
            j+=1

    #双击选择网卡触发事件
    def login(self):
        if self.listWidget.item(self.listWidget.currentRow()).text()[0] == ':':
            try:
                choose=self.listWidget.item(self.listWidget.currentRow()).text()
                self.ANY=re.compile('((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))').findall(choose)
                self.listWidget.clear()
                self.listWidget.addItem("ip地址" +"                          " + "主机名")

                self.MCAST_ADDR = '224.168.2.9'#多播地址
                self.MCAST_PORT = 1600 #多播端口
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #允许端口复用
                self.sock.bind((self.ANY[0][0],1500))
                self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) #设置使用多播发送

                data='#'+socket.gethostname()
                self.sock.sendto(data.encode(), (self.MCAST_ADDR,self.MCAST_PORT) )
            except:
                pass
        else:
            return

    #退出组按钮触发事件
    def logout(self):
        if self.listWidget.item(0) == None:
            QMessageBox.critical(self,"警告","您还未加入组！")
            return
        elif self.listWidget.item(0).text() == "ip地址" +"                          " + "主机名":
            button = QMessageBox.question(self,"提示","确定退出吗？",
                                      QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
            if button == QMessageBox.Ok:
                data='!'+socket.gethostname()
                self.sock.sendto(data.encode(), (self.MCAST_ADDR,self.MCAST_PORT) )
                self.listWidget.clear()
            elif button == QMessageBox.Cancel:
                pass
            else:
                return
        elif self.listWidget.item(0).text() == "请选择网卡":
            button = QMessageBox.question(self,"提示","您还未选择网卡，确定退出吗？",
                                      QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.listWidget.clear()
            elif button == QMessageBox.Cancel:
                pass
            else:
                return

    #发送命令按钮触发事件
    def send(self):
        try:
            if self.listWidget.item(0).text() != "ip地址" +"                          " + "主机名":
                QMessageBox.critical(self,"警告","您还未加入组！")
                return
            else:
                if self.listWidget.currentRow() == -1:
                    QMessageBox.critical(self,"警告","请先选择需要操作的主机！")
                else:
                    mission='@ '
                    if self.checkBox.isChecked():
                        mission += '1 '
                    if self.checkBox_2.isChecked():
                        mission += '2 '
                    if self.checkBox_3.isChecked():
                        mission += '3 '
                    if self.checkBox_4.isChecked():
                        mission += '4 '
                    if self.checkBox_5.isChecked():
                        mission += '5 '
                    if self.checkBox_6.isChecked():
                        mission += '6 '
                    if self.checkBox_7.isChecked():
                        mission += '7 '
                    if self.checkBox_8.isChecked():
                        mission += '8 '
                    if self.checkBox_9.isChecked():
                        mission += '9 '
                    if self.checkBox_10.isChecked():
                        mission += '10 '

                    print(mission)
                    choose=self.listWidget.item(self.listWidget.currentRow()).text()
                    destination=re.compile('((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))').findall(choose)
                    self.sock.sendto(mission.encode(), (destination[0][0],self.MCAST_PORT) )
        except:
            pass

    #清除列表信息按钮触发事件
    def clear(self):
        self.listWidget_2.clear()
        #self.listWidget_3.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    threads = []
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=MainWindow.show())
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    app.exec_()
    data='!'+socket.gethostname()
    sock.sendto(data.encode(), (MCAST_ADDR,MCAST_PORT) )


