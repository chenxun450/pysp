# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setall.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class UiSetall(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(342, 228)
        self.randua = QtWidgets.QCheckBox(Form)
        self.randua.setGeometry(QtCore.QRect(30, 30, 71, 21))
        self.randua.setObjectName("randua")
        self.randproxy = QtWidgets.QCheckBox(Form)
        self.randproxy.setGeometry(QtCore.QRect(120, 30, 71, 21))
        self.randproxy.setObjectName("randproxy")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(130, 180, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "爬取设置"))
        self.randua.setText(_translate("Form", "随机UA"))
        self.randproxy.setText(_translate("Form", "随机代理"))
        self.pushButton.setText(_translate("Form", "确  定"))

