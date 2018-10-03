# coding = utf-8

from appium import webdriver as wb
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from write_to_exel import write_xlsx as wtex
import time,os,sys
sys.setrecursionlimit(1000000)
loc = EC.presence_of_element_located
locs = EC.presence_of_all_elements_located
desired_caps = {
                'platformName': 'Android',
                'deviceName': '127.0.0.1:52001',
                'platformVersion': '4.4',
                'appPackage': 'com.sunland.exam', #红色部分如何获取下面讲解
                #'appActivity': 'launching.LaunchingActivity',
                'appActivity':'.ui.LauncherSelectActivity',
                #"appActivity":".login.SunlandSignInActivity",
                'unicodeKeyboard': True, #此两行是为了解决字符输入不正确的问题
                'resetKeyboard': True    #运行完成后重置软键盘的状态　　
            }
# .ui.home.HomePageActivity  .login.SunlandSignInActivity
dr = wb.Remote('http://localhost:4723/wd/hub',desired_capabilities=desired_caps)
wait = WebDriverWait(dr,20)
doli = ["公共课","专业课","马克思主义基本原理概论","英语（二）","综合英语（二）","英语语法","高级英语","英语翻译",
        "英语写作","英美文学选读","英语词汇学","现代语言学","语言学概论","英语"]
doli2 = ["中国近现代史纲要","企业管理概论","公文写作与处理","政治学概论","法学概论","现代管理学","社会学概论","行政管理学","基础会计学"]
with open("shangtiku2.urz","r+",encoding="utf-8") as f:
    con = f.read()
    c = con
doli0 = c.split(",")
print(doli0)
doli = doli + doli2+doli0
pwd = os.getcwd()


def preload(): # 预加载模块
    wait.until(loc((By.XPATH,"//android.widget.LinearLayout/android.widget.ImageView[1]"))).click()
    wait.until(loc((By.XPATH,"//android.widget.ScrollView/android.widget.RelativeLayout/android.widget.TextView[1]"))).click()
    wait.until(loc((By.XPATH,"//android.support.v4.view.ViewPager/android.widget.ImageView"))).click()

def login():
    wait.until(loc((By.ID,"com.sunland.exam:id/btn_login"))).click()
    wait.until(loc((By.ID,"com.sunland.exam:id/sunland_activity_sign_in_et_account"))).send_keys("15527301530")
    wait.until(loc((By.ID, "com.sunland.exam:id/sunland_activity_sign_in_et_password"))).send_keys("11980389")
    wait.until(loc((By.ID,"com.sunland.exam:id/sunland_activity_sign_in_btn_login"))).click()


def predown1():  # 课程选择

    subnamee = wait.until(loc((By.ID, "com.sunland.exam:id/tv_name_subject")))
    subnamee.click()
    if not os.path.exists(pwd + "/shangtiku2"):
        os.makedirs(pwd + "/shangtiku2")
    list = wait.until(locs((By.XPATH, "//android.support.v7.app.ActionBar.Tab/android.widget.TextView")))  # [专科，本科]
    for i in list:
        i.click()
        majorli = wait.until(locs((By.XPATH, "//android.support.v7.widget.RecyclerView[1]/android.widget.TextView")))
        for j in majorli:
            j.click()
            subli = wait.until(locs((By.XPATH,
                                     "//android.support.v7.widget.RecyclerView[2]/android.widget.RelativeLayout/android.widget.TextView")))


