# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subject.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class UiSubject(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(327, 195)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 70, 71, 21))
        self.label.setObjectName("label")
        self.subname = QtWidgets.QLineEdit(Form)
        self.subname.setGeometry(QtCore.QRect(110, 70, 151, 20))
        self.subname.setObjectName("subname")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 71, 21))
        self.label_2.setObjectName("label_2")
        self.subcode = QtWidgets.QLineEdit(Form)
        self.subcode.setGeometry(QtCore.QRect(110, 110, 151, 21))
        self.subcode.setObjectName("subcode")
        self.subcode.setInputMask('')
        # self.oksubbt = QtWidgets.QPushButton(Form)
        # self.oksubbt.setGeometry(QtCore.QRect(130, 160, 75, 23))
        # self.oksubbt.setObjectName("oksubbt")
        self.btbox = QtWidgets.QDialogButtonBox(Form)
        self.btbox.setGeometry(QtCore.QRect(130, 160, 75, 23))
        self.btbox.setOrientation(QtCore.Qt.Horizontal)
        self.btbox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.btbox.accepted.connect(self.accept)
        self.btbox.rejected.connect(self.reject)
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(60, 20, 51, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(190, 20, 51, 16))
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "确认科目"))
        self.label.setText(_translate("Form", "科目名称 ："))
        self.label_2.setText(_translate("Form", "科目代码 ："))
        #self.oksubbt.setText(_translate("Form", "确  定"))
        self.radioButton.setText(_translate("Form", "专科"))
        self.radioButton_2.setText(_translate("Form", "本科"))

    def sendcode(self):
        pass