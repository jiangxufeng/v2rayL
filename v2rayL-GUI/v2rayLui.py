# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

from PyQt5.QtWidgets import (
    QLabel, 
    QAbstractItemView, 
    QHeaderView, 
    QStatusBar,
    QItemDelegate,
    QWidget,
    QGridLayout,
    QTableView,
    QMenuBar,
    QMenu,
    QToolBar,
    QAction,
    QMainWindow,
    QApplication,
    QLineEdit,
    QPushButton,
    QDialog,
    QMessageBox,
    QFileDialog,
    QSystemTrayIcon,
    qApp
)

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt, QSize, QRect, QCoreApplication, QMetaObject
from v2rayL_api import V2rayL, MyException
from datetime import datetime
from v2rayL_threads import ConnectThread, DisConnectThread, UpdateSubsThread, PingThread


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(853, 400)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 853, 28))
        self.menubar.setObjectName("menubar")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QMenu(self.menu)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QMenu(self.menu_4)
        self.menu_5.setObjectName("menu_5")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.connect_ui = QAction(QIcon("./images/ok2.png"), "连接", self)
        self.toolBar.addAction(self.connect_ui)

        self.disconnect_ui = QAction(QIcon("./images/no2.png"), "断开连接", self)
        self.toolBar.addAction(self.disconnect_ui)

        self.delconf_ui = QAction(QIcon("./images/del.png"), "删除当前配置", self)
        self.toolBar.addAction(self.delconf_ui)

        self.ping_ui = QAction(QIcon("./images/ping.png"), "测试延时", self)
        self.toolBar.addAction(self.ping_ui)

        self.action = QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_4 = QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_6 = QAction(MainWindow)
        self.action_6.setObjectName("action_6")
        self.action_8 = QAction(MainWindow, checkable=True)
        self.action_8.setObjectName("action_8")
        self.action_9 = QAction(MainWindow, checkable=True)
        self.action_9.setObjectName("action_9")
        self.action_10 = QAction(MainWindow)
        self.action_10.setObjectName("action_10")
        self.action_11 = QAction(MainWindow)
        self.action_11.setObjectName("action_11")
        self.action_24 = QAction(MainWindow)
        self.action_24.setObjectName("action_24")
        self.action_25 = QAction(MainWindow)
        self.action_25.setObjectName("action_25")
        self.menu_3.addAction(self.action_24)
        self.menu_3.addAction(self.action_25)
        self.menu.addAction(self.menu_3.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.action_10)
        self.menu.addSeparator()
        self.menu.addAction(self.action_11)
        self.menu.addSeparator()
        self.menu_5.addAction(self.action_8)
        self.menu_5.addAction(self.action_9)
        self.menu_4.addAction(self.action_5)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.action_6)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.menu_5.menuAction())
        self.menu_4.addSeparator()
        self.menu_2.addSeparator()
        self.menu_2.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "V2rayL"))
        MainWindow.setWindowIcon(QIcon("./images/logo.png"))
        self.menu.setTitle(_translate("MainWindow", "配置"))
        self.menu_3.setTitle(_translate("MainWindow", "添加配置"))
        self.menu_4.setTitle(_translate("MainWindow", "订阅"))
        self.menu_5.setTitle(_translate("MainWindow", "自动更新"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action.setText(_translate("MainWindow", "订阅设置"))
        self.action_2.setText(_translate("MainWindow", "更新订阅"))
        self.action_4.setText(_translate("MainWindow", "二维码获取配置"))
        self.action_5.setText(_translate("MainWindow", "地址设置"))
        self.action_6.setText(_translate("MainWindow", "更新订阅"))
        self.action_8.setText(_translate("MainWindow", "开启"))
        self.action_9.setText(_translate("MainWindow", "关闭"))
        self.action_10.setText(_translate("MainWindow", "导出当前配置"))
        self.action_11.setText(_translate("MainWindow", "分享当前配置"))
        self.action_24.setText(_translate("MainWindow", "通过链接"))
        self.action_25.setText(_translate("MainWindow", "通过二维码"))


class Ui_Subs_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(442, 109)
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(10, 20, 79, 23))
        self.label.setObjectName("label")
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setGeometry(QRect(90, 20, 331, 25))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(160, 70, 89, 25))
        self.pushButton.setStyleSheet("background-color: rgb(115, 210, 22)")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setGeometry(QRect(270, 70, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "订阅地址设置"))
        self.label.setText(_translate("Dialog", "订阅地址 ："))
        self.pushButton.setText(_translate("Dialog", "确定"))
        self.pushButton_2.setText(_translate("Dialog", "取消"))