def predown():# 课程选择
    print(">选择 专业 和 课程<")
    subnamee = wait.until(loc((By.ID,"com.sunland.exam:id/tv_name_subject")))
    subnamee.click()
    if not os.path.exists(pwd+"/shangtiku2"):
        os.makedirs(pwd+"/shangtiku2")
    list = wait.until(locs((By.XPATH,"//android.support.v7.app.ActionBar.Tab/android.widget.TextView"))) #[专科，本科]
    for n,i in enumerate(list):
        if n == 1:

            i.click()
            majorli = wait.until(locs((By.XPATH,"//android.support.v7.widget.RecyclerView[1]/android.widget.TextView")))
            for j in majorli:
                time.sleep(1)
                print(j.text)
                j.click()
                time.sleep(2)
                print(">")
                subli = wait.until(locs((By.XPATH,"//android.support.v7.widget.RecyclerView[2]/android.widget.RelativeLayout/android.widget.TextView")))
                flag = 0
                for i in range(50):
                    l,k = subli[0+flag],subli[1+flag]
                    print(l.text,k.text)
                    if "英语" in l.text:
                        doli.append(l.text)
                    if "英语" in k.text:
                        doli.append(k.text)
                    if l.text not in doli:
                        doli.append(l.text)
                        print("1:",l.text)
                        l.click()
                        time.sleep(1)
                        subname = subnamee.text
                        subname = subname.replace("/", "")
                        fpath = pwd+"/shangtiku2/"+subname
                        if not os.path.exists(fpath):
                            os.makedirs(fpath)
                        subd(fpath,subname)  # 课程下载 调用
                        with open("shangtiku2.urz","a+",encoding="utf-8") as f:
                            f.write(subname+",")
                        subnamee.click()
                    elif k.text not in doli:
                        doli.append(k.text)
                        print("2:",k.text)
                        k.click()
                        time.sleep(1)
                        subname = subnamee.text
                        subname = subname.replace("/","")
                        fpath = pwd + "/shangtiku2/" + subname
                        if not os.path.exists(fpath):
                            os.makedirs(fpath)
                        subd(fpath, subname)  # 课程下载 调用
                        with open("shangtiku2.urz","a+",encoding="utf-8") as f:
                            f.write(subname+",")
                        subnamee.click()
                    else:
                        a = subli[-1].text
                        dr.swipe(360,781,360,703,900)
                        print(subli[-1])
                        time.sleep(2)
                        li = wait.until(locs((By.XPATH,"//android.support.v7.widget.RecyclerView[2]/android.widget.RelativeLayout/android.widget.TextView")))
                        b = li[-1].text
                        if a ==b :
                            flag += 1
                            if flag + 2 == len(subli):
                                break


def subd(fpath,subname): # 课程试题下载
    print("课程下载>>>")
    wait.until(loc((By.ID,"com.sunland.exam:id/tv_chapter_exercise"))).click()
    # ((By.ID,"com.sunland.exam:id/tv_real_exercise"))
    try:
        chaterslie = wait.until(loc((By.ID,"com.sunland.exam:id/rv_left"))).find_elements_by_id("com.sunland.exam:id/ll_item")
    except:
        chaterslie = []
    chaterslie = [i for i in chaterslie if isexist("id","com.sunland.exam:id/tv_name",d=i)] # com.sunland.exam:id/tv_chapter_order
    for n,c in enumerate(chaterslie): # 遍历章节题
        dochapter(c,fpath)
        if n >=8 and n == len(chaterslie)-1:
            while True:
                a = c.find_element_by_id("com.sunland.exam:id/tv_chapter_order").text

                dr.swipe(54, 692, 54, 561, 1000)
                li = wait.until(loc((By.ID,"com.sunland.exam:id/rv_left"))).find_elements_by_id("com.sunland.exam:id/ll_item")
                li = [i for i in li if isexist("id","com.sunland.exam:id/tv_name",d=i)]
                b = li[-1].find_element_by_id("com.sunland.exam:id/tv_chapter_order").text

                c = li[-1]
                if a == b:  # 滑动后 相等，说明到最后一章节了
                    break
                dochapter(c,fpath)

    wait.until(loc((By.ID, "com.sunland.exam:id/actionbarButtonBack"))).click()
    time.sleep(1)
    print("点击返回到某科目页面1")
    wait.until(loc((By.ID,"com.sunland.exam:id/tv_real_exercise"))).click()
    try:
        reallie = wait.until(locs((By.ID,"com.sunland.exam:id/ll_item")))
        reallie = [i for i in reallie if isexist("id", "com.sunland.exam:id/tv_count", d=i)]
    except:
        reallie = []
    for n,d in enumerate(reallie):
        doreal(d,fpath)
        if n == len(reallie)-1:
            while True:
                a = d.find_element_by_id("com.sunland.exam:id/tv_paper_name").text
                dr.swipe(54, 696, 54, 591, 1000)
                time.sleep(1)
                li = dr.find_elements_by_id("com.sunland.exam:id/ll_item")
                li = [i for i in li if isexist("id", "com.sunland.exam:id/tv_paper_name", d=i)]
                b = li[-1].find_element_by_id("com.sunland.exam:id/tv_paper_name").text
                print("|",a,"|",b,"|")
                d = li[-1]
                if a == b:
                    break
                doreal(d,fpath)
    print("点击返回1")
    wait.until(loc((By.ID, "com.sunland.exam:id/actionbarButtonBack"))).click()
    print("返回到:",dr.current_activity)
    time.sleep(3)

    # 回到科目选择页

