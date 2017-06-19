简介
===
用python编写的一个可以令同一局域网内的计算机通信软件

依赖
===
	python3.4.3
	pyqt5
功能
===
设计一个基于多播的多点控制系统，能在多个节点完成对加入本组的所有主机进行监控，能实时显示指定主机当前的运行状态，如CPU使用率，
开启的进程等等，在权限允许下可关闭或重启指定机器。组的范围不局限于某个局域网。

使用
===
	$ git clone git@github.com:laogewen/socket.git
	$ python broadcast.py
