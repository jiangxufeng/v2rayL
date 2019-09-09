# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import qtawesome


class SwitchBtn(QWidget):
    # 信号
    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, checked=False):
        super(QWidget, self).__init__(parent)
        self.checked = checked
        self.bgColorOff = QColor(169, 169, 169)
        self.bgColorOn = QColor(124, 252, 0)

        self.sliderColorOff = QColor(245,245,245)
        self.sliderColorOn = QColor(245, 245, 245)

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "OFF"
        self.textOn = "ON"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        if checked:
            self.startX = self.height()
        else:
            self.startX = 0
        self.endX = 0

        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.updateValue)  # 计时结束调用operate()方法

        #self.timer.start(5)  # 设置计时间隔并启动

        self.setFont(QFont("Microsoft Yahei", 10))

        #self.resize(55,22)

    def updateValue(self):
        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()

    def mousePressEvent(self, event):
        self.checked = not self.checked
        #发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        #状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
            # print("11111 ")
        else:
            self.endX = 0
        self.timer.start(5)

    def paintEvent(self, evt):
        #绘制准备工作, 启用反锯齿
            painter = QPainter()
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing)

            #绘制背景
            self.drawBg(evt, painter)
            #绘制滑块
            self.drawSlider(evt, painter)
            #绘制文字
            self.drawText(evt, painter)

            painter.end()

    def drawText(self, event, painter):
        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(0, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2, 0, self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()

    def drawBg(self, event, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        #半径为高度的一半
        radius = rect.height() / 2
        #圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()

    def drawSlider(self, event, painter):
        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.drawEllipse(sliderRect)

        painter.restore()


class MainUi(QMainWindow):

    def init_ui(self):
        self.setFixedSize(980, 610)
        self.main_widget = QWidget()  # 创建窗口主部件
        self.setWindowIcon(QIcon("/etc/v2rayL/images/logo.ico"))
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        self.right_widget = QWidget()  # 创建右上侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.right_down_widget = QWidget()  # 创建右下侧部件
        self.right_down_widget.setObjectName('right_down_widget')
        self.right_down_layout = QGridLayout()
        self.right_down_widget.setLayout(self.right_down_layout)  # 设置右侧部件布局为网格

        self.right_up_widget = QWidget()  # 创建右上侧部件
        self.right_up_widget.setObjectName('right_up_widget')
        self.right_up_layout = QGridLayout()
        self.right_up_widget.setLayout(self.right_up_layout)  # 设置右侧部件布局为网格

        self.right_down_widget = QWidget()  # 创建右下侧部件
        self.right_down_widget.setObjectName('right_down_widget')
        self.right_down_layout = QGridLayout()
        self.right_down_widget.setLayout(self.right_down_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        # self.main_layout.addWidget(self.right_up_widget, 0, 2, 2, 10)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.right_layout.addWidget(self.right_up_widget, 0, 0, 1, 9)
        self.right_layout.addWidget(self.right_down_widget, 1, 0, 8, 9)
        self.left_close = QPushButton("")  # 关闭按钮
        self.left_mini = QPushButton("")  # 最小化按钮

        self.left_connect_label = QPushButton("连接")
        self.left_connect_label.setObjectName('left_label')
        self.left_settings_label = QPushButton("设置")
        self.left_settings_label.setObjectName('left_label')
        self.left_help__label = QPushButton("帮助")
        self.left_help__label.setObjectName('left_label')

        self.left_button_1 = QPushButton(qtawesome.icon('fa.plug', color='black'), "可用连接")
        self.left_button_1.setObjectName('left_button')
        self.left_button_3 = QPushButton(qtawesome.icon('fa.tachometer', color='black'), "配置订阅")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QPushButton(qtawesome.icon('fa.info-circle', color='black'), "版本说明")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QPushButton(qtawesome.icon('fa.cog', color='black'), "系统设置")
        self.left_button_5.setObjectName('left_button')


        self.left_layout.addWidget(self.left_mini, 0, 1, 1, 3)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 2)
        self.left_layout.addWidget(self.left_connect_label, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_settings_label, 5, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_2, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_help__label, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 10, 0, 1, 3)


        self.right_bar_widget = QWidget()  # 右侧顶部logo部件
        self.right_bar_layout = QGridLayout()  # 右侧顶部logo网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.v2rayL_icon = QLabel()
        self.v2rayL_icon.setPixmap(QPixmap("/etc/v2rayL/images/logo.ico"))
        self.v2rayL_label = QLabel('V2rayL')
        self.v2rayL_label.setFont(qtawesome.font('fa', 24))

        self.right_bar_layout.addWidget(self.v2rayL_icon, 0, 0, 1, 4, Qt.AlignRight)
        self.right_bar_layout.addWidget(self.v2rayL_label, 0, 4, 1, 5, Qt.AlignLeft)

        self.right_up_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)
        # self.right_layout.addWidget(self.right_one_widget, 1, 0, 8, 9)

        # 顶部三个按钮Qss
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:7px;}
            QPushButton:hover{background:red;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:7px;}
            QPushButton:hover{background:green;}''')

        # 左部Qss
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
                background:#708090;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                }
        ''')

        # 右部Qss
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_up_widget.setStyleSheet('''
            QWidget#right_up_widget{
                border-bottom: 2px solid darkGray;
            }
        ''')



        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

        self.config_setting_widget = QWidget()
        self.system_setting_widget = QWidget()
        self.help_widget = QWidget()
        self.first_widget = QWidget()

        # 配置页面
        self.config_setting_ui = Ui_Setting1_Form()
        self.config_setting_ui.setupUi(self.config_setting_widget)
        self.right_down_layout.addWidget(self.config_setting_widget)

        # 系统设置页面
        self.system_setting_ui = Ui_SystemSettings()
        self.system_setting_ui.setupUi(self.system_setting_widget)
        self.right_down_layout.addWidget(self.system_setting_widget)

        # 版本说明页面
        self.help_ui = Ui_HelpUi()
        self.help_ui.setupUi(self.help_widget)
        self.right_down_layout.addWidget(self.help_widget)

        # 主页连接页面
        self.first_ui = Ui_FirstPage()
        self.first_ui.setupUi(self.first_widget)
        self.right_down_layout.addWidget(self.first_widget)

        # 分享配置窗口
        self.share_ui = QDialog()
        self.share_child_ui = Ui_Share_Dialog()
        self.share_child_ui.setupUi(self.share_ui)

        # 二维码分享配置窗口
        self.qr_ui = QDialog()
        self.qr_child_ui = Ui_Qr_Dialog()
        self.qr_child_ui.setupUi(self.qr_ui)

        self.current_page = self.first_widget
        self.config_setting_widget.hide()
        self.system_setting_widget.hide()
        self.help_widget.hide()

        self.left_mini.clicked.connect(self.on_left_mini_clicked)
        self.left_close.clicked.connect(self.on_left_close_clicked)
        self.left_button_1.clicked.connect(self.change_to_firstPage)
        self.left_button_3.clicked.connect(self.change_to_configSetting)
        self.left_button_4.clicked.connect(self.change_to_Help)
        self.left_button_5.clicked.connect(self.change_to_systemSetting)

    def change_to_firstPage(self):
        self.current_page.hide()
        self.first_widget.show()
        self.current_page = self.first_widget

    def change_to_systemSetting(self):
        self.current_page.hide()
        self.system_setting_widget.show()
        self.current_page = self.system_setting_widget

    def change_to_configSetting(self):
        self.current_page.hide()
        self.config_setting_widget.show()
        self.current_page = self.config_setting_widget

    def change_to_Help(self):
        self.current_page.hide()
        self.help_widget.show()
        self.current_page = self.help_widget

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def on_left_close_clicked(self):
        """
        关闭窗口
        """
        self.close()

    def on_left_mini_clicked(self):
        """
        最小化窗口
        """
        self.showMinimized()


