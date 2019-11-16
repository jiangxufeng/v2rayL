# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-10-24

import sys
import datetime
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (
    QtInfoMsg,
    QtWarningMsg,
    QtCriticalMsg,
    QtFatalMsg
)


class SystemTray(object):
    # 程序托盘类
    def __init__(self, w, app):
        self.app = app
        self.w = w
        QApplication.setQuitOnLastWindowClosed(False)  # 禁止默认的closed方法，
        self.w.show()  # 不设置显示则为启动最小化到托盘
        self.tp = QSystemTrayIcon(self.w)
        self.initUI()
        self.run()

        # sys.stdout = EmittingStream(textWritten=self.w.output_ter_result)
        # sys.stderr = EmittingStream(textWritten=self.w.output_ter_result)

    def initUI(self):
        # 设置托盘图标
        self.tp.setIcon(QIcon('/etc/v2rayL/images/logo.ico'))

    def quitApp(self):
        # 退出程序
        self.w.show()  # w.hide() #设置退出时是否显示主窗口
        re = QMessageBox.question(self.w, "提示", "确认退出？", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            self.tp.setVisible(False)  # 隐藏托盘控件
            qApp.quit()  # 退出程序
            self.w.v2rayL.disconnect()

    def act(self, reason):
        # 主界面显示方法
        if reason == 2 or reason == 3:
            self.w.show()

    def run(self):
        self.w.a2.triggered.connect(self.quitApp)
        self.tp.setContextMenu(self.w.tpMenu)
        self.tp.show()  # 不调用show不会显示系统托盘消息，图标隐藏无法调用

        # 绑定提醒信息点击事件
        # self.tp.messageClicked.connect(self.message)
        # 绑定托盘菜单点击事件
        self.tp.activated.connect(self.act)
        sys.exit(self.app.exec_())  # 持续对app的连接


def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
     mode = 'INFO'
    elif mode == QtWarningMsg:
     mode = 'WARNING'
    elif mode == QtCriticalMsg:
     mode = 'CRITICAL'
    elif mode == QtFatalMsg:
     mode = 'FATAL'
    else:
     mode = 'DEBUG'

    en, info = message.split("@$ff$@")
    if en == "True":
        with open("/etc/v2rayL/v2rayL_op.log", "a+") as f:
            f.write(' %s - %s: %s\n' % (datetime.datetime.now(), mode, info))
