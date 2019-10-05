# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

from PyQt5.QtCore import QThread, pyqtSignal
from sub2conf_api import MyException
import subprocess
import requests


class ConnectThread(QThread):
    """连接线程"""
    sinOut = pyqtSignal(tuple)

    def __init__(self, tv=(None, None, None), parent=None):
        super(ConnectThread, self).__init__(parent)
        # 设置工作状态与初始num数值
        self.tableView, self.v2rayL, self.row = tv

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        try:
            # row = self.tableView.currentIndex().row()
            region = self.tableView.item(self.row, 1).text()
        except AttributeError:
            self.sinOut.emit(("conn", "@@Fail@@", "未选中配置无法连接，请导入配置后再次连接", None))
        else:
            try:
                self.v2rayL.connect(region, False)
            except MyException as e:
                self.sinOut.emit(("conn", "@@Fail@@", e.args[0], None))
            else:
                self.sinOut.emit(("conn", "@@OK@@", region, self.row))


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
    测试延时线程
    """
    sinOut = pyqtSignal(tuple)

    def __init__(self, v2ray=None, parent=None):
        super(PingThread, self).__init__(parent)
        self.v2rayL = v2ray

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        try:
            # # row = self.tableView.currentIndex().row()
            # addr = self.tableView.model().item(self.row, 1).text()
            ret = self.v2rayL.ping()
        except MyException as e:
            self.sinOut.emit(("ping", "@@Fail@@", e.args[0], None))
        except AttributeError:
            self.sinOut.emit(("ping", "@@Fail@@", "请选择需要测试的配置.", None))
        else:
            self.sinOut.emit(("ping", "@@OK@@", ret, None))


class CheckUpdateThread(QThread):
    """
    检查更新线程
    """
    sinOut = pyqtSignal(tuple)

    def __init__(self, version=None, parent=None):
        super(CheckUpdateThread, self).__init__(parent)
        self.version = version

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        update_url = "https://api.github.com/repos/jiangxufeng/v2rayL/releases/latest"
        try:
            req = requests.get(update_url, timeout=10)
            if req.status_code != 200:
                self.sinOut.emit(("ckud", "@@Fail@@", "网络错误，请检查网络连接或稍后再试.", None))
            else:
                latest = req.json()['tag_name']
                if latest == self.version:
                    self.sinOut.emit(("ckud", "@@OK@@", "当前版本已是最新版本.", None))
                else:
                    self.sinOut.emit(("ckud", "@@OK@@", "正在后台进行更新..", req))
        except:
            self.sinOut.emit(("ckud", "@@Fail@@", "网络错误，请检查网络连接或稍后再试.", None))


class VersionUpdateThread(QThread):
    """
    测试延时线程
    """
    sinOut = pyqtSignal(tuple)

    def __init__(self, update_url=None, parent=None):
        super(VersionUpdateThread, self).__init__(parent)
        self.url = update_url

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()

    def run(self):
        try:
            req = requests.get(self.url)
            if req.status_code != 200:
                self.sinOut.emit(("vrud", "@@Fail@@", "网络错误，请检查网络连接或稍后再试.", None))
            else:
                with open("/etc/v2rayL/update.sh", 'w') as f:
                    f.write(req.text)

                subprocess.call(["chmod +x /etc/v2rayL/update.sh && /etc/v2rayL/update.sh"], shell=True)

                self.sinOut.emit(("vrud", "@@OK@@", "更新完成, 重启程序生效.", None))

        except Exception:
            self.sinOut.emit(("vrud", "@@Fail@@", "网络错误，请检查网络连接或稍后再试.", None))

