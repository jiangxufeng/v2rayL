# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

from PyQt5.QtCore import QThread, pyqtSignal


class ConnectThread(QThread):
    """连接线程"""
    sinOut = pyqtSignal(tuple)

    def __init__(self, tv=(None, None), parent=None):
        super(ConnectThread, self).__init__(parent)
        # 设置工作状态与初始num数值
        self.tableView, self.v2rayL = tv

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        row = self.tableView.currentIndex().row()
        region = self.tableView.model().item(row, 0).text()
        try:
            self.v2rayL.connect(region)
        except MyException as e:
            self.sinOut.emit(("conn", "@@Fail@@", e.args[0], None))
        else:
            self.sinOut.emit(("conn", "@@OK@@", region, row))


class DisConnectThread(QThread):
    """
    断开连接线程
    """
    sinOut = pyqtSignal(tuple)

    def __init__(self, tv=(None, None), parent=None):
        super(DisConnectThread, self).__init__(parent)
        self.tableView, self.v2rayL = tv

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        try:
            self.v2rayL.disconnect()
        except MyException as e:
            self.sinOut.emit(("disconn", "@@Fail@@", e.args[0], None))
        else:
            self.sinOut.emit(("disconn", "@@OK@@", "未连接至VPN", None))


class UpdateSubsThread(QThread):
    """
    更新订阅线程
    """
    sinOut = pyqtSignal(tuple)

    def __init__(self, tv=(None, None,), parent=None):
        super(UpdateSubsThread, self).__init__(parent)
        self.v2rayL, self.subs_child_ui = tv

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        # msg = QMessageBox.information()
        if self.subs_child_ui:
            url = self.subs_child_ui.lineEdit.text()
            try:
                self.v2rayL.update(url)
            except MyException as e:
                self.sinOut.emit(("addr", "@@Fail@@", e.args[0], None))
            else:
                self.sinOut.emit(("addr", "@@OK@@", "订阅地址更新成功！", None))
        else:
            url = self.v2rayL.url
            if not url:
                self.sinOut.emit(("update", "@@Fail@@", "不存在订阅地址，无法更新", None))
            else:
                try:
                    self.v2rayL.update(url)
                except MyException as e:
                    self.sinOut.emit(("update", "@@Fail@@", e.args[0], None))
                else:
                    self.sinOut.emit(("update", "@@OK@@", "订阅更新成功！", None))


class PingThread(QThread):
    """
    断开连接线程
    """
    sinOut = pyqtSignal(tuple)

    def __init__(self, tv=(None, None), parent=None):
        super(PingThread, self).__init__(parent)
        self.tableView, self.v2rayL = tv

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        try:
            row = self.tableView.currentIndex().row()
            addr = self.tableView.model().item(row, 1).text()
            ret = self.v2rayL.ping(addr)
        except MyException as e:
            self.sinOut.emit(("ping", "@@Fail@@", e.args[0], None))
        else:
            self.sinOut.emit(("ping", "@@OK@@", ret.strip(), None))