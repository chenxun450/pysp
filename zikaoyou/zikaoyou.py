# coding = utf-8

from appium import webdriver as wb
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from utils.write_to_exel import write_xlsx as wtex
import time,os,sys,re
sys.setrecursionlimit(1000000)
loc = EC.presence_of_element_located
locs = EC.presence_of_all_elements_located
desired_caps = {
                'platformName': 'Android',
                'deviceName': '127.0.0.1:62025',
                'platformVersion': '5.1.1',
                'appPackage': 'com.self.study.sns',
                #'appActivity': 'launching.LaunchingActivity',
                'appActivity':'.activity.login.LoginActivity',
                #"appActivity":".login.SunlandSignInActivity",
                'unicodeKeyboard': True, #此两行是为了解决字符输入不正确的问题
                'resetKeyboard': True    #运行完成后重置软键盘的状态　　
            }
cwd = os.getcwd()
dr = wb.Remote('http://localhost:4723/wd/hub',desired_capabilities=desired_caps)
wait = WebDriverWait(dr,20)
if not os.path.exists(cwd + "/zikaoyou"):
    os.mkdir(cwd +"/zikaoyou")
fpath = cwd + "/zikaoyou"
with open("zikaoyou.urz","r+",encoding="utf-8") as f:
    con = f.read()
    content = con
subdoli = content.split(",")
print(subdoli)

def login():
    print("登陆中。。。")
    wait.until(loc((By.ID,"com.self.study.sns:id/name"))).send_keys("ba460@sina.com")
    dr.find_element_by_id("com.self.study.sns:id/pwd").send_keys("11980389")
    dr.find_element_by_id("com.self.study.sns:id/login").click()

def choose():

    dr.find_element_by_id("com.self.study.sns:id/activity_study_part_img").click()   # 章节练习
    dr.find_element_by_id("com.self.study.sns:id/activity_study_main_studyQuestion_id").click() # 历年真题
    chapterli = wait.until(locs((By.ID,"com.self.study.sns:id/tree_view_item_title"))) # 72
    # chapter.click()

def mainwork():
    print("正在获取学科信息")
    # main ui 点击我 com.self.study.sns:id/radio_button3
    time.sleep(3)
    wait.until(loc((By.ID, "com.self.study.sns:id/radio_button3"))).click()
    # 个人中心 点击进入 学科 选择
    wait.until(loc((By.ID, "com.self.study.sns:id/editInfoview"))).click()
    time.sleep(4)
    # detail  点击下拉学科菜单
    wait.until(loc((By.ID, "com.self.study.sns:id/examprofession"))).click()
    # 专业选择页 点击专科或本科
    time.sleep(3)
    li = wait.until(locs((By.ID, "android:id/title")))

    for p,i in enumerate(li):
        mjdone = []   # 爬过的专业
        print("专科><本科",p)
        i.click()
        time.sleep(3)
        # 专业选择页  专业列表选择
        majorli = wait.until(locs((By.ID, "com.self.study.sns:id/name")))
        for o,j in enumerate(majorli):
            if p != 0:
                i.click()
            time.sleep(2)
            mj = j.text
            time.sleep(1)
            j.click()
            time.sleep(3)
            if o ==0 and p == 0:
                #detail 保存 com.self.study.sns:id/saveMineInfoBtn
                wait.until(loc((By.ID, "com.self.study.sns:id/saveMineInfoBtn"))).click()
                print("点击保存")
                # 个人中心  切换到学习
                time.sleep(2)
                wait.until(loc((By.ID, "com.self.study.sns:id/radio_button0"))).click()
                dr.find_element_by_id("com.self.study.sns:id/activity_study_main_textView1").click()
            time.sleep(2)
            todosub()
            mjdone.append(mj)
            changemaj2()
            mjtext = mj
            print("专业>>",o,j)
            if o == 14:
                while True:
                    #dr.swipe(360,910,360,860,1000)
                    b = isbottom("id", "com.self.study.sns:id/name", mjtext)
                    if not b:
                        # 返回到 主页
                        #dr.find_element_by_id("com.self.study.sns:id/activity_question_past_courseBack_id").click()
                        break
                    else:
                        subname = b.text
                        mjtext = subname
                        if mjtext not in mjdone:
                            b.click()
                            time.sleep(2)
                            # wait.until(loc((By.ID, "com.self.study.sns:id/saveMineInfoBtn"))).click()
                            # # 个人中心  切换到学习
                            # time.sleep(2)
                            # wait.until(loc((By.ID, "com.self.study.sns:id/radio_button0"))).click()
                            todosub()
                            mjdone.append(mjtext)
                            changemaj2()
                        else:
                            print("下滑寻找尾页")
                            dr.swipe(360, 900, 360, 870, 1000)

    print("> End<")


