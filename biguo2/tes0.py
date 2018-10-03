from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore,QtGui

e = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                      QtCore.QPointF(5, 5), QtCore.Qt.LeftButton,
                      QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
QtCore.QCoreApplication.sendEvent(self.label, e)
class MyEvent(QtCore.QEvent):
    idType = QtCore.QEvent.registerEventType()
    def __init__(self, data):
        QtCore.QEvent.__init__(self, MyEvent.idType)
        self.data = data
    def get_data(self):
        return self.data

QtCore.QCoreApplication.sendEvent(self.label, MyEvent("512"))

def customEvent(self, e):
    if e.type() == MyEvent.idType:
        self.setText("Received data: {0}".format(e.get_data()))