class Ui_Conf_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(463, 159)
        Dialog.setMinimumSize(QSize(463, 159))
        Dialog.setMaximumSize(QSize(463, 159))
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(30, 30, 81, 21))
        self.label.setObjectName("label")
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setGeometry(QRect(110, 30, 321, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QLabel(Dialog)
        self.label_2.setGeometry(QRect(30, 60, 331, 31))
        self.label_2.setMinimumSize(QSize(331, 31))
        self.label_2.setObjectName("label_2")
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(220, 110, 89, 25))
        self.pushButton.setStyleSheet("background-color:rgb(138, 226, 52)")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setGeometry(QRect(330, 110, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "添加配置"))
        self.label.setText(_translate("Dialog", "配置链接："))
        self.label_2.setText(_translate("Dialog", "注：目前只支持vmess://和ss://格式的连接"))
        self.pushButton.setText(_translate("Dialog", "确定"))
        self.pushButton_2.setText(_translate("Dialog", "取消"))


class CenterDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.save()
        painter.drawText(option.rect, Qt.AlignCenter, str(index.data(Qt.DisplayRole)))
        painter.restore()


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
        self.tp.setIcon(QIcon('./images/logo.png'))

    def quitApp(self):
        # 退出程序
        self.w.show()  # w.hide() #设置退出时是否显示主窗口
        re = QMessageBox.question(self.w, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            self.tp.setVisible(False)  # 隐藏托盘控件
            qApp.quit()  # 退出程序

    def message(self):
        # 提示信息被点击方法
        print("弹出的信息被点击了")

    def act(self, reason):
        # 主界面显示方法
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.w.show()

    def run(self):
        a1 = QAction('&显示(Show)', triggered=self.w.show)
        a2 = QAction('&退出(Exit)', triggered=self.quitApp)
        tpMenu = QMenu()
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        self.tp.setContextMenu(tpMenu)
        self.tp.show()  # 不调用show不会显示系统托盘消息，图标隐藏无法调用

        # 信息提示
        # 参数1：标题
        # 参数2：内容
        # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
        # self.tp.showMessage('Hello', '我藏好了', icon=0)
        # 绑定提醒信息点击事件
        self.tp.messageClicked.connect(self.message)
        # 绑定托盘菜单点击事件
        self.tp.activated.connect(self.act)
        sys.exit(self.app.exec_())  # 持续对app的连接


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 订阅设置窗口
        self.subsui = QDialog()
        self.subs_child_ui = Ui_Subs_Dialog()
        self.subs_child_ui.setupUi(self.subsui)
        # 订阅配置窗口
        self.confui = QDialog()
        self.confs_child_ui = Ui_Conf_Dialog()
        self.confs_child_ui.setupUi(self.confui)
        # 获取api操作
        self.v2rayL = V2rayL()

        if self.v2rayL.auto:
            self.action_8.setChecked(True)
            self.action_9.setChecked(False)
        else:
            self.action_8.setChecked(False)
            self.action_9.setChecked(True)
        # 默认行
        self.default = 0

        # 修改toolbar按钮属性
        if self.v2rayL.current == "未连接至VPN":
            self.connect_ui.setEnabled(True)
            self.disconnect_ui.setDisabled(True)
        else:
            self.connect_ui.setDisabled(True)
            self.disconnect_ui.setEnabled(True)
        # 填充当前订阅地址
        self.subs_child_ui.lineEdit.setText(self.v2rayL.url)

        # 显示当前所有配置
        self.display_all_conf()
        self.statusbar.showMessage("当前状态: "+self.v2rayL.current+"\t\t\t\t\t\t自动更新: "+
                                   ("开启" if self.v2rayL.auto else "关闭"))

        # 开启连接线程
        self.conn_start = ConnectThread(tv=(self.tableView, self.v2rayL))
        # 断开连接线程
        self.disconn_start = DisConnectThread(tv=(self.tableView, self.v2rayL))
        # 更新线程
        self.update_addr_start = UpdateSubsThread(tv=(self.v2rayL, self.subs_child_ui))
        self.update_subs_start = UpdateSubsThread(tv=(self.v2rayL, None))

        self.ping_start = PingThread(tv=(self.tableView, self.v2rayL))
        # 事件绑定
        self.action_5.triggered.connect(self.subs_ui_show)  # 显示订阅地址窗口
        self.action_6.triggered.connect(self.update_subs)  # 更新订阅
        self.action_8.triggered.connect(self.enable_auto_update)  # 开启自动更新订阅
        self.action_9.triggered.connect(self.disable_auto_update)  # 关闭自动更新订阅
        self.action_24.triggered.connect(self.confs_ui_show)  # 显示配置窗口
        self.action_10.triggered.connect(self.output_conf)  # 导出配置文件
        self.action_11.triggered.connect(self.output_conf_by_uri)  # 生成分享链接
        self.subs_child_ui.pushButton_2.clicked.connect(self.subs_ui_hide)  # 关闭订阅地址窗口
        self.confs_child_ui.pushButton_2.clicked.connect(self.confs_ui_hide)  # 显示配置窗口
        self.subs_child_ui.pushButton.clicked.connect(self.change_subs_addr)  # 更新订阅操作
        self.confs_child_ui.pushButton.clicked.connect(self.get_conf_from_uri)  # 解析URI获取配置
        self.connect_ui.triggered.connect(self.start_conn_th)  # 绑定开启连接线程
        self.conn_start.sinOut.connect(self.alert)  # 得到连接反馈
        self.disconnect_ui.triggered.connect(self.end_conn_th)  # 绑定断开连接线程
        self.disconn_start.sinOut.connect(self.alert)  # 得到断开连接反馈
        self.tableView.doubleClicked.connect(self.start_conn_th)  # 双击配置连接
        self.delconf_ui.triggered.connect(self.del_conf)  # 移除配置
        self.update_addr_start.sinOut.connect(self.alert)  # 得到反馈
        self.update_subs_start.sinOut.connect(self.alert)   # 得到反馈
        self.ping_ui.triggered.connect(self.start_ping_th)  # 绑定ping程序
        self.ping_start.sinOut.connect(self.alert)  # 得到反馈

        # 设置最小化到托盘
        self.tray()

    def tray(self):
        # 创建托盘程序
        ti = SystemTray(self)

    def display_all_conf(self):
        """
        列出所有的可用配置
        :return:
        """
        all_conf = self.v2rayL.subs.conf
        model = QStandardItemModel(len(all_conf), 5)
        # 设置水平方向四个头标签文本内容
        model.setHorizontalHeaderLabels(['名称', '服务器地址', '服务器端口', "状态", '协议格式', '更新时间'])
        row = 0
        for k, v in all_conf.items():
            if k == self.v2rayL.current:
                self.default = row
                model.setItem(row, 3, QStandardItem("已连接"))
            else:
                model.setItem(row, 3, QStandardItem("未连接"))
            model.setItem(row, 0, QStandardItem(k))
            model.setItem(row, 1, QStandardItem(v["add"]))
            model.setItem(row, 2, QStandardItem(v["port"]))
            model.setItem(row, 4, QStandardItem(v["prot"]))
            model.setItem(row, 5, QStandardItem(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            row += 1
        self.tableView.setModel(model)
        # 设置默认选中行，未连接时为第一行，默认为已选择配置行
        self.tableView.selectRow(self.default)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 不可编辑
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 选中一列
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置背景颜色
        self.tableView.setStyleSheet("#tableView{background-color:#F2F2F2;}")
        # 除第一列不居中,其他居中
        self.tableView.setItemDelegate(CenterDelegate())
        self.tableView.setItemDelegateForColumn(0, QItemDelegate())
        #
        self.tableView.setShowGrid(False)

    def subs_ui_show(self):
        """
        显示修改订阅地址窗口
        :return:
        """
        self.subsui.show()

    def confs_ui_show(self):
        """
        显示添加配置地址窗口
        :return:
        """
        self.confui.show()

    def subs_ui_hide(self):
        """
        隐藏修改订阅地址窗口
        :return:
        """
        self.subsui.hide()

    def confs_ui_hide(self):
        """
        隐藏添加配置地址窗口
        :return:
        """
        self.confui.hide()

    def change_subs_addr(self):
        """
        更新订阅地址
        :return:
        """
        url = self.subs_child_ui.lineEdit.text()
        if not url:
            choice = QMessageBox.warning(self, "订阅地址更新", self.tr("当前订阅地址为空，继续则删除订阅地址，是否继续？"),
                                         QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if choice == QMessageBox.Ok:
                self.statusbar.showMessage("正在更新订阅地址......")
                self.update_addr_start.start()
            else:
                self.subs_child_ui.lineEdit.setText(self.v2rayL.url)
        else:
            if url == self.v2rayL.url:
                self.subs_ui_hide()
                QMessageBox.information(self, "订阅通知", self.tr("订阅地址未改变"))
            else:
                self.statusbar.showMessage("正在更新订阅地址......")
                self.update_addr_start.start()

    def update_subs(self):
        self.update_subs_start.start()

    def get_conf_from_uri(self):
        """
        通过分享链接获取配置
        :return:
        """
        uri = self.confs_child_ui.lineEdit.text()
        if not uri:
            QMessageBox.warning(self, "提示",
                                self.tr("请输入配置分享路径！"),
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            try:
                self.v2rayL.addconf(uri)
            except MyException as e:
                QMessageBox.critical(self, "错误", self.tr(e.args[0]))
            else:
                QMessageBox.information(self, "完成", self.tr("配置添加成功！"))
                self.confs_ui_hide()
                self.v2rayL = V2rayL()
                self.display_all_conf()
                self.confs_child_ui.lineEdit.setText("")

    def del_conf(self):
        row = self.tableView.currentIndex().row()
        region = self.tableView.model().item(row, 0).text()
        if self.v2rayL.current == region:
            QMessageBox.critical(self, "移除失败", self.tr("当前配置正在使用，无法移除."))
        else:
            try:
                self.v2rayL.delconf(region)
            except MyException as e:
                QMessageBox.critical(self, "移除失败", self.tr(e.args[0]))
            else:
                self.display_all_conf()

    def start_conn_th(self):
        """开启连接线程"""
        self.connect_ui.setDisabled(True)
        self.disconnect_ui.setEnabled(True)
        self.statusbar.showMessage("正在连接.......")
        self.conn_start.start()

    def end_conn_th(self):
        """开启断开连接线程"""
        self.connect_ui.setEnabled(True)
        self.disconnect_ui.setDisabled(True)
        self.statusbar.showMessage("正在断开连接.......")
        self.disconn_start.start()

    def alert(self, tp):
        """操作反馈"""
        tp, rs, ret, row = tp
        if rs == "@@OK@@":
            if tp == "conn":
                QMessageBox.information(self, "连接成功", self.tr("连接成功！当前状态: " + ret))
                self.statusbar.showMessage("当前状态: " + ret + "\t\t\t\t\t\t自动更新: " +
                                           ("开启" if self.v2rayL.auto else "关闭"))
                if self.default != row:  # 当前配置和上一次使用的不一致
                    # 上一次的更改为未连接
                    self.tableView.model().setItem(self.default, 3, QStandardItem("未连接"))
                self.tableView.model().setItem(row, 3, QStandardItem("已连接"))
                self.default = row
                self.tableView.selectRow(self.default)

            elif tp == "disconn":
                QMessageBox.information(self, "断开连接成功", self.tr("VPN连接已断开"))
                self.statusbar.showMessage("当前状态: " + ret + "\t\t\t\t\t\t自动更新: " +
                                           ("开启" if self.v2rayL.auto else "关闭"))
                self.tableView.model().setItem(self.default, 3, QStandardItem("未连接"))
                self.tableView.selectRow(self.default)

            elif tp == "addr":
                QMessageBox.information(self, "更新地址", self.tr("更新订阅地址成功"))
                self.v2rayL = V2rayL()
                self.display_all_conf()
                self.subs_ui_hide()
                self.statusbar.showMessage("当前状态: " + self.v2rayL.current + "\t\t\t\t\t\t自动更新: " +
                                           ("开启" if self.v2rayL.auto else "关闭"))

            elif tp == "update":
                QMessageBox.information(self, "订阅通知", self.tr("订阅更新完成"))
                self.v2rayL = V2rayL()
                self.display_all_conf()
                self.statusbar.showMessage("当前状态: " + self.v2rayL.current + "\t\t\t\t\t\t自动更新: " +
                                           ("开启" if self.v2rayL.auto else "关闭"))

            elif tp == "ping":
                self.statusbar.showMessage("当前状态: {}\t\t\t\t\t\t自动更新: {}\t\t\t\t\t\t延时: {}ms".format(
                                            self.v2rayL.current, ("开启" if self.v2rayL.auto else "关闭"), ret))
        else:
            QMessageBox.critical(self, "错误", self.tr(ret))

    def output_conf(self):
        """导出配置文件"""
        fileName, ok2 = QFileDialog.getSaveFileName(self,
                                                     "文件保存",
                                                     "/home",
                                                     "Json Files (*.json)")
        with open("/etc/v2rayL/config.json", "r") as f:
            tmp = f.read()
        with open(fileName, "w") as wf:
            wf.write(tmp)

        QMessageBox.information(self, "导出成功", self.tr("保存为： "+fileName))

    def enable_auto_update(self):
        self.action_8.setChecked(True)
        self.action_9.setChecked(False)
        self.v2rayL.subscribe(True)
        self.statusbar.showMessage("当前状态: " + self.v2rayL.current + "\t\t\t\t\t\t自动更新: 开启")

    def disable_auto_update(self):
        self.action_8.setChecked(False)
        self.action_9.setChecked(True)
        self.v2rayL.subscribe(False)
        self.statusbar.showMessage("当前状态: " + self.v2rayL.current + "\t\t\t\t\t\t自动更新: 关闭")

    def start_ping_th(self):
        self.ping_start.start()

    def output_conf_by_uri(self):
        row = self.tableView.currentIndex().row()
        region = self.tableView.model().item(row, 0).text()
        ret = self.v2rayL.subs.conf2b64(region)
        QMessageBox.information(self, "分享链接", self.tr(ret))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    # 显示在屏幕上
    myWin.show()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())