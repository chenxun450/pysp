# coding:utf-8
import os,re
import sys,time
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QMenu,QMessageBox,QListWidget,QDialog
from PyQt5 import QtCore,QtGui
from biguo2.login import UiLogin
from biguo2.tkspider import UiMainWindow
from biguo2.subject import UiSubject
from biguo2.setall import UiSetall
import threading as tr
import requests
from biguo2.tkspiders.wantikuapp import wantiku
from requests_toolbelt.multipart import MultipartEncoder
from bs4 import BeautifulSoup as bs
import csv,jieba,lxml,copy

cwd = os.getcwd()         # 获取运行目录的路径
def num2str(num):         # 科目代码转换 ，设置为始终5位数字的字符串，不到5位用0代替
    if len(num)<5:
        b = ""
        for a in range(5):
            if 5 - a > len(num):
                b = b + "0"
            else:
                return b + num
    else:
        return num


filename = cwd + "/courses.csv"
try:                                  ##########
    with open(filename) as f:         # 读取配置#
        reader = csv.reader(f)        # 文件的科#
        codeli = list(reader)         # 目代码  #
                                      ##########
    csvli1 = [item[2:0:-1] for item in codeli]
    # csvli: [['name', 'code'], ["['思想', '道德修养', '法律', '基础', '思想道德修养与法律基础']", '03706'],
except Exception as e:
    print(e)

def func1(sinal): # 暂代函数 funcdict
    pass
def func2(sinal):
    pass
def func3(sinal):
    pass
def func4(sinal):
    pass
def func5(sinal):
    pass
def func6(sinal):
    pass


funcdict = {0:wantiku, 1:func1, 2:func2, 3:func3, 4:func4, 5:func5, 6:func6}
# post 登录请求头,会保存 cookie
headers2 = {
    #"X-CSRF-TOKEN":"9HJB9MwNrmPvV1rnbbpi021YIeHuLGzxe9D0S8Yl",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    #"Cookie":"XSRF-TOKEN=eyJpdiI6Im4yRVwvTlA2RExzYXllV1BcL3I1SERsQT09IiwidmFsdWUiOiJ1b0x5WnF6bkI2bUNveENvdmlPK2ZaeEpcL1BJVXB1b3hQV1NLVlNUdGhxdWJZSXFFUjN3M2RRRFwvaUNZVzFBVWF3NURjVmJGYVwvUzl3NzJOQndvMkUrdz09IiwibWFjIjoiMWNhYjRjMTQ5YmExZjlkZmFjZGM2MTJmZDRhMDBlN2M0YTRlZWQzMTE5NGZmNDM5ZGNhNjYxN2U4YTUwMDM4OSJ9; laravel_session=wvGGZsyHrxYeGkXyzH1L5jOgdAMVRiAXbEMbxUAJ"
    }
boundary='----WebKitFormBoundaryetr1Sq6VzYVCK9H5'
url = "https://www.biguotk.com/admin/login/20186663312"
csrfli = [0]


class LoginW(QWidget,UiLogin):  #登录窗口
    flag = 0
    def __init__(self):
        super(LoginW, self).__init__()
        self.setupUi(self)
        res = requests.get('https://www.biguotk.com/admin/login/20186663312',headers=headers2,verify=False)
        headers2["Cookie"] = ';'.join(['='.join(each) for each in res.cookies.items()])
        soup = bs(res.text)                                                              # 用来做登录的cookie
        csrfli[0] = soup.select("meta[name='csrf-token']")[0].get('content') # 获取x-csrf-token

    def clear_(self):
        self.label_3.setText('')

    def closeLoginW(self):
        self.close()

    def login(self):
        self.label_3.clear()
        self.label_3.setText("登录中")
        data = {"account":self.user.text(),"password":  self.pwd.text(),}
        try:
            hd = headers2.copy()
            hd["X-CSRF-TOKEN"] = csrfli[0]
            res = requests.post(url,data=data,headers=hd,verify=False)
            if dict(res.json())["result_info"] == '\u767b\u9646\u6210\u529f':
                mainW.show()
                headers2["Cookie"] = ';'.join(['='.join(each) for each in res.cookies.items()])  # 获取cookie 并添加到headers2 中
                self.close()
                mainW.userlabel.setText("用户："+self.user.text())
                mainW.cookies = res.cookies
            else:
                self.label_3.clear()
                self.label_3.setText("用户名或密码错误")
        except Exception as e:
            print(e)

    @QtCore.pyqtSlot()
    def on_loginbt_clicked(self):
        self.login()

    def mousePressEvent(self, QMouseEvent):
        self.label_3.setText('')

    def keyPressEvent(self, QKeyEvent): #按enter键 触发事件
        if QKeyEvent.key() in [16777220,16777221,QtCore.Qt.Key_Enter]:
            self.login()

