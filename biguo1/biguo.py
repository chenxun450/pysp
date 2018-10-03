# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'biguo.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

import os
import re
import sys
import time
import xlwt

import win32com.client
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal,Qt
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication


def write_xlsx(fpath,fname, con_list):
    #print os.getcwd()
    fpath = fpath + "/excel/"
    if not os.path.exists(fpath):
        os.mkdir(fpath)
    # print type(fname),fname
    filename = fname + '.xlsx'
    path = os.path.join(fpath, filename)

    if not os.path.exists(path):
        try:
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
            for i in range(len(con_list)):
                for j in range(0,11):
                    worksheet.write(i,j,con_list[i][j])

            workbook.save(path)
            print('写入excel完毕!')
        except Exception as e:
            print(e)
        finally:
            pass
    else:
        print('文件已存在')


class Signal1(QObject):
    display_li = pyqtSignal()


class Ui_MainWindow(object):
    def setupUi(self, QUnFrameWindow):
        self.text = ''
        self.flag1 = 0
        self.file_li = []
        QUnFrameWindow.setObjectName("MainWindow")
        QUnFrameWindow.resize(468, 347)
        QUnFrameWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint)
        #MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #MainWindow.setStyleSheet('''background-color:cyan;''')
        QUnFrameWindow.setFixedSize(QUnFrameWindow.width(), QUnFrameWindow.height())
        QUnFrameWindow.setUnifiedTitleAndToolBarOnMac(False)
        QUnFrameWindow.setWindowIcon(QIcon("2.ico"))

        # 设置控件
        self.centralwidget = QtWidgets.QWidget(QUnFrameWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(370, 200, 75, 23))
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(150, 200, 156, 23))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Open)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 471, 191))
        self.listWidget.setObjectName("listWidget_1")
        self.processBar = QtWidgets.QProgressBar(self.centralwidget)
        self.processBar.setGeometry(QtCore.QRect(22, 240, 447, 23))
        self.processBar.setProperty("value", 0)
        #self.processBar.setVisible(False)
        self.processBar.setObjectName("progressBar")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(20, 200, 71, 24))
        self.toolButton.setObjectName("toolButton")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(20,280,427,40)
        self.label1.setFrameStyle(6)
        self.label1.setFont(QFont("Microsoft Yahei",15,QFont.Bold))
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setText("笔果试题工具")

        QUnFrameWindow.setCentralWidget(self.centralwidget)

        # 自定义信号
        self.s = Signal1()
        self.s.display_li.connect(self.display_str)

        self.retranslateUi(QUnFrameWindow)

        # 信号与槽设置
        self.buttonBox.accepted.connect(QUnFrameWindow.openbut_click)
        self.buttonBox.clicked.connect(QUnFrameWindow.applybut_click)
        self.pushButton_2.clicked.connect(QUnFrameWindow.transform)
        self.toolButton.clicked.connect(QUnFrameWindow.get_doc_dialog)

        QtCore.QMetaObject.connectSlotsByName(QUnFrameWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "笔果试题转换器"))
        self.pushButton_2.setText(_translate("MainWindow", "转 换"))
        self.toolButton.setText(_translate("MainWindow", "选取文档"))

    def display_str(self):
        self.listWidget.clear()
        self.listWidget.addItems(self.file_li)


    def openbut_click(self):
        print("1")

    def applybut_click(self):
        print("2")

    def h3(self):
        print("3")

    def transform(self):
        self.processBar.setVisible(True)
        self.pushButton_2.setDisabled(True)
        self.processBar.setValue(0)
        self.label1.clear()
        self.label1.setText("转换中...")

        for file in self.file_li:
            fpath,fnameex = os.path.split(file)
            fname = re.sub('\.[a-zA-Z0-9]{2,4}','',fnameex)
            self.doc2str(self.upd_path(file))
            print(fpath,fname)
            time.sleep(0.1)
            try:
                with open(fpath+"/cache/"+fname+".txt","r") as f:
                    text = f.read()
                p = Paper(fname,text)

                if p.flag:
                    write_xlsx(fpath,fname,p.array)
            except Exception as e:
                self.text = repr(e)
                self.label1.setText(self.text)
            self.flag1 += 100/len(self.file_li)
            self.processBar.setValue(self.flag1)
        self.pushButton_2.setDisabled(False)
        if not self.text:
            self.processBar.setValue(100)
            self.label1.setText("笔果试题工具")

    def dir(self):
        print("helloworld")
        pwd = os.getcwd()
        print(pwd)
        li = os.listdir(pwd)
        li1 = [x for x in li if x.endswith(".doc|.docx")]
        print(li1)

    def process(self):
        self.processBar.setValue(self.flag1)

    def get_doc_dialog(self):
        self.file_li, a = QFileDialog.getOpenFileNames(self, 'Open file', "D:\\", "word(*.doc;*.docx;*.wps)")
        self.s.display_li.emit()

    @staticmethod  # pywin32 模块
    def doc2str(fpath):
        wordapp = win32com.client.Dispatch("Word.Application")
        wordapp.Visible = 0  # 后台运行
        wordapp.DisplayAlerts = 0
        doc = wordapp.Documents.Open(fpath)

        # 按照 路径 文件名 带后缀文件名, path0 fname fnameex
        path0, fnameex = os.path.split(fpath)
        fname = re.sub("\.docx|\.doc|\.wps", '', fnameex)

        if not os.path.exists(path0 + "\cache"):
            os.mkdir(path0 + "\cache")
        doc.SaveAs(path0 + "\cache\\" + fname+".txt", 4)

        # content = '\n'.join([para.Range.text for para in doc.paragraphs])

        doc.Close()  # 关闭word文档
        wordapp.Quit()  # 关闭word程序

    @staticmethod
    def upd_path(path):
        return path.replace('/', "\\")

