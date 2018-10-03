# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class UiLogin(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(341, 228)
        Form.setFixedSize(341,228)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 50, 61, 20))
        self.label.setObjectName("label")
        self.user = QtWidgets.QLineEdit(Form)
        self.user.setGeometry(QtCore.QRect(100, 50, 191, 21))
        self.user.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.user.setObjectName("user")
        self.pwd = QtWidgets.QLineEdit(Form)
        self.pwd.setGeometry(QtCore.QRect(100, 120, 191, 21))
        self.pwd.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pwd.setText("")
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd.setCursorPosition(0)
        self.pwd.setDragEnabled(False)
        self.pwd.setReadOnly(False)
        self.pwd.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.pwd.setObjectName("pwd")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 120, 54, 21))
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(100, 20, 170, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
        #self.label.setAutoFillBackground(True)
        pe.setColor(QtGui.QPalette.Window,QtCore.Qt.blue)
        # pe.setColor(QPalette.Background,Qt.blue)
        self.label_3.setPalette(pe)
        #self.label_3.setFont(QtGui.QFont("Roman times", 10, QtGui.QFont.Bold))
        self.label_3.setFrameShape(0)
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setObjectName("label_3")

        self.loginbt = QtWidgets.QPushButton(Form)
        self.loginbt.setGeometry(QtCore.QRect(120, 170, 81, 23))
        icon1 = QtGui.QIcon()
        cwd = os.getcwd()
        icon1.addPixmap(QtGui.QPixmap(cwd+"/ico/1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.loginbt.setIcon(icon1)

        self.loginbt.setAutoRepeatInterval(100)
        self.loginbt.setAutoDefault(False)
        self.loginbt.setDefault(True)
        self.loginbt.setFlat(False)
        self.loginbt.setObjectName("loginbt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "欢迎登录"))
        self.label.setText(_translate("Form", "登录名  ："))
        self.label_2.setText(_translate("Form", "密  码  ："))
        self.label_3.setText(_translate("Form", ""))
        self.loginbt.setText(_translate("Form", "登  录"))