def changemaj():
    print("切换专业>>>")
    # main ui 点击我 com.self.study.sns:id/radio_button3
    wait.until(loc((By.ID, "com.self.study.sns:id/radio_button3"))).click()
    time.sleep(2)
    # 个人中心 点击进入 学科 选择
    wait.until(loc((By.ID, "com.self.study.sns:id/editInfoview"))).click()
    # detail  点击下拉学科菜单
    time.sleep(3)
    wait.until(loc((By.ID, "com.self.study.sns:id/examprofession"))).click()
    print("进入专业菜单")
    time.sleep(2)

def changemaj2():
    print("切换专业>>>")
    time.sleep(3)
    wait.until(loc((By.ID, "com.self.study.sns:id/activity_study_main_textView1"))).click()

    time.sleep(3)
    wait.until(loc((By.ID, "com.self.study.sns:id/change_id"))).click()


def todosub():
    time.sleep(10)

    # 68 px
    subeli = wait.until(locs((By.ID,"com.self.study.sns:id/name")))
    subdone = []  # 爬过的科目
    for n,i in enumerate(subeli):
        print(n,i,len(subeli))
        subname = i.text
        if "英语" not in subname:
            if subname not in subdoli:
                i.click()
                time.sleep(2)
                dosub(subname)
                subdone.append(subname)
            if n == 16:

                while True:
                    print("下滑找kemu")
                    b = isbottom("id","com.self.study.sns:id/name",subname)
                    if not b:
                        # 返回到 主页
                        # dr.find_element_by_id("com.self.study.sns:id/activity_question_past_courseBack_id").click()
                        # dr.find_element_by_id("com.self.study.sns:id/activity_study_main_textView1").click()
                        i.click()
                        break
                    else:
                        # todo 11dai
                        subname = b.text
                        if subname not in subdoli:
                            b.click()
                            time.sleep(2)
                            dosub(subname)
                            subdone.append(subname)
    iscoubc = isexist("id","com.self.study.sns:id/activity_course_select_courseBack_id")
    if iscoubc:
        iscoubc.click()


def dosub(subname):
    print("处理科目...")
    wait.until(loc((By.ID, "com.self.study.sns:id/activity_study_main_studyQuestion_id"))).click()
    ispapers = isexist("id", "com.self.study.sns:id/item2_head")
    if ispapers:
        papereli = dr.find_elements_by_id("com.self.study.sns:id/item2_head")
        time.sleep(2)
        for o, j in enumerate(papereli):
            print(o,j,len(papereli))
            papername = j.text
            print(papername)
            if "暂无" in papername:
                print("无真题")
                break
            if o != 12:
                if not os.path.exists(fpath + "/"+subname +"/"+ papername+".xlsx"):
                    j.click()
                    a = isexist("id", "android:id/button2")
                    if a:
                        a.click()
                    dopaper(subname, papername)
            elif o == 12:
                while True:
                    print("下滑找试卷")
                    b = isbottom("id", "com.self.study.sns:id/item2_head", papername)
                    if not b:
                        # 返回到 主页
                        break
                    else:
                        papername = b.text
                        if not os.path.exists(fpath + "/" + subname + "/" + papername+".xlsx"):
                            b.click()
                            a = isexist("id","android:id/button2")
                            if a:
                                a.click()
                            dopaper(subname, papername)

    else:
        print("没找到真题")
        # 点击返回 。
    # com.self.study.sns:id/activity_course_select_courseBack_id
    print("返回到主页")
    dr.find_element_by_id("com.self.study.sns:id/activity_question_past_courseBack_id").click()
    with open("zikaoyou.urz","a+",encoding="utf-8") as f:
        f.write(subname+",")
    print("点击选择科目")
    dr.find_element_by_id("com.self.study.sns:id/activity_study_main_textView1").click()

    #dr.find_element_by_id("com.self.study.sns:id/activity_course_select_courseBack_id").click()