# 试题提取
class Paper():
    def __init__(self, fname, text):
        self.paper_name1 = fname
        self.paper_name2 = ""
        text = re.sub("(?<=\D)\n(\d+)。","\n\g<1>.",text)
        text = re.sub("\n.{0,10}第二部分.{0,10}\n", '\n', text)
        self.all_text = re.sub("(\n\d)O","\g<1>0",text)
        self.paper_cls = 1
        self.cls1 = ''
        self.cls2 = ''
        self.cls4 = []

        self.option_dict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
        self.big_dict = {"一、": 1, "二、": 2, "三、": 3, "四、": 4, "五、": 5, "六、": 6, "七、": 7, "八、": 8, "九、": 9, "十、": 10,"一.": 1, "二.": 2, "三.": 3, "四.": 4, "五.": 5, "六.": 6, "七.": 7, "八.": 8, "九.": 9, "十.": 10,"一．": 1, "二．": 2, "三．": 3, "四．": 4, "五．": 5, "六．": 6, "七．": 7, "八．": 8, "九．": 9, "十．": 10}

       # 大题题号正则
        self.big_sep = re.compile("^一[、.．]|(?<=\n)(?:一[、.．]|二[、.．]|三[、.．]|四[、.．]|五[、.．]|六[、.．]|七[、.．]|八[、.．]|九[、.．]|十[、.．])")
        # 小题题号正则匹配
        self.small_sep = re.compile("(?<=\n)\d{1,2}[、.．,，](?=[\u4E00-\u9FA5]?.{1,10}\d{0,4}[\u4E00-\u9FA5])")
        self.find_sep = re.compile("(?<=\n)\d{1,2}([、.．,，])(?=[\u4E00-\u9FA5]?.{1,10}\d{0,4}[\u4E00-\u9FA5])")
        self.flag = 0
        # 选择题答案正则匹配
        self.option_sep = re.compile("([\(（【]).{0,4}?[A-F]{1,6}.{0,4}?([\)）】])|正确答案[:：]?.{0,2}?[A-F]{1,6}|答案[:：]?.{0,2}?[A-F]{1,6}|答[:：]{0,2}?[A-F]{1,6}")
        self.answer_sep = re.compile("[\(（【].{0,4}?[A-F]{1,6}.{0,4}?[\)）】]|正确答案[:：]?.{0,2}?[A-F]{1,6}|答案[:：]?.{0,2}?[A-F]{1,6}|答[:：]{0,2}?[A-F]{1,6}")

        self.array = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]

        self.bigs_q()

    def bigs_q(self):  # 大题处理
        li = []
        for item in self.big_sep.split(self.all_text):
            if not len(self.small_sep.findall(item)): # item 中没找到小题,则
                if not len(re.findall("(\d{1,4}年\d{1,2}月)?[\u4E00-\u9FA5]{1,15}[试真]题", item)):
                    pass
                else:
                    self.paper_name2 = re.findall("(\d{1,4}年\d{1,2}月)?[\u4E00-\u9FA5]{1,15}[试真]题", item)[0]
            else:
                li.append(item)
        li1 = self.big_sep.findall(self.all_text)

        for i, item in enumerate(li1):  # 判断大题题号是否有错漏
            if self.big_dict[li1[i]] != i + 1:
                raise Exception("大题题号有错误，请检查")

        for i,item in enumerate(li):  # 分割大题s,加到li列表中
            if re.search("单项选择|单选", item[0:8]):
                self.cls1 = item
            elif re.search("多项选择|多选", item[0:8]):
                self.cls2 = item
            else:
                self.cls4.append(item)
        self.choice_q()
        self.essay_q()
        print(">>>")
        self.flag = 1

    def choice_q(self):  # 选择题处理
        # 单选
        self.init_li(self.cls1,1)
        # 多选
        self.init_li(self.cls2,2)

    def essay_q(self):
        for item in self.cls4:
            if re.search("判断", item[0:7]):
                self.init_li2(item,3)
            elif re.search("填空",item[0:7]):
                self.init_li2(item,4)
            elif re.search("名词解释",item[0:8]):
                self.init_li2(item,4)
            else:
                self.init_li2(item,4)

    def init_li2(self,big,cls):  # 问答题 的处理
        # 获得题号列表
        li = [i for i in re.findall("(?<=\n)(\d{1,2})[、.．,，](?=[\u4E00-\u9FA5]?.{1,4}\d{0,4}[\u4E00-\u9FA5])", big) if int(i) > len(self.array)-2]
        li = li + [i for i in re.findall("(?<=\n)(\d{1,2})[、.．,，][a-zA-Z]{1,5}",big) if int(i) > len(self.array)-2]
        li.insert(0,'\\&//')
        li1 = re.split('|\n'.join(li), big)[1:]  # 用题号切割成小题,会导致带着题号中的符号
        for each in li1:

            each = each.lstrip("、.．,， ")
            empty_li = self.empty_li()

            if len(re.findall("解释[:：]|解析[:：]", each)): # 有解析  则
                lis = [x for x in re.split("解释[:：]|解析[:：]", each) if x not in ' \n']
                each = lis[0]
                empty_li[10] = lis[1]

            if not len(re.findall("\n答[：:]|\n答案[：:]",each)):# 没有答案 则
                # if len(re.findall("\n", each)) in range(1,5):
                #     if len(re.findall("\n[（(](.{1,20})[)）]",each)) and cls != 4:
                #         li2 = [x for x in re.split("\n[（(](.{1,20})[)）]", each,2) if x not in ' \n']
                #     else:
                #         li2 = [x for x in re.split("\n", each,2) if x not in ' \n']
                #
                #     if len(li2) == 1:
                #         empty_li[2] = li2[0]
                #     elif len(li2) == 2:
                #         empty_li[2] = re.sub("[（(]本题l?\d+分[)）]","",li2[0])
                #         empty_li[9] = li2[1]
                #     elif len(li2) == 3:
                #         empty_li[2] = li2[0]
                #         empty_li[9] = li2[1] + li2[2]
                # else:
                empty_li[2] = re.sub("[（(]本题l?\d+分[)）]","",each)
            else:
                empty_li[2], empty_li[9] = re.split("\n答[：:]|\n答案[：:]", each)
                empty_li[2] = re.sub("[（(]本题l?\d+分[)）]","",empty_li[2])
            empty_li[1] = cls
            empty_li[0] = len(self.array)
            self.array.append(empty_li)

    def init_li(self, big,cls):  # 切割小题，获取到一个列表

        for each in self.small_sep.split(big)[1:]:
            each = re.sub("\n",'',each)
            li = self.empty_li()
            if self.answer_sep.search(each):
                answer = re.search("[A-L]{1,6}", self.answer_sep.search(each).group(0)).group(0)
                each = self.option_sep.sub('\g<1>\g<2>', each)
            else:
                answer = ''
            li1 = re.findall("([A-F])[、.．,，]", each)
            if not len(li1):  # 判断选项是否有错漏
                li2 = re.findall("([A-F])[、.．,，]?", each)
                if len(li2) >= 0:
                    for i, item in enumerate(li2):
                        if self.option_dict[li2[i]] != i + 1:
                            self.print_txt = "注意！有选择题选项有问题"
                for i, x in enumerate(re.split("[A-F][、.．,，。]?", each)):  # 根据选项对小题分割
                    if i > 6:
                        self.print_txt = "注意!选项过多,请注意检查"
                        continue
                    if not len(re.findall("解释[:：]|解析[:：]",x)):  # 判断是否有解析
                        a,b = re.split("解释[:：]|解析[:：]", x)
                        li[i + 2], li[10] = a.strip(),b.strip()
                    else:
                        li[i + 2] = x.strip()
                    li[9] = answer.strip()
                else:
                    self.print_txt = "注意,该题未获取到选项"
            else:
                for i, item in enumerate(li1):
                    if self.option_dict[li1[i]] != i + 1:
                        self.print_txt = "注意！有选择题选项有问题"
                for i, x in enumerate(re.split("[A-F][、.．,，]", each)):  # 根据选项对小题分割
                    if len(re.findall("解释[:：]|解析[:：]",x)):  # 判断是否有解析
                        a, b = re.split("解释[:：]|解析[:：]", x)
                        li[i + 2], li[10] = a.strip(), b.strip()
                    else:
                        li[i + 2] = x.strip()
                    li[9] = answer.strip()
            li[0] = len(self.array)
            li[1] = cls
            self.array.append(li)

    @staticmethod
    def empty_li():
        array = ['' for i in range(11)]
        return array


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = MyMainWindow()
    mywin.show()
    sys.exit(app.exec())