class TkW(QMainWindow,UiMainWindow,):   # 主窗口
    def __init__(self):
        super(TkW, self).__init__()
        self.setupUi(self)
        self.setallw = SetW()
        self.signal1 = tr.Event()
        self.cbli = [False,False,False,False,False,False,False]  # ***
        self.selectli = []              #选择的爬虫 列表 下标值
        self.lwli = [self.listWidget_1, self.listWidget_2, self.listWidget_3, self.listWidget_4, self.listWidget_5,
                     self.listWidget_6, self.listWidget_7]
                                        # listwidget列表对应下标  ***
        # sys.stdout = EmittingStream()
        # sys.stderr = EmittingStream()
        # sys.stdout.textWritten.connect(self.normalOutputWritten)
        # sys.stderr.textWritten.connect(self.normalOutputWritten)
        #self.subw = SubW()

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def set_spider(self):               # 设置窗口
        self.setallw.show()
        self.setallw.setFocus()

    def cbedit1(self,e):    # 设置多选框的各个选项的状态 True or False
        i = int(self.sender().objectName().replace("checkBox",""))
        self.cbli[i-1] = e

    def normalOutputWritten(self, text):    # 输出调试信息到主窗口界面
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        try:
            cursor = self.printtext.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(text)
            self.printtext.setTextCursor(cursor)
            self.printtext.ensureCursorVisible()
        except Exception as e:
            print(e)

    def spider_handle(self,e):          # 爬虫开关调用
        if e:                # 根据开关状态判断 是创建线程 还是  关闭 线程
            self.selectli.clear()
            for i,bool in enumerate(self.cbli):
                if bool:
                    self.selectli.append(i)
            self.signal1.set()
            self.sender().setText("结束")
            try:
                self.t1.start()
            except:
                for i in self.selectli:             # 遍历选中的爬虫，创建对应线程
                    self.t1 = tr.Thread(target=funcdict[i], args=(self.signal1,),daemon=True)
                    self.t1.setDaemon(True)
                    self.t1.start()

        else:
            self.signal1.clear()
            self.sender().setText("开始")

            # 结束时触发函数把已下载 的excel 显示到listview
            self.display_li()
            self.flushnum()
            print(">>关闭 爬虫<<")

    def upload1(self):          # 上传
        try:
            self.sender().setDisabled(True)
            btob = self.sender()
            #self.uploadbt_1
            lwob = self.lwli[int(btob.objectName().replace("uploadbt_","")) - 1]   # 根据下标获取对应的listWidget对象
            self.t2 = tr.Thread(target=self.worker2,args=(btob,lwob),daemon=True)
            print(">>开始上传<<")
            self.t2.start()
        except Exception as e:
            self.sender().setDisabled(False)
            print(e)

    def worker1(self,li):       # 爬虫开关的线程
        while self.signal1:
            time.sleep(1.5)
            print("正在下载数据。。。")

    def worker2(self, btob, lwob):        # 上传的线程 item.objectName  uploadbt_1 ...
        time.sleep(1)

        _,i = btob.objectName().split("_")
        self.tabWidget.setTabIcon(int(i)-1,self.icon2)
        # QListWidget.items()
        for i in range(lwob.count()): # 得到listwidget 中的各个文件的路径列表
            filepath = lwob.item(i).text()
            path,filenameex = os.path.split(filepath)
            filename = filenameex.split(".xls")[0]
            examid = self.checksub(filename)
            self.sendfile(filenameex,examid,filepath)
        print(">>上传完毕<<")
        btob.setDisabled(False)

    def closeEvent(self,event):         # 重写关闭窗口事件没，　正在下载的时候有提示
        try:
            if self.t1.is_alive():
                re = QMessageBox.question(self,'正在下载数据',"要退出程序？",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
                if re == QMessageBox.Yes:
                    self.signal1.clear()
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()
        except:
            event.accept()

    def display_li(self):                   # 根据勾选过的爬虫 来展示对应的下载文件列表
        for i in self.selectli:
            try:
                li = [item for item in os.listdir(cwd + '/' + str(funcdict[i].__name__) + '/') if end_with(item, '.xlsx')]
                self.lwli[i].clear()
                self.lwli[i].addItems(li)
            except Exception as e:
                print(e)

    def checksub(self, filename):                # 获取试卷年月，检查是否存在试卷，不存在则创建，并获得试卷id
        li = re.findall("(\d{2,4})年(\d{1,2})月", filename)
        code = ''
        year = ''
        month = ''
        if len(li):
            year,month = li[0]
            if len(year) == 2:
                year = "20" + year
            subli = re.findall("\《.{1,30}\》", filename)
            if len(subli):                      # 根据中括号提取科目名称
                subname = subli[0]
                code = self.checkcode(subname)
            else:                               # 为空则需要判断 中文是否带有科目，无年份
                print("模拟")
        else:
            # code = self.checkcode(filename)
            tr.Thread(target=self.checkcode,args=(filename),daemon=True)
            year = "1970"
            month = '1'
        print('>',code,'>', year,'>', month, '哈哈')
        url = "http://www.biguotk.com/admin/exam_real_paper"
        para1 = {"code":code}                    # 代码参数 ,设置 一个代码变量 <<<
        hd = headers2.copy()
        hd["X-CSRF-TOKEN"] = csrfli[0]
        res = requests.get(url,params=para1,headers=hd,verify=False)
        html = lxml.etree.HTML(res.text)
        paperli = [x.strip() for x in html.xpath("//table/tbody/tr/td[1]/text()")]
        print(res.status_code,"获取到的试卷列表：",paperli)
        str1 = year + "年" + str(int(month)) + "月"      # 需要前缀不带0的月份

        urlli = html.xpath('//table/tbody/tr[1]/td[2]/a/@href')

        if str1 in paperli:
            index = paperli.index(str1)
            url,examid = urlli[index].split('?id=')
            para = {'id':examid}
            res = requests.get(url,params=para,headers=hd,verify=False)
            len1 = len(lxml.etree.HTML(res.text).xpath('/html/body/div[2]/div[2]/div/div[4]/div'))
            print("#试卷内容为：>>",len1)
            if not len1:
                print("#试卷无内容，可上传#")
            else:
                print("#试卷已有题目，未上传#")
        else:
            form = {"year": year, "month": month, "code": code}
            res = requests.post("http://www.biguotk.com/admin/exam_real_paper",data=form,headers=hd,verify=False)
            print(">>>>",res.text)

        return 1476

    def sendfile(self,filenameex,examid,filepath):    # 试卷上传功能
        m = MultipartEncoder(fields=[("_token",csrfli[0]),
                                    ('exampaper_id',str(examid)),
                                     ("excel",
                                      ("1.xlsx",
                                       open(filepath, 'rb'),
                                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
                                     ], boundary=boundary)
        hd = headers2.copy()
        hd["Content-Type"] = "multipart/form-data;charset=UTF-8;" + "boundary={}".format(boundary)
        try:
            res = requests.post("http://www.biguotk.com/admin/exam_real", data=m, headers=hd,verify=False)
            print("返回内容：", "返回状态:", res.status_code)
            return res.content,res.status_code
        except Exception as e:
            print("网络异常,重新上传。。。")
            self.sendfile(filenameex,examid,filepath)

    def checkcode(self,subname):
        poli = []
        poli1 = []
        out1 = [i for i in jieba.cut(subname) if len(i) >1]
        print(out1)
        for b in csvli1:           # 遍历csv科目列表，从非name行开始
            if b[0] != "name":     # 把分词后出现的词语进行对比，有可能的code 和科目加入到列表中
                count = 0
                for i in out1:
                    if i in eval(b[0]):
                        count += 1
                if count >= (2 * len(out1)) / 3:

                    print(csvli1.index(b), b[1], 'wa')
                    # if b[1] not in poli:
                    if b[1] not in poli:
                        poli.append(b[1])
                        poli1.append(eval(b[0])[-1])

        if len(poli) > 1:           # 大于1 说明识别出多个code，需要进行手动选择
            print("识别出多个")
            for i, j in zip(poli, poli1):
                print(i, j)

        elif len(poli) == 1:        # 只有1个code 则直接返回该code
            code = poli[0]
            print(poli[0], poli1[0])
            return code

        else:                       # 没有识别出科目，手动填写
            print('无法识别科目，请填写')
            code = ''
            try:
                self.subw1 = subw
                self.subw1.exec()

            except Exception as e:
                print('>',e)

    # def getcode(self,e):
    #     print(e,"<>")
    #     self.subw1.code = self.subw1.subcode.text()
    #     if self.subw1.code:
    #         self.subw1.subcode.clear()
    #         self.subw1.subname.clear()


class SubW(QDialog,UiSubject):           #科目录入窗口
    def __init__(self):
        super(SubW,self).__init__()
        self.setupUi(self)
        self.key = '0'
        self.code = ''

    def closeSubW(self):
        self.close()

    # def __str__(self):
    #     return self.key
    # __repr__ = __str__


class SetW(QWidget,UiSetall):   #爬虫设置窗口
    def __init__(self):
        super(SetW, self).__init__()
        self.setupUi(self)

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        self.close()


class EmittingStream(QtCore.QObject):   # 调试信息信号发送
    textWritten = QtCore.pyqtSignal(str)
    num = 0
    def write(self,text):
        if text == '该链接已下载！！！':
            if self.num == 0:
                self.textWritten.emit(str(text))
                self.num += 1
            else:
                self.num += 1
                self.textWritten.emit(str(text)+str(self.num))
        else:
            self.textWritten.emit(str(text))

def end_with(item,*str):           # 判断文件是否 以某个字符串结尾
    array = map(item.endswith,str)
    if True in array:
        return True
    else:
        return False

def work():                # 主进程
    loginW = LoginW()
    mainW = TkW()
    loginW.show()
    #mainW.show()
    return mainW,loginW

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainW,loginW = work()
        subw = SubW()
        sys.exit(app.exec())
    except Exception as e:
        print('main',e)
