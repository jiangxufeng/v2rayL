# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

import requests
import subprocess
import pickle
from PyQt5.QtWidgets import (
    QMenu,
    QAction,
    QApplication,
    QMessageBox,
    QFileDialog,
    QSystemTrayIcon,
    qApp
)

from PyQt5.QtGui import QIcon, QPixmap
from v2rayL_api import V2rayL, MyException
import pyzbar.pyzbar as pyzbar
from PIL import Image
from v2rayL_threads import (
    ConnectThread,
    DisConnectThread,
    UpdateSubsThread,
    PingThread,
    CheckUpdateThread,
    VersionUpdateThread
)
from new_ui import MainUi, SwitchBtn


class SystemTray(object):
    # 程序托盘类
    def __init__(self, w):
        self.app = app
        self.w = w
        QApplication.setQuitOnLastWindowClosed(False)  # 禁止默认的closed方法，
        self.w.show()  # 不设置显示则为启动最小化到托盘
        self.tp = QSystemTrayIcon(self.w)
        self.initUI()
        self.run()

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
        a1 = QAction('恢复(Show)', triggered=self.w.show)
        a3 = QAction('退出(Exit)', triggered=self.quitApp)
        tpMenu = QMenu()
        tpMenu.addAction(a1)
        tpMenu.addAction(a3)
        self.tp.setContextMenu(tpMenu)
        self.tp.show()  # 不调用show不会显示系统托盘消息，图标隐藏无法调用

        # 绑定提醒信息点击事件
        # self.tp.messageClicked.connect(self.message)
        # 绑定托盘菜单点击事件
        self.tp.activated.connect(self.act)
        sys.exit(self.app.exec_())  # 持续对app的连接