class Ui_Setting1_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(796, 489)
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setGeometry(QRect(650, 350, 111, 31))
        self.pushButton_3.setStyleSheet("#pushButton_3{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
                                        "#pushButton_3:hover{ background: #5599FF;}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setGeometry(QRect(40, 350, 581, 31))
        self.lineEdit.setStyleSheet("border-style:none none solid none;\n"
                                    "background-color:transparent;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("http://或https://，可回车确认")
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(40, 320, 101, 17))
        self.label.setStyleSheet("font: 13pt \"Purisa\";")
        self.label.setObjectName("label")
        self.label_2 = QLabel(Form)
        self.label_2.setGeometry(QRect(340, 20, 51, 31))
        self.label_2.setStyleSheet("font-size: 24px;\n"
                                    "color:rgb(136, 138, 133);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(Form)
        self.label_3.setGeometry(QRect(40, 80, 67, 17))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(Form)
        self.label_4.setGeometry(QRect(40, 90, 101, 17))
        self.label_4.setStyleSheet("font: 13pt \"Purisa\";")
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setGeometry(QRect(40, 120, 431, 25))
        self.lineEdit_2.setStyleSheet("border-style:none none solid none;\n"
                                        "background-color:transparent;")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("以vmess://或ss://开头，以英文;分隔多条，回车确认")
        self.label_5 = QLabel(Form)
        self.label_5.setGeometry(QRect(570, 90, 131, 21))
        self.label_5.setStyleSheet("font: 13pt \"Purisa\";")
        self.label_5.setObjectName("label_5")
        self.pushButton = QPushButton(Form)
        self.pushButton.setGeometry(QRect(570, 120, 171, 31))
        self.pushButton.setStyleSheet("#pushButton{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
                                      "#pushButton:hover{ background: #5599FF;}")
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QLabel(Form)
        self.label_6.setGeometry(QRect(40, 190, 141, 21))
        self.label_6.setStyleSheet("font: 13pt \"Purisa\";\n")
        self.label_6.setObjectName("label_6")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setGeometry(QRect(210, 184, 171, 31))
        self.pushButton_2.setStyleSheet("#pushButton_2{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
                                        "#pushButton_2:hover{ background: #5599FF;}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_7 = QLabel(Form)
        self.label_7.setGeometry(QRect(340, 260, 51, 31))
        self.label_7.setStyleSheet("font-size: 24px;\n"
                                    "color:rgb(136, 138, 133);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QLabel(Form)
        self.label_8.setGeometry(QRect(40, 415, 201, 17))
        self.label_8.setStyleSheet("font: 13pt \"Purisa\";")
        self.label_8.setObjectName("label_8")
        self.line = QFrame(Form)
        self.line.setGeometry(QRect(40, 140, 441, 16))
        self.line.setStyleSheet("")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QFrame(Form)
        self.line_2.setGeometry(QRect(40, 370, 581, 16))
        self.line_2.setStyleSheet("")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_9 = QLabel(Form)
        self.label_9.setGeometry(QRect(250, 410, 201, 71))
        self.label_9.setObjectName("label_9")

        self.switchBtn = SwitchBtn(self.label_9)
        self.switchBtn.setGeometry(0, 0, 60, 30)


        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "更新地址"))
        self.label.setText(_translate("Form", "当前订阅地址"))
        self.label_2.setText(_translate("Form", "配置"))
        self.label_4.setText(_translate("Form", "通过URI添加"))
        self.label_5.setText(_translate("Form", "通过二维码添加"))
        self.pushButton.setText(_translate("Form", "点击选择二维码"))
        self.label_6.setText(_translate("Form", "导出当前完整配置"))
        self.pushButton_2.setText(_translate("Form", "选择保存地址"))
        self.label_7.setText(_translate("Form", "订阅"))
        self.label_8.setText(_translate("Form", "程序启动时自动更新订阅"))


class Ui_SystemSettings(object):
    def setupUi(self, SystemSettings):
        SystemSettings.setObjectName("SystemSettings")
        SystemSettings.resize(796, 489)
        self.label = QLabel(SystemSettings)
        self.label.setGeometry(QRect(310, 40, 101, 31))
        self.label.setStyleSheet("font-size: 24px;\n"
                                 "color:rgb(136, 138, 133);")
        self.label.setObjectName("label")
        self.label_2 = QLabel(SystemSettings)
        self.label_2.setGeometry(QRect(60, 130, 67, 17))
        self.label_2.setStyleSheet("font: 14pt \"Purisa\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(SystemSettings)
        self.label_3.setGeometry(QRect(450, 130, 67, 17))
        self.label_3.setStyleSheet("font: 14pt \"Purisa\";")
        self.label_3.setObjectName("label_3")
        # self.socks_spinBox = QSpinBox(SystemSettings)
        # self.socks_spinBox.setGeometry(QRect(530, 120, 131, 31))
        # self.socks_spinBox.setMinimum(1080)
        # self.socks_spinBox.setMaximum(10000)
        # self.socks_spinBox.setObjectName("socks_spinBox")
        # self.socks_spinBox_2 = QSpinBox(SystemSettings)
        # self.socks_spinBox_2.setGeometry(QRect(150, 120, 131, 31))
        # self.socks_spinBox_2.setMinimum(1080)
        # self.socks_spinBox_2.setMaximum(10000)
        # self.socks_spinBox_2.setObjectName("socks_spinBox_2")
        self.label_4 = QLabel(SystemSettings)
        self.label_4.setGeometry(QRect(310, 230, 101, 31))
        self.label_4.setStyleSheet("font-size: 24px;\n"
                                   "color:rgb(136, 138, 133);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QLabel(SystemSettings)
        self.label_5.setGeometry(QRect(60, 320, 101, 21))
        self.label_5.setStyleSheet("font: 13pt \"Purisa\";")
        self.label_5.setObjectName("label_5")
        self.version_label = QLabel(SystemSettings)
        self.version_label.setGeometry(QRect(160, 320, 67, 17))
        self.version_label.setStyleSheet("font: 13pt \"Purisa\";")
        self.version_label.setObjectName("version_label")
        self.checkupdateButton = QPushButton(SystemSettings)
        self.checkupdateButton.setGeometry(QRect(290, 314, 151, 31))
        self.checkupdateButton.setStyleSheet("#checkupdateButton{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
                                             "#checkupdateButton:hover{ background: #5599FF;}")
        self.checkupdateButton.setObjectName("checkupdateButton")
        self.label_7 = QLabel(SystemSettings)
        self.label_7.setGeometry(QRect(60, 380, 231, 21))
        self.label_7.setStyleSheet("font: 13pt \"Purisa\";")
        self.label_7.setObjectName("label_7")
        self.label_6 = QLabel(SystemSettings)
        self.label_6.setGeometry(QRect(60, 170, 461, 17))
        self.label_6.setStyleSheet("font: 10pt \"Purisa\";\n"
                                    "color: rgb(186, 189, 182);")
        self.label_6.setObjectName("label_6")
        self.label_8 = QLabel(SystemSettings)
        self.label_8.setGeometry(QRect(320, 375, 201, 71))
        self.label_8.setObjectName("label_8")

        self.label_9 = QLabel(SystemSettings)
        self.label_9.setGeometry(QRect(130, 130, 67, 17))
        self.label_9.setStyleSheet("font: 14pt \"Purisa\";")
        self.label_9.setObjectName("label_9")

        self.label_10 = QLabel(SystemSettings)
        self.label_10.setGeometry(QRect(525, 130, 67, 17))
        self.label_10.setStyleSheet("font: 14pt \"Purisa\";")
        self.label_10.setObjectName("label_10")

        self.switchBtn = SwitchBtn(self.label_8, True)
        self.switchBtn.setGeometry(0, 0, 60, 30)

        self.retranslateUi(SystemSettings)
        QMetaObject.connectSlotsByName(SystemSettings)

    def retranslateUi(self, SystemSettings):
        _translate = QCoreApplication.translate
        SystemSettings.setWindowTitle(_translate("SystemSettings", "Form"))

        self.label.setText(_translate("SystemSettings", "本地端口"))
        self.label_2.setText(_translate("SystemSettings", "Http："))
        self.label_3.setText(_translate("SystemSettings", "Socks："))
        self.label_4.setText(_translate("SystemSettings", "版本更新"))
        self.label_5.setText(_translate("SystemSettings", "当前版本："))
        self.version_label.setText(_translate("SystemSettings", "v2.0.3"))
        self.checkupdateButton.setText(_translate("SystemSettings", "检查更新"))
        self.label_7.setText(_translate("SystemSettings", "程序启动时自动进行检查更新"))
        self.label_6.setText(_translate("SystemSettings", "**端口可选范围：1080-10000"))
        self.label_9.setText(_translate("SystemSettings", "1081"))
        self.label_10.setText(_translate("SystemSettings", "1080"))


class Ui_HelpUi(object):
    def setupUi(self, HelpUi):
        HelpUi.setObjectName("HelpUi")
        HelpUi.resize(796, 489)
        self.label_3 = QLabel(HelpUi)
        self.label_3.setGeometry(QRect(40, 40, 611, 231))
        self.label_3.setObjectName("label_3")
        self.label = QLabel(HelpUi)
        self.label.setGeometry(QRect(130, 260, 481, 171))
        self.label.setObjectName("label")

        self.retranslateUi(HelpUi)
        QMetaObject.connectSlotsByName(HelpUi)

    def retranslateUi(self, HelpUi):
        _translate = QCoreApplication.translate
        HelpUi.setWindowTitle(_translate("HelpUi", "Form"))
        self.label_3.setWhatsThis(_translate("HelpUi", "<html><head/><body><p><br/></p></body></html>"))
        self.label_3.setText(_translate("HelpUi", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">当前版本</span></p>\n"
        "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">——————————————————————</span></p>\n"
        "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">v2.0.2</span></p>\n"
        "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
        "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">说明</span></p>\n"
        "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">——————————————————————</span></p></body></html>"))
        self.label.setText(_translate("HelpUi", "1. 具有全新的V2rayL UI\n"
        "2. github地址：https://github.com/jiangxufeng/v2rayL\n"
        "3. 目前支持协议有：Vmess、shadowsocks\n"
        "4. 支持通过分享链接、二维码导入和分享配置\n"
        "5. 程序可能存在未测试到的Bug，使用过程中发现Bug请在github提交"))


class CenterDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.save()
        painter.drawText(option.rect, Qt.AlignCenter, str(index.data(Qt.DisplayRole)))
        painter.restore()


class Ui_FirstPage(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.tableWidget = QTableWidget(Form)
        self.tableWidget.setGeometry(QRect(0, 60, 770, 320))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        # self.tableWidget.setRowCount(12)
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(130, 30, 41, 21))
        self.label.setStyleSheet('font: 75 14pt "宋体";font-weight:bold;')
        self.label.setObjectName("label")
        self.label_2 = QLabel(Form)
        self.label_2.setGeometry(QRect(335, 30, 41, 21))
        self.label_2.setStyleSheet('font: 75 14pt "宋体";font-weight:bold;')
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(Form)
        self.label_3.setGeometry(QRect(490, 30, 41, 21))
        self.label_3.setStyleSheet('font: 75 14pt "宋体";font-weight:bold;')
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(Form)
        self.label_4.setGeometry(QRect(15, 30, 41, 21))
        self.label_4.setStyleSheet('font: 75 14pt "宋体";font-weight:bold;')
        self.label_4.setObjectName("label_4")
        self.pushButton = QPushButton(Form)
        self.pushButton.setGeometry(QRect(200, 400, 111, 31))
        self.pushButton.setStyleSheet(
            "#pushButton{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
            "#pushButton:hover{ background: #5599FF;}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_1 = QPushButton(Form)
        self.pushButton_1.setGeometry(QRect(360, 400, 130, 31))
        self.pushButton_1.setStyleSheet(
            "#pushButton_1{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
            "#pushButton_1:hover{ background: #5599FF;}")
        self.pushButton_1.setObjectName("pushButton_1")
        self.time = QLabel(Form)
        self.time.setGeometry(QRect(510, 400, 100, 31))
        self.time.setStyleSheet('font: 75 11pt "宋体";font-weight:bold;')
        self.time.setObjectName("time")

        self.tableWidget.setShowGrid(False)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setItemDelegate(CenterDelegate())
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnWidth(0, 12)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 80)
        self.tableWidget.setColumnWidth(5, 50)
        self.tableWidget.setColumnWidth(6, 50)
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.setStyleSheet('''
            #tableWidget{
                selection-background-color:white;
            }

        ''')

        self.tableWidget.verticalScrollBar().setStyleSheet(
          "QScrollBar{background:transparent; width: 12px;}"
         "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
         "QScrollBar::handle:hover{background:gray;}"
         "QScrollBar::sub-line{background:transparent;}"
         "QScrollBar::add-line{background:transparent;}")

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def add_item(self, args):
        item = QTableWidgetItem(str(args[0]))
        self.tableWidget.setItem(args[0]-1, 0, item)
        item = QTableWidgetItem(args[1])
        self.tableWidget.setItem(args[0]-1, 1, item)
        item = QTableWidgetItem(args[2])
        self.tableWidget.setItem(args[0]-1, 2, item)
        item = QTableWidgetItem(args[3])
        self.tableWidget.setItem(args[0]-1, 3, item)
        label_1 = QLabel()
        if args[4]:
            switchBtn = SwitchBtn(label_1, True)
        else:
            switchBtn = SwitchBtn(label_1, False)
        switchBtn.setGeometry(20, 5, 60, 30)
        switchBtn.checkedChanged.connect(lambda: args[5](args[0]-1, not switchBtn.checked))
        self.tableWidget.setCellWidget(args[0]-1, 4, label_1)
        button1 = QPushButton("删除")
        button1.setObjectName("delbt")
        button1.setStyleSheet('''
            #delbt{border-width: 0px; 
            border-radius: 15px; 
            background: red; 
            outline: none; 
            font-family: Microsoft YaHei; 
            color: white; 
            font-size: 13px; 
            margin:5px;
            }
            #delbt:hover{ background: #FF6347;}
        ''')
        button1.clicked.connect(lambda: args[6](args[0]-1))
        self.tableWidget.setCellWidget(args[0]-1, 5, button1)
        button2 = QPushButton("分享")
        button2.setObjectName("delbt")
        button2.setStyleSheet('''
            #delbt{border-width: 0px; 
            border-radius: 15px; 
            background: #1E90FF; 
            outline: none; 
            font-family: Microsoft YaHei; 
            color: white; 
            font-size: 13px; 
            margin:5px;
            }
            #delbt:hover{ background: #5599FF;}
        ''')
        button2.clicked.connect(lambda: args[7](args[1]))
        self.tableWidget.setCellWidget(args[0]-1, 6, button2)



    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "名称"))
        self.label_2.setText(_translate("Form", "地址"))
        self.label_3.setText(_translate("Form", "协议"))
        self.label_4.setText(_translate("Form", "序号"))
        self.pushButton.setText(_translate("Form", "更新订阅"))
        self.pushButton_1.setText(_translate("Form", "测试当前延时"))


class Ui_Share_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(226, 171)
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(20, 20, 191, 17))
        self.label.setStyleSheet("font: 75 13pt \"新宋体\";")
        self.label.setObjectName("label")
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(40, 60, 141, 31))
        self.pushButton.setStyleSheet("#pushButton{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
        "#pushButton:hover{ background: #5599FF;}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setGeometry(QRect(40, 110, 141, 31))
        self.pushButton_2.setStyleSheet("#pushButton_2{border-width: 0px; border-radius: 15px; background: #1E90FF; outline: none; font-family: Microsoft YaHei; color: white; font-size: 13px; }\n"
        "#pushButton_2:hover{ background: #5599FF;}")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "配置分享"))
        self.label.setText(_translate("Dialog", "请选择以下一种方式分享"))
        self.pushButton.setText(_translate("Dialog", "二维码分享"))
        self.pushButton_2.setText(_translate("Dialog", "链接分享"))


class Ui_Qr_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(218, 218)
        Dialog.setMinimumSize(QSize(218, 218))
        Dialog.setMaximumSize(QSize(218, 218))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QLabel(Dialog)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QSize(200, 200))
        self.label.setMaximumSize(QSize(200, 200))
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "二维码分享配置"))

def main():
    app = QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