def dochapter(c,fpath): # 章节题处理
    ae = c.find_element_by_id("com.sunland.exam:id/tv_chapter_order")
    ce = c.find_element_by_id("com.sunland.exam:id/tv_name")
    c.click()
    onesli = wait.until(loc((By.ID, "com.sunland.exam:id/rv_right"))).find_elements_by_id("com.sunland.exam:id/ll_item")
    fname = ae.text + " " + ce.text
    if os.path.exists(fpath + "/" + fname + ".xlsx"):
        print("已下载...")

    else:
        p = Paper(onesli, 1)
        farray = p.farray
        print(fpath, fname, p.farray)
        wtex(fpath, fname, farray)
        time.sleep(1)

def doreal(d,fpath):  # 真题处理
    realnamee = d.find_element_by_id("com.sunland.exam:id/tv_paper_name")
    realname = realnamee.text
    if os.path.exists(fpath + "/" + realname + ".xlsx"):
        print("已下载...")
    else:
        d.click()
        p = Paper(clsi=2)
        farray = p.farray
        wtex(fpath, realname, farray)

def isexist(meth,astr,nowait=1,d=dr):
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
                ele = wait.until(loc((By.ID,astr)))
            return ele
        except:
            print("注意没获取到元素，id",astr)
            return None
    elif meth == "xpath":
        try:
            if nowait:
                ele = d.find_element_by_xpath(astr)
            else:
                ele = wait.until(loc((By.XPATH,astr)))
            return ele
        except:
            print("注意没获取到元素，xpath",astr)
            return None