class MyMainWindow(MainUi):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.init_ui()

        self.version = "2.0.4"

        # 获取api操作
        self.v2rayL = V2rayL()
        # 开启连接线程
        self.conn_start = ConnectThread()
        # 断开连接线程
        self.disconn_start = DisConnectThread()
        # 更新线程
        self.update_addr_start = UpdateSubsThread()
        self.update_subs_start = UpdateSubsThread()

        self.ping_start = PingThread()
        # 检查版本更新线程
        self.check_update_start = CheckUpdateThread(version=self.version)
        # 更新版本线程
        self.version_update_start = VersionUpdateThread()
        if self.v2rayL.auto:
            self.config_setting_ui.switchBtn = SwitchBtn(self.config_setting_ui.label_9, True)
            self.config_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)
        else:
            self.config_setting_ui.switchBtn = SwitchBtn(self.config_setting_ui.label_9, False)
            self.config_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)

        # 自动更新订阅
        if self.v2rayL.auto and self.v2rayL.url:
            try:
                self.update_subs_start.v2rayL = self.v2rayL
                self.update_subs_start.subs_child_ui = None
                self.update_subs_start.start()
            except:
                with open("/etc/v2rayL/ncurrent", "wb") as jf:
                    pickle.dump((self.v2rayL.current, None, False, self.v2rayL.check), jf)
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format("更新失败, 已关闭自动更新，请更新订阅地址")
                subprocess.call([shell], shell=True)

        # 自动检查更新
        if self.v2rayL.check:
            self.system_setting_ui.switchBtn = SwitchBtn(self.system_setting_ui.label_8, True)
            self.system_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)
            self.check_update_start.start()
        else:
            self.system_setting_ui.switchBtn = SwitchBtn(self.system_setting_ui.label_8, False)
            self.system_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)

        # 填充当前订阅地址
        self.config_setting_ui.lineEdit.setText(self.v2rayL.url)
        #
        # # 显示当前所有配置
        self.display_all_conf()

        # self.ping_start = PingThread(tv=(self.tableView, self.v2rayL))
        # 事件绑定
        self.config_setting_ui.switchBtn.checkedChanged.connect(self.change_auto_update)
        self.system_setting_ui.switchBtn.checkedChanged.connect(self.change_check_update)
        self.first_ui.pushButton.clicked.connect(self.update_subs)  # 更新订阅
        self.config_setting_ui.pushButton_2.clicked.connect(self.output_conf)  # 导出配置文件
        self.config_setting_ui.pushButton.clicked.connect(self.get_conf_from_qr)  # 通过二维码导入
        self.first_ui.pushButton_1.clicked.connect(self.start_ping_th)  # 测试延时
        self.system_setting_ui.checkupdateButton.clicked.connect(self.check_update)  # 检查更新
        self.config_setting_ui.lineEdit.returnPressed.connect(self.change_subs_addr)  # 更新订阅操作
        self.config_setting_ui.pushButton_3.clicked.connect(self.change_subs_addr)  # 更新订阅操作
        self.config_setting_ui.lineEdit_2.returnPressed.connect(self.get_conf_from_uri)  # 解析URI获取配置
        self.conn_start.sinOut.connect(self.alert)  # 得到连接反馈
        self.disconn_start.sinOut.connect(self.alert)  # 得到断开连接反馈
        self.update_addr_start.sinOut.connect(self.alert)  # 得到反馈
        self.update_subs_start.sinOut.connect(self.alert)   # 得到反馈
        self.ping_start.sinOut.connect(self.alert)  # 得到反馈
        self.check_update_start.sinOut.connect(self.alert)
        self.version_update_start.sinOut.connect(self.alert)

        # 设置最小化到托盘
        SystemTray(self)

    def check_update(self):
        shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在检查版本更新."
        subprocess.call([shell], shell=True)
        self.check_update_start.start()

    def display_all_conf(self):
        """
        列出所有的可用配置
        :return:
        """
        all_conf = self.v2rayL.subs.conf
        lists = []
        i = 1
        for k, v in all_conf.items():
            lists.append((i, k, str(v["add"])+":"+str(v["port"]), v["prot"],
                          True if k == self.v2rayL.current else False, self.start_conn_th,
                          self.del_conf, self.show_share_dialog))
            i += 1
        self.first_ui.tableWidget.setRowCount(i-1)

        for i in lists:
            self.first_ui.add_item(i)

    def change_subs_addr(self):
        """
        更新订阅地址
        :return:
        """
        url = self.config_setting_ui.lineEdit.text()
        self.update_addr_start.v2rayL = self.v2rayL
        self.update_addr_start.subs_child_ui = self.config_setting_ui
        if not url:
            choice = QMessageBox.warning(self, "订阅地址更新", self.tr("当前订阅地址为空，"
                                                                 "继续则删除订阅地址，同时会删除所有订阅配置，"
                                                                 "是否继续？"),
                                         QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if choice == QMessageBox.Ok:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在更新订阅地址......"
                subprocess.call([shell], shell=True)
                self.update_addr_start.start()
            else:
                self.config_setting_ui.lineEdit.setText(self.v2rayL.url)
        else:
            if url == self.v2rayL.url:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 订阅地址未改变"
                subprocess.call([shell], shell=True)
            else:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在更新订阅地址......"
                subprocess.call([shell], shell=True)
                self.update_addr_start.start()

    def update_subs(self):
        """
        手动更新订阅
        :return:
        """
        self.update_subs_start.v2rayL = self.v2rayL
        self.update_subs_start.subs_child_ui = None
        shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在更新订阅...... -t 1"
        subprocess.call([shell], shell=True)
        self.update_subs_start.start()

    def get_conf_from_uri(self):
        """
        通过分享链接获取配置
        :return:
        """
        uris = self.config_setting_ui.lineEdit_2.text().split(";")
        if not uris:
            QMessageBox.warning(self, "提示",
                                self.tr("请输入配置分享路径！"),
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            uris = [x for x in uris if x]
            errors = []
            for i in range(len(uris)):
                try:
                    self.v2rayL.addconf(uris[i])
                except MyException:
                    # shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format("错误： "+e.args[0])
                    # subprocess.call([shell], shell=True)
                    # self.config_setting_ui.lineEdit_2.setText("")
                    errors.append(str(i+1))
                # else:
            if not errors:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 添加配置成功"
            else:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL " \
                        "添加配置成功，其中第{}条配置解析错误，无法添加".format("、".join(errors))
            subprocess.call([shell], shell=True)
            self.v2rayL = V2rayL()
            self.display_all_conf()
            self.config_setting_ui.lineEdit_2.setText("")

    def get_conf_from_qr(self):
        """
        从二维码导入配置
        :return:
        """
        fname, ok = QFileDialog.getOpenFileName(self, '选择二维码图片', '/home', 'Image files(*.jpg *.png)')
        if ok:
            try:
                barcode = pyzbar.decode(Image.open(fname))
            except:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 二维码解析错误：无法解析该二维码"
                subprocess.call([shell], shell=True)
            else:
                try:
                    self.v2rayL.addconf(barcode[0].data.decode("utf-8"))
                except MyException as e:
                    shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format("错误： " + e.args[0])
                    subprocess.call([shell], shell=True)
                except:
                    shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 二维码解析错误：无法解析该二维码"
                    subprocess.call([shell], shell=True)
                else:
                    shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 添加配置成功"
                    subprocess.call([shell], shell=True)
                    self.v2rayL = V2rayL()
                    self.display_all_conf()

    def del_conf(self, row):
        """
        移除一个配置
        :return:
        """
        try:
            # row = self.tableView.currentIndex().row()
            region = self.first_ui.tableWidget.item(row, 1).text()
        except AttributeError:
            QMessageBox.information(self, "移除通知", self.tr("未选择任何配置."))
        else:
            if self.v2rayL.current == region:
                QMessageBox.information(self, "移除通知", self.tr("当前配置正在使用，无法移除."))
            else:
                try:
                    self.v2rayL.delconf(region)
                except MyException as e:
                    QMessageBox.critical(self, "移除失败", self.tr(e.args[0]))
                else:
                    self.display_all_conf()

    def start_conn_th(self, row, checked):
        """
        开启连接线程
        """
        if not checked:
            # shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在连接...... -t 0"
            # subprocess.call([shell], shell=True)
            self.conn_start.v2rayL = self.v2rayL
            self.conn_start.tableView = self.first_ui.tableWidget
            self.conn_start.row = row
            self.conn_start.start()
        else:
            # shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在断开连接...... -t 0"
            # subprocess.call([shell], shell=True)
            self.disconn_start.v2rayL = self.v2rayL
            self.disconn_start.tableView = self.first_ui.tableWidget
            self.disconn_start.start()

    def alert(self, tp):
        """
        操作反馈
        """
        tp, rs, ret, row = tp
        if rs == "@@OK@@":
            if tp == "conn":
                # QMessageBox.information(self, "连接成功", self.tr("连接成功！当前状态: " + ret))
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '连接成功！当前状态: " + ret + "'"
                subprocess.call([shell], shell=True)
                self.display_all_conf()

            elif tp == "disconn":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL VPN连接已断开"
                subprocess.call([shell], shell=True)
                self.display_all_conf()

            elif tp == "addr":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 更新订阅地址成功"
                subprocess.call([shell], shell=True)
                self.v2rayL = V2rayL()
                self.display_all_conf()

            elif tp == "update":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 订阅更新完成"
                subprocess.call([shell], shell=True)
                self.v2rayL = V2rayL()
                self.display_all_conf()

            elif tp == "ping":
                self.first_ui.time.setText(str(ret)+"ms")

            elif tp == "ckud":
                if not row:
                    shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL {}".format(ret)
                    subprocess.call([shell], shell=True)
                else:
                    choice = QMessageBox.question(self, "检查更新", "最新版本: v{}"
                                                  "\n更新内容:\n{}\n是否更新？".format(
                        row.json()['tag_name'],
                        row.json()['body']),
                                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if choice == QMessageBox.Yes:
                        shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL {}".format(ret)
                        subprocess.call([shell], shell=True)
                        self.version_update_start.url = row.json()["assets"][1]['browser_download_url']
                        self.version_update_start.start()

            elif tp == "vrud":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format(ret)
                subprocess.call([shell], shell=True)

        else:
            if tp == "addr":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 地址设置错误"
                subprocess.call([shell], shell=True)

            elif tp == "conn":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL {}".format(ret)
                subprocess.call([shell], shell=True)
                self.display_all_conf()

            elif tp == "disconn":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL {}".format(ret)
                subprocess.call([shell], shell=True)
                self.display_all_conf()

            elif tp == "ckud":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL {}".format(ret)
                subprocess.call([shell], shell=True)

            elif tp == "vrud":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL {}".format(ret)
                subprocess.call([shell], shell=True)

    def output_conf(self):
        """
        导出配置文件
        """
        fileName, ok2 = QFileDialog.getSaveFileName(self,
                                                     "文件保存",
                                                     "/home",
                                                     "Json Files (*.json)")
        if ok2:
            with open("/etc/v2rayL/config.json", "r") as f:
                tmp = f.read()
            with open(fileName, "w") as wf:
                wf.write(tmp)
            shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format("保存为： "+fileName)
            subprocess.call([shell], shell=True)

    def change_auto_update(self):
        """
        是否自动更新订阅
        :return:
        """
        if self.v2rayL.auto:
            self.v2rayL.subscribe(False)
        else:
            if not self.v2rayL.url:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 不存在订阅地址，无需开启自动更新订阅"
                subprocess.call([shell], shell=True)
            self.v2rayL.subscribe(True)

    def change_check_update(self):
        """
        是否自动检查更新
        :return:
        """
        if self.v2rayL.check:
            self.v2rayL.auto_check(False)
        else:
            self.v2rayL.auto_check(True)

    def start_ping_th(self):
        """
        开始测延时
        :return:
        """
        self.ping_start.v2rayL = self.v2rayL
        self.ping_start.start()

    def show_share_dialog(self, region):
        self.share_child_ui.pushButton.clicked.connect(lambda: self.output_conf_by_qr(region))
        self.share_child_ui.pushButton_2.clicked.connect(lambda: self.output_conf_by_uri(region))
        self.share_ui.show()

    def output_conf_by_uri(self, region):
        """
        输出分享链接
        :return:
        """
        # if self.v2rayL.current != "未连接至VPN":
        #     ret = self.v2rayL.subs.conf2b64(self.v2rayL.current)
        #     QMessageBox.information(self, "分享链接", self.tr(ret))
        # else:
        #     shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 请连接一个VPN后再选择分享 -t 3"
        #     subprocess.call([shell], shell=True)
        ret = self.v2rayL.subs.conf2b64(region)
        QMessageBox.information(self, "分享链接", self.tr(ret))

    def output_conf_by_qr(self, region):
        """
        输出分享二维码
        :return:
        """
        ret = self.v2rayL.subs.conf2b64(region)
        # 生成二维码
        url = "http://api.k780.com:88/?app=qr.get&data={}".format(ret)
        try:
            req = requests.get(url)
            if req.status_code == 200:
                qr = QPixmap()
                qr.loadFromData(req.content)
                self.qr_child_ui.label.setPixmap(qr)
                self.qr_child_ui.label.setScaledContents(True)
                self.qr_ui.show()
            else:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 服务错误，可能原因：调用API发生错误"
                subprocess.call([shell], shell=True)
        except:
            shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 服务错误，请将错误在github中提交"
            subprocess.call([shell], shell=True)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    # 显示在屏幕上
    myWin.show()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
