# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

import json
import random
import base64
import requests
import subprocess
import datetime
import pickle
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtCore import Qt, qInfo, qInstallMessageHandler
from PyQt5.QtGui import QPixmap
from v2rayL_api import V2rayL, MyException
import pyzbar.pyzbar as pyzbar
from PIL import Image
from v2rayL_threads import (
    ConnectThread,
    DisConnectThread,
    UpdateSubsThread,
    PingThread,
    CheckUpdateThread,
    VersionUpdateThread,
    RunCmdThread
)
from new_ui import MainUi, SwitchBtn, Ui_Add_Ss_Dialog, Ui_Add_Vmess_Dialog, Ui_Subs_Dialog
from utils import SystemTray, qt_message_handler


class MyMainWindow(MainUi):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        self.init_ui()
        self.version = "2.1.3"

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
        # CMD线程
        self.run_cmd_start = RunCmdThread()
        self.run_cmd_start.start()

        if self.v2rayL.current_status.auto:
            self.config_setting_ui.switchBtn = SwitchBtn(self.config_setting_ui.label_9, True)
            self.config_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)
        else:
            self.config_setting_ui.switchBtn = SwitchBtn(self.config_setting_ui.label_9, False)
            self.config_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)

        # 自动更新订阅
        if self.v2rayL.current_status.auto and self.v2rayL.current_status.url:
            try:
                self.update_subs_start.v2rayL = self.v2rayL
                self.update_subs_start.subs_child_ui = None
                self.update_subs_start.start()
            except:
                # with open("/etc/v2rayL/ncurrent", "wb") as jf:
                #     self.v2rayL.current_status.url = set()
                #     self.v2rayL.current_status.auto = False
                #     pickle.dump(self.v2rayL.current_status, jf)
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format("更新失败")
                subprocess.call([shell], shell=True)

        # 自动检查更新
        if self.v2rayL.current_status.check:
            self.system_setting_ui.switchBtn = SwitchBtn(self.system_setting_ui.label_8, True)
            self.system_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)
            self.check_update_start.start()
        else:
            self.system_setting_ui.switchBtn = SwitchBtn(self.system_setting_ui.label_8, False)
            self.system_setting_ui.switchBtn.setGeometry(0, 0, 60, 30)

        # 是否启用日志
        if self.v2rayL.current_status.log:
            self.a3.setChecked(True)
            self.a4.setChecked(False)
        else:
            self.a4.setChecked(True)
            self.a3.setChecked(False)

        # 全局代理模式
        if self.v2rayL.current_status.proxy == 1:
            self.a5.setChecked(True)
            self.a6.setChecked(False)
            self.a7.setChecked(False)
        elif self.v2rayL.current_status.proxy == 2:
            self.a5.setChecked(False)
            self.a6.setChecked(True)
            self.a7.setChecked(False)
        else:
            self.a5.setChecked(False)
            self.a6.setChecked(False)
            self.a7.setChecked(True)

        # 填充当前订阅地址
       #  print(self.v2rayL.current_status.url)
        self.config_setting_ui.lineEdit.setText(";".join([x[1] for x in self.v2rayL.current_status.url]))
        # 端口
        self.system_setting_ui.http_sp.setValue(self.v2rayL.current_status.http)
        self.system_setting_ui.socks_sp.setValue(self.v2rayL.current_status.socks)
        # # 显示当前所有配置
        self.display_all_conf()

        qInfo("{}@$ff$@app start.".format(self.v2rayL.current_status.log))

        # self.ping_start = PingThread(tv=(self.tableView, self.v2rayL))
        # 事件绑定
        self.config_setting_ui.switchBtn.checkedChanged.connect(self.change_auto_update)
        self.system_setting_ui.switchBtn.checkedChanged.connect(self.change_check_update)
        # self.system_setting_ui.switchBtn1.checkedChanged.connect(self.auto_on)
        self.first_ui.pushButton.clicked.connect(lambda: self.update_subs(True))  # 更新订阅
        self.subs_add_child_ui.pushButton.clicked.connect(self.change_subs_addr)
        # self.subs_add_child_ui.textEdit.returnPressed.connect(self.change_subs_addr)
        self.config_setting_ui.pushButton_2.clicked.connect(self.output_conf)  # 导出配置文件
        self.config_setting_ui.pushButton.clicked.connect(self.get_conf_from_qr)  # 通过二维码导入
        self.first_ui.pushButton_1.clicked.connect(self.start_ping_th)  # 测试延时
        self.system_setting_ui.checkupdateButton.clicked.connect(self.check_update)  # 检查更新
       # self.config_setting_ui.lineEdit.returnPressed.connect(self.change_subs_addr)  # 更新订阅操作
        self.config_setting_ui.pushButton_3.clicked.connect(self.show_subs_dialog)  # 显示具体订阅操作
        self.config_setting_ui.lineEdit_2.returnPressed.connect(self.get_conf_from_uri)  # 解析URI获取配置
        self.conn_start.sinOut.connect(self.alert)  # 得到连接反馈
        self.disconn_start.sinOut.connect(self.alert)  # 得到断开连接反馈
        self.update_addr_start.sinOut.connect(self.alert)  # 得到反馈
        self.update_subs_start.sinOut.connect(self.alert)   # 得到反馈
        self.ping_start.sinOut.connect(self.alert)  # 得到反馈
        self.check_update_start.sinOut.connect(self.alert)
        self.version_update_start.sinOut.connect(self.alert)
        self.system_setting_ui.http_sp.valueChanged.connect(lambda: self.value_change(True))
        self.system_setting_ui.socks_sp.valueChanged.connect(lambda: self.value_change(False))
        self.config_setting_ui.pushButton_ss.clicked.connect(self.show_add_ss_dialog)
        self.config_setting_ui.pushButton_vmess.clicked.connect(self.show_add_vmess_dialog)
        self.ss_add_child_ui.pushButton.clicked.connect(self.add_ss_by_input)
        self.vmess_add_child_ui.pushButton.clicked.connect(self.add_vmess_by_input)
        self.subs_child_ui.pushButton.clicked.connect(self.show_add_subs_dialog)
        self.a1.triggered.connect(self.show)
        self.a3.triggered.connect(self.enable_log)
        self.a4.triggered.connect(self.disable_log)
        self.a5.triggered.connect(lambda: self.proxy_handler(1))
        self.a6.triggered.connect(lambda: self.proxy_handler(2))
        self.a7.triggered.connect(lambda: self.proxy_handler(0))

        # 设置最小化到托盘
        SystemTray(self, app)

        # print("aaaaa")

    def check_update(self):
        """
        检查版本更新
        :return:
        """
        # print("hahah")
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
                          True if k == self.v2rayL.current_status.current else False, self.start_conn_th,
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
        remark = self.subs_add_child_ui.lineEdit.text()
        url = self.subs_add_child_ui.textEdit.toPlainText()
        self.update_addr_start.v2rayL = self.v2rayL
        self.update_addr_start.subs_child_ui = self.subs_add_child_ui
        if not url:
            QMessageBox.warning(self, "添加订阅地址", self.tr("当前订阅地址为空，请输入订阅地址。"))
        elif not remark:
            QMessageBox.warning(self, "添加订阅地址", self.tr("当前别名为空，请输入别名。"))
        else:
            # shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在更新订阅地址......"
            # subprocess.call([shell], shell=True)
            self.update_addr_start.start()
            self.add_subs_ui.hide()

    def update_subs(self, flag):
        """
        手动更新订阅
        :return:
        """
        self.update_subs_start.v2rayL = self.v2rayL
        self.update_subs_start.subs_child_ui = None
        if flag:
            shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 正在更新订阅......"
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
            if self.v2rayL.current_status.current == region:
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
                qInfo("{}@$ff$@Successfully connected to: {}".format(self.v2rayL.current_status.log, ret).encode())
                self.display_all_conf()

            elif tp == "disconn":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL VPN连接已断开"
                subprocess.call([shell], shell=True)
                qInfo("{}@$ff$@VPN connection disconnected.".format(self.v2rayL.current_status.log))
                self.display_all_conf()

            elif tp == "addr":
                # shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 更新订阅地址成功"
                # subprocess.call([shell], shell=True)
                qInfo("{}@$ff$@Add a new subscription address: {}".format(self.v2rayL.current_status.log, ret))
                self.v2rayL = V2rayL()
                self.display_all_conf()
                self.show_subs_dialog()
                self.subs_add_child_ui.lineEdit.setText("")
                self.subs_add_child_ui.textEdit.setPlainText("")
                self.add_subs_ui.hide()
                self.config_setting_ui.lineEdit.setText(";".join([x[1] for x in self.v2rayL.current_status.url]))

            elif tp == "update":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 订阅更新完成"
                subprocess.call([shell], shell=True)
                if not ret[1]:
                    qInfo("{}@$ff$@Successfully updated subscription.".format(self.v2rayL.current_status.log))
                else:
                    retinfo = ""
                    for i in ret[1]:
                        retinfo += "\n{}-{}-{}".format(i[0][0], i[0][1], i[1])
                    qInfo("{}@$ff$@{}".format(self.v2rayL.current_status.log, retinfo).encode())
                    # print(retinfo)
                self.v2rayL = V2rayL()
                # print(123)
                self.display_all_conf()
                self.config_setting_ui.lineEdit.setText(";".join([x[1] for x in self.v2rayL.current_status.url]))

            elif tp == "ping":
                if isinstance(ret, int):
                    self.first_ui.time.setText(str(ret)+"ms")
                else:
                    self.first_ui.time.setText(ret)

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
                        self.version_update_start.url = "http://dl.thinker.ink/update.sh"
                        qInfo("{}@$ff$@Ready to update, the latest version number is: v{}.".format(
                            self.v2rayL.current_status.log, row.json()['tag_name']))
                        self.version_update_start.start()

            elif tp == "vrud":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format(ret)
                subprocess.call([shell], shell=True)
                qInfo("{}@$ff$@Successfully updated to the latest version.".format(self.v2rayL.current_status.log))

        else:
            if tp == "addr":
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL '{}'".format(ret)
                subprocess.call([shell], shell=True)
                if ret == "无法获取订阅信息，订阅站点访问失败":
                    ret = "Failed to access subscription site, unable to get subscription information"
                elif ret == "解析订阅信息失败，请确认链接正确":
                    ret = "Failed to resolve subscription information, please confirm the link is correct"
                else:
                    pass

                qInfo("{}@$ff$@Failed to get subscriptions: {}.".format(self.v2rayL.current_status.log, ret))

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

            elif tp == "ping":
                self.first_ui.time.setText(str(ret))

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
        if self.v2rayL.current_status.auto:
            self.v2rayL.subscribe(False)
            qInfo("{}@$ff$@Automatic update subscription is disabled.".format(self.v2rayL.current_status.log))
        else:
            if not self.v2rayL.current_status.url:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 不存在订阅地址，无需开启自动更新订阅"
                subprocess.call([shell], shell=True)
            self.v2rayL.subscribe(True)
            qInfo("{}@$ff$@Automatic update subscription is enabled.".format(self.v2rayL.current_status.log))

    def change_check_update(self):
        """
        是否自动检查更新
        :return:
        """
        if self.v2rayL.current_status.check:
            self.v2rayL.auto_check(False)
            qInfo("{}@$ff$@Automatically check for version updates disabled.".format(self.v2rayL.current_status.log))
        else:
            self.v2rayL.auto_check(True)
            qInfo("{}@$ff$@Automatically check for version updates enabled.".format(self.v2rayL.current_status.log))

    def start_ping_th(self):
        """
        开始测延时
        :return:
        """
        self.first_ui.time.setText("正在测试")
        self.ping_start.v2rayL = self.v2rayL
        self.ping_start.start()

    def show_share_dialog(self, region):
        """
        展示分享窗口
        :param region:
        :return:
        """
        ret = self.v2rayL.subs.conf2b64(region)
        # 生成二维码
        url = "http://api.k780.com:88/?app=qr.get&data={}".format(ret)
        try:
            req = requests.get(url, timeout=2)
            if req.status_code == 200:
                qr = QPixmap()
                qr.loadFromData(req.content)
                self.share_child_ui.label.setPixmap(qr)
                self.share_child_ui.label.setScaledContents(True)
            else:
                shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 生成二维码失败，可能原因：调用API发生错误"
                subprocess.call([shell], shell=True)
        except:
            shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 生成二维码失败，请将错误在github中提交"
            subprocess.call([shell], shell=True)

        self.share_child_ui.textBrowser.setText(ret)
        self.share_ui.show()

    def value_change(self, flag):
        """
        端口改变
        :param flag: true时为http， false为socks
        :return:
        """
        http_port = self.system_setting_ui.http_sp.value()
        socks_port = self.system_setting_ui.socks_sp.value()

        if flag:
            if http_port == self.v2rayL.current_status.socks:
                http_port = http_port + 1 if http_port < 10079 else http_port - 1
                self.system_setting_ui.http_sp.setValue(http_port)
            self.v2rayL.current_status.http = http_port

            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                pickle.dump(self.v2rayL.current_status, jf)

            qInfo("{}@$ff$@HTTP port is changed to {}".format(self.v2rayL.current_status.log, http_port))

        else:
            if socks_port == self.v2rayL.current_status.http:
                socks_port = socks_port + 1 if socks_port < 10079 else socks_port - 1
                self.system_setting_ui.socks_sp.setValue(socks_port)

            self.v2rayL.current_status.socks = socks_port

            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                pickle.dump(self.v2rayL.current_status, jf)

            qInfo("{}@$ff$@SOCKS port is changed to {}".format(self.v2rayL.current_status.log, socks_port))

        try:
            with open("/etc/v2rayL/config.json", "r") as f:
                ret = json.load(f)
        except FileNotFoundError:
            pass
        else:
            ret["inbounds"][1]["port"] = http_port
            ret["inbounds"][0]["port"] = socks_port
            with open("/etc/v2rayL/config.json", "w") as f:
                f.write(json.dumps(ret, indent=4))

        # if flag:
        #     self.v2rayL.current_status.http = http_port
        #     with open("/etc/v2rayL/ncurrent", "wb") as jf:
        #         # self.v2rayL.current_status.http = http_port
        #         pickle.dump(self.v2rayL.current_status, jf)
        #     qInfo("{}@$ff$@HTTP port is changed to {}".format(self.v2rayL.current_status.log, http_port))
        # else:
        #     self.v2rayL.current_status.socks = socks_port
        #     with open("/etc/v2rayL/ncurrent", "wb") as jf:
        #         pickle.dump(self.v2rayL.current_status, jf)
        #     qInfo("{}@$ff$@SOCKS port is changed to {}".format(self.v2rayL.current_status.log, socks_port))

        if self.v2rayL.current_status.current != "未连接至VPN":
            self.v2rayL.connect(self.v2rayL.current_status.current, True)

    def show_add_ss_dialog(self):
        """
        显示手动添加ss配置窗口
        :return:
        """
        self.ss_add_ui.show()

    def show_add_vmess_dialog(self):
        """
        显示添加Vmess配置窗口
        :return:
        """
        self.vmess_add_ui.show()

    def add_ss_by_input(self):
        """
        手动添加shadowsocks配置
        :return:
        """
        remark = self.ss_add_child_ui.lineEdit_2.text().strip()
        addr = self.ss_add_child_ui.lineEdit_3.text().strip()
        port = self.ss_add_child_ui.lineEdit_4.text().strip()
        password = self.ss_add_child_ui.lineEdit_5.text().strip()
        method = self.ss_add_child_ui.comboBox.currentText()
        # print(remark, addr, port, password, security)
        if not remark:
            remark = "shadowsocks_" + str(random.choice(range(10000, 99999)))

        b64str = "ss://"+base64.b64encode("{}:{}@{}:{}".format(method, password, addr, port).encode()).decode()\
                 + "#" + remark

        self.v2rayL.addconf(b64str)
        shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 添加成功"
        subprocess.call([shell], shell=True)
        self.v2rayL = V2rayL()
        self.display_all_conf()
        self.ss_add_child_ui.lineEdit_2.setText("")
        self.ss_add_child_ui.lineEdit_3.setText("")
        self.ss_add_child_ui.lineEdit_4.setText("")
        self.ss_add_child_ui.lineEdit_5.setText("")
        self.ss_add_ui.hide()

    def add_vmess_by_input(self):
        """
        手动添加vmess配置
        :return:
        """
        remark = self.vmess_add_child_ui.lineEdit.text().strip()
        addr = self.vmess_add_child_ui.lineEdit_2.text().strip()
        port = self.vmess_add_child_ui.lineEdit_3.text().strip()
        uid = self.vmess_add_child_ui.lineEdit_4.text().strip()
        aid = self.vmess_add_child_ui.lineEdit_5.text().strip()
        net = self.vmess_add_child_ui.comboBox.currentText()
        types = self.vmess_add_child_ui.comboBox_2.currentText()
        host = self.vmess_add_child_ui.lineEdit_6.text().strip()
        path = self.vmess_add_child_ui.lineEdit_7.text().strip()
        tls = self.vmess_add_child_ui.comboBox_3.currentText()
        # print(remark, addr, port, password, security)
        if not remark:
            remark = "vmess_" + str(random.choice(range(10000, 99999)))
        conf = {
            'add': addr,
            'port': port,
            'host': host,
            'ps': remark,
            'id': uid,
            'aid': aid,
            'net': net,
            'type': types,
            'path': path,
            'tls': tls,
            "v": 2
        }
        b64str = "vmess://" + base64.b64encode(str(conf).encode()).decode()

        self.v2rayL.addconf(b64str)
        shell = "notify-send -i /etc/v2rayL/images/logo.ico v2rayL 添加成功"
        subprocess.call([shell], shell=True)
        self.v2rayL = V2rayL()
        self.display_all_conf()
        self.vmess_add_child_ui.lineEdit.setText("")
        self.vmess_add_child_ui.lineEdit_2.setText("")
        self.vmess_add_child_ui.lineEdit_3.setText("")
        self.vmess_add_child_ui.lineEdit_4.setText("")
        self.vmess_add_child_ui.lineEdit_5.setText("")
        self.vmess_add_child_ui.lineEdit_6.setText("")
        self.vmess_add_child_ui.lineEdit_7.setText("")
        self.vmess_add_ui.hide()

    def enable_log(self):
        """
        启用操作日志
        :return:
        """
        self.v2rayL.current_status.log = True
        qInfo("{}@$ff$@Operation log has been enabled".format(self.v2rayL.current_status.log))
        self.a3.setChecked(True)
        self.a4.setChecked(False)
        self.v2rayL.logging(True)

    def disable_log(self):
        """
        启用操作日志
        :return:
        """
        qInfo("{}@$ff$@Operation log has been disabled".format(self.v2rayL.current_status.log))
        self.v2rayL.current_status.log = False
        self.a4.setChecked(True)
        self.a3.setChecked(False)
        self.v2rayL.logging(False)

    def show_subs_dialog(self):
        """
        显示订阅设置窗口
        :return:
        """
        subs_urls = self.v2rayL.current_status.url
        #print(subs_urls)
        self.subs_child_ui.tableWidget.setRowCount(len(subs_urls))
        i = 1
        # print(1111)
        for url in subs_urls:
            self.subs_child_ui.add_item((i, url[0], url[1], self.del_subs))
            i += 1
        self.subs_ui.show()

    def show_add_subs_dialog(self):
        """
        显示添加订阅窗口
        :return:
        """
        self.add_subs_ui.show()

    def auto_on(self):
        """
        开启/关闭开机自动连接
        :return:
        """
        if self.v2rayL.current_status.on:
            self.v2rayL.auto_on(False)
            qInfo("{}@$ff$@Automatic connection when booting is disabled.".format(self.v2rayL.current_status.log))
        else:
            self.v2rayL.auto_on(True)
            qInfo("{}@$ff$@Automatic connection when booting is enabled.".format(self.v2rayL.current_status.log))

    def del_subs(self, row):
        choice = QMessageBox.question(self, "删除订阅", "删除订阅地址，对应的配置也将删除，是否继续？",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            remark = self.subs_child_ui.tableWidget.item(row, 1).text()
            url = self.subs_child_ui.tableWidget.item(row, 2).text()
            for i in self.v2rayL.current_status.url:
                if i[0] == remark and i[1][:57] == url:
                    self.v2rayL.current_status.url.remove(i)
                    break

            with open("/etc/v2rayL/ncurrent", "wb") as f:
                pickle.dump(self.v2rayL.current_status, f)
            self.show_subs_dialog()
            if self.v2rayL.current_status.url:
                self.update_subs(False)
            else:
                # 如果连接对象为删除的订阅地址中的配置，断开连接
                if self.v2rayL.current_status.current in self.v2rayL.subs.saved_conf["subs"]:
                    self.disconn_start.v2rayL = self.v2rayL
                    self.disconn_start.tableView = self.first_ui.tableWidget
                    self.disconn_start.start()

                self.v2rayL.subs.saved_conf["subs"] = {}
                with open("/etc/v2rayL/ndata", "wb") as jf:
                    # print(self.v2rayL.subs.saved_conf)
                    pickle.dump(self.v2rayL.subs.saved_conf, jf)
                self.v2rayL = V2rayL()
                self.display_all_conf()
                self.config_setting_ui.lineEdit.setText(";".join([x[1] for x in self.v2rayL.current_status.url]))

    def proxy_handler(self, types):
        """
        修改全局代理模式
        :param types: 1:白名单 2:黑名单 0:关闭
        :return:
        """
        if types == 1:
            self.a5.setChecked(True)
            self.a6.setChecked(False)
            self.a7.setChecked(False)
        elif types == 2:
            self.a5.setChecked(False)
            self.a6.setChecked(True)
            self.a7.setChecked(False)
        else:
            self.a5.setChecked(False)
            self.a6.setChecked(False)
            self.a7.setChecked(True)

        lt = ["off", "whiteList", "gfwList"]
        self.v2rayL.proxy(types)
        qInfo("{}@$ff$@Proxy mode changed to: {}".format(self.v2rayL.current_status.log, lt[types]))
        if self.v2rayL.current_status.current != "未连接至VPN":
            self.v2rayL.connect(self.v2rayL.current_status.current, False)


if __name__ == "__main__":
    import sys
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    qInstallMessageHandler(qt_message_handler)
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    # 显示在屏幕上
    myWin.show()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())