class Paper():

    def __init__(self,onesli=None,clsi=0):
        self.farray =  [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]
        self.clsi = clsi
        if clsi == 1:
            # for one in onesli:
            #     print(one.find_element_by_id("com.sunland.exam:id/tv_node_name").text)
            li = [i for i in onesli if isexist("id", "com.sunland.exam:id/tv_count", d=i)]
            for n,one in enumerate(li):
                self.doone(one)
                if n == len(onesli)-1:
                    while True:
                        a = one.find_element_by_id("com.sunland.exam:id/tv_node_name").text
                        dr.swipe(360, 697, 360, 619, 1000)
                        oli = wait.until(loc((By.ID, "com.sunland.exam:id/rv_right"))).find_elements_by_id(
                            "com.sunland.exam:id/ll_item")
                        oli = [i for i in oli if isexist("id", "com.sunland.exam:id/tv_count", d=i)]
                        b = oli[-1].find_element_by_id("com.sunland.exam:id/tv_node_name").text
                        one = oli[-1]
                        if a == b:
                            break
                        self.doone(one)

        elif clsi == 2:
            # 真题
            self.getitems()

        else:
            print("没有试题类型")
        print("爬取完一套题")
    def doone(self,one):
        print("爬取小节↓↓↓")
        a = one.find_element_by_id("com.sunland.exam:id/tv_node_name").text
        cnt = one.find_element_by_id("com.sunland.exam:id/tv_count").text
        print(a,len(a))

        if len(a) >=35:
            return
        if cnt != "0":
            one.click()
            self.getitems(one)
        else:
            print("该小节无题")

    def getitems(self,one=''):
        iscomit = isexist("id","com.sunland.exam:id/question_analysis_into")
        isquiz = isexist("id","com.sunland.exam:id/dialog_new_quizzes_one")
        if isquiz:
            print("第一次点击")
            isquiz.click()
            wait.until(loc((By.XPATH,"//android.widget.FrameLayout"))).click()
        if iscomit:
            iscomit.click()
        else:
            print("点击答题卡")
            try:
                wait.until(loc((By.ID, "com.sunland.exam:id/iv_answer_card"))).click()
                wait.until(loc((By.ID, "com.sunland.exam:id/item_new_exam_submit_btn"))).click()
                isquiz2 = isexist("id","com.sunland.exam:id/item_quizzes_submit_btn")
                if isquiz2:
                    isquiz2.click()
            except TimeoutException:
                print(">time out<")
                time.sleep(30)
                self.getitems(one)

            wait.until(loc((By.ID, "com.sunland.exam:id/question_analysis_into"))).click()
        try:
            self.parse()
        except TimeoutException:
            dr.find_element_by_id("com.sunland.exam:id/iv_back").click()
            print(one)
            if one:one.click()
            self.getitems(one)


    def parse(self):  # 内容解析
        # 章节题
        array = self.empty_li()
        type = wait.until(loc((By.ID, "com.sunland.exam:id/qestion_title_type"))).text
        sindex = dr.find_element_by_id("com.sunland.exam:id/qestion_title_sequence").text
        index = int(sindex)
        stotal = dr.find_element_by_id("com.sunland.exam:id/qestion_title_total").text.strip("/")
        total = int(stotal)
        print("解析题目...")
        if "单选" in type:
            cls = 1
        elif "多选" in type:
            cls = 2
        elif "填空" in type:
            cls =4
            flag = 1
        else:
            cls = 4
        # titlee = dr.find_element_by_id("com.sunland.exam:id/choice_question_body").find_element_by_xpath("//android.widget.TextView")
        titlee = isexist("xpath","//android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView")
        if titlee:
            title = titlee.text
        else:
            titlee = isexist("id","com.sunland.exam:id/questionView").find_element_by_xpath("//android.widget.TextView")
            title = titlee.text
        ist2 = isexist("id","com.sunland.exam:id/fragment_exam_synthesise_question_topic_of_dry")
        if ist2:
            t2 = ist2.text
            title = t2 + "\n" + title
        if cls ==1 or cls == 2:
            optionlie = dr.find_elements_by_xpath("//android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout")
            for i,ele in enumerate(optionlie):
                op = ele.find_element_by_id("com.sunland.exam:id/item_option_content").text
                array[i+3] = op

        isanse = isexist("id","com.sunland.exam:id/tv_answer")
        if not isanse:
            anse = self.swipefindit(1)
            if anse:
                ans = anse.text.strip()
                if not ans:
                    ans = anse.get_attribute("name")
            else:
                ans = ""
        else:
            try:
                ans = isanse.find_element_by_xpath("//android.widget.TextView").text
            except:
                ans = isanse.find_element_by_xpath("//android.view.View").get_attribute("name")

        isanise = isexist("id","com.sunland.exam:id/webview_analyse")
        if not isanise:
            anise = self.swipefindit(2)
            if anise:
                anis = anise.text
            else:
                anis = ""
        else:
            try:
                anis = isanise.find_element_by_xpath("//android.widget.TextView").text
            except:
                anis = isanise.find_element_by_xpath("//android.view.View").text

        array[1] = cls
        array[2] = title
        array[9] = ans.replace("参考答案：","").replace("我的答案：","").strip()
        array[10] = anis
        array[0] = len(self.farray)
        self.farray.append(array)
        if index < total:
            # 下一题
            dr.swipe(684, 917, 174, 917, 1000)
            time.sleep(1)
            return self.parse()
        elif index == total:
            print("爬完该节")
            dr.find_element_by_id("com.sunland.exam:id/iv_back").click()
            if self.clsi == 2:
                dr.find_element_by_id("com.sunland.exam:id/actionbarButtonBack").click()

    def swipefindit(self,clsi,timeout=1):
        """
        定位寻找 答案或者解析
        :param clsi:  1 为答案 2 为解析
        :return: 返回 元素 或者超时后返回None
        """
        timeout += 1
        dr.swipe(324, 917, 324, 717, 1000)
        if clsi == 1:# 找答案位置
            isanse = isexist("id","com.sunland.exam:id/tv_answer")
            if not isanse:
                if timeout <= 20:
                    return self.swipefindit(1,timeout)
                else:
                    return None
            else:
                dr.swipe(324, 917, 324, 817, 1000)
                time.sleep(0.2)
                try:
                    anse = isanse.find_element_by_xpath("//android.widget.TextView")
                except:
                    anse = isanse.find_element_by_xpath("//android.view.View")
                return anse
        elif clsi == 2:# 找解析位置
            isanise = isexist("id","com.sunland.exam:id/webview_analyse")
            if not isanise:
                if timeout <= 20:
                    return self.swipefindit(2,timeout)
                else:
                    return None
            else:
                dr.swipe(324, 917, 324, 817, 1000)
                time.sleep(0.2)
                ansise = isanise.find_element_by_xpath("//android.widget.TextView")
                return ansise

    @staticmethod
    def empty_li():
        array = ['' for i in range(11)]
        return array


# 程序入口
def shangtiku2():
    try:
        preload()
        a = wait.until(loc((By.ID,"com.sunland.exam:id/tv_chapter_exercise")))
        a.click()
        wait.until(loc((By.ID,"android:id/button1"))).click()
        login()
        predown()
    except TimeoutException:
        time.sleep(100)
        dr.reset()
        time.sleep(10)
        print("重新启动")
        shangtiku2()

if __name__ == '__main__':
    shangtiku2()
    print(">wantiku END<")
