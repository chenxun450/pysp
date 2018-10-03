# coding:utf-8

import requests,re,time,os
import xlrd
from PIL import Image
from lxml import etree
from threading import Thread
import pickle
info = []
try:
    with open("./hneao.pl","rb") as f :
        dic = pickle.load(f)
except Exception as e:
    print(e)
    dic = ''
if len(dic) >0:
    cookiejar = dic
else:
    cookiejar = {}
def exceldone():
    book = xlrd.open_workbook("../9.8湖南成考抢号汇总表.xlsx")
    sh = book.sheet_by_index(0)
    for k in range(0,131):
        if k>=1:
            a = sh.cell_value(k,1)
            b = sh.cell_value(k,2)
            c = sh.cell_value(k, 5)
            d = sh.cell_value(k, 9)
            print(a,b,c,d)
            if a and a != "不报考":
                if "医药" not in d and "农业" not in d:
                    info.append([a,b,c,1])
                elif "农业" in d:
                    info.append([a,b,c,2])
                else:
                    print("yiyao")

class Signupsys():
    def __init__(self,a,b,c,d,cook):
        super(Signupsys,self).__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
            "Referer": "https://cz.hneao.cn/ks/login.aspx",
        }
        self.cookie = cook
        if cook:
            self.headers["Cookie"] = self.cookie
        self.url = "https://cz.hneao.cn/ks/default.aspx"

        self.headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
            "Referer": "https://cz.hneao.cn/ks/login.aspx",
        }
        self.user = a
        self.pwd = b
        self.name = c
        self.flag = d

        self.flag2 = 0 # 0 是优先选择翰林
        pass

    def pre(self):
        res = requests.get(self.url,headers=self.headers,timeout=20)
        #print(res.text)
        c = res.text
        hte = etree.HTML(c)
        ele = hte.xpath('//*[@id="btnLogin"]')
        if ele:
            print(self.name,"需要重新登录")
            self.login()
            res = requests.get(self.url, headers=self.headers,timeout=20)
            #print(res.text)
            c = res.text
        try:
            li = re.findall("ks={([^;]*)}",c)
            li1 = [j.strip("\"") for i in li[0].split(",") for j in i.split(":")]
            li3 = [x for i,x in enumerate(li1) if i%2 == 0]
            li4 = [x for i,x in enumerate(li1) if i%2 == 1]
            d = dict(zip(li3,li4))
            print(d["YHM"],d["XM"])
        except Exception as e:
            print(e)

        if self.flag == 1:
            xq = "0103"
            if self.flag2==0:
                bmd = "010313"
            elif self.flag2 ==1:
                bmd = "010309"
            else:
                print(self.name," 没有预选上")
        elif self.flag == 2:
            xq = "0111"
            bmd = "011103"

        data = {
            "action": "yy_bmd",
            "sz": "01",
            "xq": xq,  # 0103 天心  0111 雨花
            "bmd":bmd, # 010313 翰林  010309 金科 011103 农业
            "timestamp": str(int(time.time() * 1000))
        }
        res2 = requests.post("https://cz.hneao.cn/ks/ajax_operation.aspx",data=data,headers=self.headers)
        try:
            res2d = dict(res2.json())
            print(res2d["MSG"])
        except Exception as e:
            print(e)
            print("提交失败")
            return self.pre()

        if res2d["MSG"] == "所选报名确认点已满额":
            print("已满额")
            self.flag2 += 1


    def mainwork(self):
        self.pre()

    def run(self):
        self.mainwork()

    def login(self):
        try:
            res = requests.get("https://cz.hneao.cn/ks/verificationCode.aspx",headers=self.headers1)
            d = dict(res.cookies)
            imname = self.user+".jpg"
            with open("./"+imname,"wb") as f:
                f.write(res.content)
            im = Image.open("./"+imname)
            im.show()
            yzm = input("请输入验证码：")
            time.sleep(1)
            os.remove("./"+imname)
            if len(d)>0:
                self.headers["Cookie"] = "ASP.NET_SessionId=" + d["ASP.NET_SessionId"]
                cookiejar[self.user] = d["ASP.NET_SessionId"]
            else:
                print("注意。。。未获取到cookie")
            data = {
                "action":"login",
                "yhm":self.user,
                "mm":self.pwd,
                "yzm":yzm
            }
            res1 = requests.post("https://cz.hneao.cn/ks/ajax_login.aspx",data=data,headers=self.headers)
            d1 = dict(res1.json())
            if d1["MSG"] == "default.aspx":
                print("登录成功，获取到session id",d["ASP.NET_SessionId"])
        except Exception as e:
            print(self.name,"登录异常，重新登录",e)
            time.sleep(2)
            return self.login()


# url  https://cz.hneao.cn/ks/ajax_operation.aspx
if __name__ == '__main__':
    exceldone()
    time.sleep(1)
    for a,b,c,d in info:
        if a in cookiejar.keys():
            print("cookie in cookiejar!")
            cook = cookiejar[a]
        else:
            cook = ""
        p = Signupsys(a,b,c,d,cook)
        p.run()
        time.sleep(2)
    with open("./hneao.pl","wb") as f:
        pickle.dump(cookiejar,f)
    time.sleep(2)
    print("> END <")