def dopaper(subname,papername):
    print("处理试卷中。。。")
    fpath1 = fpath + "/" + subname
    p = Paper()
    if not os.path.exists(fpath1):
        os.mkdir(fpath1)
    wtex(fpath1, papername, p.farray)

def isbottom(by,astr,text,flag=0):
    '''
    判断是否到菜单底部
    :return: 返回 最后一个元素 or None
    '''
    a = text
    print("前：",a)
    dr.swipe(360,665,360,620,1200)
    flag += 1
    if by == "id":
        li = dr.find_elements_by_id(astr)
        try:
            b = li[-1].text
        except:
            b = a
        print("后：",b)
        if a == b:
            print(a==b,"继续")
            if flag <=4:
                return isbottom(by,astr,a,flag)
            else:
                print("列表到底部了")
                return None
        elif a != b:
            print("返回")
            ele = li[-1]
            return ele

def isexist(meth, astr, nowait=1, d=dr):
    """
    判断元素是否存在
    :param meth: "id" or "xpath"
    :param astr: ""表达式
    :param nowait: 是否开启等待
    :param d:  父元素，默认是 driver
    :return: 存在则返回元素本身，否则返回None
    """
    if meth == "id":
        try:
            if nowait:
                ele = d.find_element_by_id(astr)
            else:
                ele = wait.until(loc((By.ID, astr)))
            return ele
        except:
            print("注意没获取到元素，id", astr)
            return None
    elif meth == "xpath":
        try:
            if nowait:
                ele = d.find_element_by_xpath(astr)
            else:
                ele = wait.until(loc((By.XPATH, astr)))
            return ele
        except:
            print("注意没获取到元素，xpath", astr)
            return None

class Paper():

    def __init__(self):
        self.farray = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]
        self.predone()
        self.parse1()

    def predone(self):
        # 交卷
        print("提交答题...")
        a = wait.until(loc((By.ID,"com.self.study.sns:id/activity_question_past_study_submit_id")))
        time.sleep(2)
        if a.text != "已交卷":
            a.click()
            time.sleep(5)
            dr.find_element_by_id("android:id/button1").click()
            time.sleep(6)
            dr.find_element_by_id("com.self.study.sns:id/activity_score_past_button3").click()

    def parse1(self):
        print("解析题目中...")
        for i in range(10):
            dr.swipe(324, 717, 324, 917, 1000)
            time.sleep(1)
            isclsstr =isexist("id","com.self.study.sns:id/danxuan_questionType_id")
            if isclsstr:
                break
        if isclsstr:
            clsstr = isclsstr.text
        else:
            clsstr = ""
        t2 = ""
        if "单项" in clsstr:
            cls = 1
        elif "多项" in clsstr:
            cls = 2
        else:
            cls = 4
            isslide =  isexist("id","com.self.study.sns:id/sliding_text_id")
            if isslide:
                t2 = isslide.text

        oneli = self.empty_li()
        oneli[0] = len(self.farray)
        oneli[1] = cls
        title = dr.find_element_by_id("com.self.study.sns:id/danxuan_title_id").text
        title = re.sub("^\d+\.","",title)
        oneli[2] = t2 + title.strip()
        seq = dr.find_element_by_id("com.self.study.sns:id/danxuan_num_id").text


        if cls == 1 or cls == 2:
            isoptes = isexist("id","com.self.study.sns:id/danxuan_option_id")
            if not isoptes:
                optes = self.swipefindit(3)
            else:
                optes = isoptes

            if optes:
                opeli = optes.find_elements_by_xpath("//android.widget.TextView")
            else:
                oneli[1] = 4
                opeli = []
            for n, i in enumerate(opeli):
                if n <= 5:
                    oneli[3 + n] = i.text

        isanse = isexist("id", "com.self.study.sns:id/danxuan_answer_id")
        if isanse:
            oneli[9] = isanse.text.strip()
        else:
            anse = self.swipefindit(1)
            if anse:
                oneli[9] = anse.text.strip()
            else:
                oneli[9] = ""
        isansise= isexist("id","com.self.study.sns:id/danxuan_analysis_id")
        if isansise:
            oneli[10] = isansise.text.replace("无", "").strip()
        else:
            ansise = self.swipefindit(2)
            if ansise:
                print(ansise)
                try:
                    oneli[10] = ansise.text.strip()
                except:
                    oneli[10] = ""
            else:
                oneli[10] = ""
        #oneli[10] = dr.find_element_by_id("com.self.study.sns:id/danxuan_analysis_id").text.replace("无", "")
        if oneli[9] == "暂无":
            oneli[9] = oneli[10]
        self.farray.append(oneli)

        a, b = re.findall("(\d+)题/(\d+)题", seq)[0]
        print("当前题号:",a,"总题数:",b)
        if a == b or len(self.farray)>int(b):
            print("爬完毕")
            wait.until(loc((By.ID, "com.self.study.sns:id/activity_question_error_study_studyCourseBack_id"))).click()
        else:
            print("滑到下一题")

            dr.swipe(700, 930, 650, 930, 1000)
            dr.swipe(700,930,50,930,1000)
            return self.parse1()

    def swipefindit(self,clsi,timeout=1):
        """
        定位寻找 答案或者解析
        :param clsi:  1 为答案 2 为解析 3 为选项
        :return: 返回 元素 或者超时后返回None
        """
        timeout += 1
        dr.swipe(324, 917, 324, 717, 1000)
        if clsi == 1:# 找答案位置
            isanse = isexist("id","com.self.study.sns:id/danxuan_answer_id")
            if not isanse:
                if timeout <= 15:
                    return self.swipefindit(1,timeout)
                else:
                    return None
            else:
                dr.swipe(324, 917, 324, 717, 1000)
                time.sleep(0.2)
                #
                return isanse
        elif clsi == 2:# 找解析位置
            isansise = isexist("id","com.self.study.sns:id/danxuan_analysis_id")
            if not isansise:
                if timeout <= 15:
                    return self.swipefindit(2,timeout)
                else:
                    return None
            else:
                dr.swipe(324, 917, 324, 717, 1000)
                time.sleep(0.2)
                #ansise = isanise.find_element_by_xpath("//android.widget.TextView")
                return isansise
        elif clsi == 3:
            isopte = isexist("id","com.self.study.sns:id/danxuan_option_id")
            if not isopte:
                if timeout <= 10 :
                    return self.swipefindit(3,timeout)
                else:
                    return None
            else:
                dr.swipe(324, 917, 324, 817, 1000)
                time.sleep(0.2)
                return isopte

    @staticmethod
    def empty_li():
        array = ['' for i in range(11)]
        return array

def zikaoyou():
    login()
    # 选择一个科目
    time.sleep(4)
    wait.until(loc((By.ID, "com.self.study.sns:id/name"))).click()
    mainwork()

if __name__ == '__main__':
    zikaoyou()
