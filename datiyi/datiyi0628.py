# coding:utf-8

import random
import os,re,time
import requests
from lxml import etree
import sys
from PIL import Image
from shibie import tessocr
from write_to_exel import write_xlsx as wtex
sys.setrecursionlimit(1000000)

p = re.compile("\d{4,5}")
s = requests.session()
uri = "http://www.datiyi.com/"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
           }
cookie = {"Cookie":"loginUrlReferrer=http://www.datiyi.com/"}
forms = {"__VIEWSTATE":"/wEPDwULLTE0MTEwMDk3MjQPZBYCAgIPZBYCAgkPDxYCHgRUZXh0BZABPGRpdiBpZD0nZm9vdGVyJz4gPHNwYW4gY2xhc3M9J2FzaHR4dCc+Q29weXJpZ2h0wqkyMDE3IGRhdGl5aS5jb20gPGEgaHJlZj0naHR0cDovL3d3dy5taWl0YmVpYW4uZ292LmNuJz4g57KkSUNQ5aSHMTUwNTcwNDDlj7c8L2E+PC9zcGFuPiAgPC9kaXY+ZGRkZOQi0Sg7cQjQElSdXYhS7Enhpzs=",
        "__EVENTVALIDATION":"/wEWBALAk7PkDAL/0fDaBwKns6TyDgLc7/3ICyk19ajyVXaJzOx76Tj0r/5LwAgo",
        "khTxb":"ba460",
         "passwordTxb":"b5d7f12f38477b2cdd237e2771dde211",
         "submitBtn":"登录"}
headers2 = dict(headers,**cookie)
kmli = []

def login():
    '''
    :return:
    '''
    try:
        s.get(uri+"login.aspx",headers=headers,timeout=25)
        res = s.post(uri+"login.aspx",data=forms,headers=headers2,timeout=25)
        print(res.cookies.items(),sep="\n")
    except Exception as e:
        print(e,"登陆超时，正在重登陆")
        return login()


def _getkemu():
    '''
    :return:
    '''
    res_major = s.get(uri, headers=headers,timeout=25)
    htmlele = etree.HTML(res_major.text)
    majorurili = htmlele.xpath('//*[@id="zhuankeDiv"]/ul/li/a/@href|//*[@id="benkeDiv"]/ul/li/a/@href')
    for l in majorurili:
        kmurl = uri + l
        reskemu = s.get(kmurl,headers=headers,timeout=25)
        htmlele = etree.HTML(reskemu.text)
        kmulli = htmlele.xpath('//*[@id="kemuShowLbl"]/div/ul/li/a/@href')
        subnameli = htmlele.xpath('//*[@id="kemuShowLbl"]/div/ul/li/a/text()')
        global kmli
        for ul,subname in zip(kmulli,subnameli):
            kmcode = p.findall(ul)[0]
            if kmcode not in kmli:
                kmli.append(subname)
                kmli.append(kmcode)
                kmli.append(ul)
            else:
                pass
    gettk()


def gettk():
    '''
    # 根据科目列表获取题库列表
    并 写入excel中，结束爬虫
    :return:
    '''
    try:
        with open("datiyicache.uri","r") as f:
            content = f.read()
            f.close()
    except:
        content = ''
    doli = content.split(",")
    cwd = os.getcwd()
    if not os.path.exists(cwd+'/datiyi'):
        os.makedirs(cwd+"/datiyi")
    for i in range(len(kmli)//3):
        subname = kmli[i*3]

        subname = re.sub("\*",'',subname)

        if "英语" in subname or "外语" in subname or "外贸函电" in subname:  # 略过英语
            continue
        else:
            pass
        kmcode = kmli[i*3+1]
        fpath = cwd + '/datiyi/' + subname
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        ul = kmli[i*3+2]
        url = uri + ul
        html = s.get(url,headers=headers,timeout=25).text
        htmlele = etree.HTML(html)
        tkuli =  htmlele.xpath('//*[@id="chapterLbl"]/div/a[contains(text(),"题库")]/@href')
        fnameli = [o for o in htmlele.xpath('//*[@id="chapterLbl"]/div/a[contains(text(),"题库")]/../text()') if len(o) > 1]
        if subname == "00022 高等数学（工专）":
            print("高数：：",tkuli,fnameli)
        for ul0,fname in zip(tkuli,fnameli):  # 遍历 章节 ，章节名
            url0 = uri + ul0
            fname = re.sub("[\tt*]",'',fname)
            pp = fpath+"/"+fname+".xlsx"
            print(pp)
            if os.path.exists(pp):
                print("题库已下载")
            elif ul0 in doli:
                print("空题库，上一次检查时间为")
            else:
                p = Paper(ul0)
                arr = p.zjarray
                if len(arr) > 4 and p !=1:
                    wtex(fpath,fname,arr)
                else:
                    print("题目太少")
                    with open("datiyicache.uri","a+") as f:
                        f.write(ul0+",")

class Paper():

    def __init__(self,ul):
        self.stul = ul
        self.zjarray = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]
        self.yzt_resolver = []  # 验证题答案
        self.yzt_html = ""
        self.yzt_optionli = []
        self.yzt_cls = 0
        self.notdo = 0
        self._dohtml(self.stul)

    def _dohtml(self, ul, mode=1):
        '''
        获取小题内容
        :param ul:
        :param mode:mode1 为一般模式，模式2为测试题自动跳转到的页面 mode3:测试题页面   mode4:验证码页面  mode5:重登录后
        :return:  ①func _getitem(yzt_resolver) ② 跳转下一页 func _getitem(nextul)
                 ③ 选择验证码 func _getitem(selectul)
        '''
        try:
            url1 = uri + ul
            html = s.get(url1,headers=headers,timeout=25).text
            htmlele = etree.HTML(html)

            clsstrli = htmlele.xpath('//span[@class="question_Type"]/text()')
            yzuli = htmlele.xpath('//span[contains(text(),"自动跳转")]/a/@href')
            smallti = re.findall('<span[^<]{0,30}class="question_title"[^>]{0,30}>(?:<span.{0,30}?</span>)?(.{0,20000}?)</span', html,re.DOTALL)
            answerli = re.findall('<div[^<]{0,30}class="item"[^>]{0,30}>(?:<span.{0,30}?</span>)?(.{0,6000}?)<span', html, re.DOTALL)
            nexulli = htmlele.xpath('//*[@id="tqNumNextLbl"]/a[contains(text(),"下一题")]/@href')
            relocli = htmlele.xpath('//form[@id="ctl00"]/@action')
            relodli = htmlele.xpath('//*[@id="questionLbl"]/script[contains(text(),"reload")]')
            changshili = htmlele.xpath('/html/head/title[contains(text(),"生活常识")]')
            yztopli = htmlele.xpath('//*[@id="RBtnL"]/./tr/td/label/text()')

            if len(htmlele.xpath('//script[contains(text(),"请先登录")]'))>0: # 则需要重新登录
                print("--正在重新登录模式1...")
                login()
                return self._dohtml(relocli[0].lstrip("/"))
            if len(yzuli) > 0:
                if len(yzuli[0]) < 15:
                    print("--正在重新登录模式2...")
                    login()
                    return self._dohtml(relocli[0].lstrip("/"),mode=3)
                else:
                    print("--正在跳转到测试题...")
                    return self._dohtml(yzuli[0].lstrip("/"),mode=3)
            if len(relodli)>0:
                print("--正在重新加载")
                return self._dohtml(ul)

            optionli = []
            if len(clsstrli) > 0: # 获取到题目类型

                if len(answerli) > 0:
                    ans = re.sub('<br/>|&nbsp;',' ',answerli[0])
                else:
                    print("-----没找到答案")
                    ans = ''
                opli1 = re.findall(
                    '<span[^<]{0,30}class="question_title".+?</span>.{0,100}?(?:<br/>\n?([ABCDEF].*?)(?=<br/>\n?))(?:<br/>\n?([ABCDEF].*?)(?=<br/>\n?))(?:<br/>\n?([ABCDEF].*?)(?=<br/>\n?))(?:<br/>\n?([ABCDEF].*?)(?=<br/>\n?))?(?:<br/>\n?([ABCDEF].*?)(?=<br/>\n?))?(?:<br/>\n?([ABCDEF].*?)(?=<br/>\n?))?',html, re.DOTALL)
                if "单项" in clsstrli[0]:
                    cls = 1
                    if mode !=3:
                        optionli = self.getoption(opli1)
                elif "多项" in clsstrli[0]:
                    cls = 2
                    if mode !=3:
                        optionli = self.getoption(opli1)
                else:
                    cls = 4

                if mode == 3: # “回答验证题”
                    self.yzt_html = self.yzt_html+html
                    self.yzt_cls = cls
                    self.yzt_optionli = optionli
                    vst = htmlele.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                    evtval = htmlele.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                    postuli = htmlele.xpath('//*[@id="ctl00"]/@action')
                    flag =0
                    if len(changshili) >0:
                        flag = 1
                    if len(htmlele.xpath(
                            '//*[@id="questionLbl"]/span[@class="question_Type" and contains(text(),"项选择")]')) > 0:
                        return self.commit(postuli[0], vst, evtval, cls,smallti,flag=flag,opli=yztopli)
                    else:
                        print("没有选择题,直接提交")
                        return self.commit(postuli[0], vst, evtval, 4,smallti)

                # 解析题目
                self.getitem(smallti[0], cls, optionli, ans)

                if len(nexulli) > 0: # 有下一页
                    return self._dohtml(nexulli[0])
                else: # 无下一页 则
                    imuli = htmlele.xpath('//*[@id="tqcodeimg"]/@src')
                    if len(imuli) > 0:  # 有验证码
                        selectuli = htmlele.xpath('//*[@id="tqNumNextLbl"]/a/@href')
                        strnum = self.rec(imuli[0])
                        a = re.sub("checkNum=[1234]", "checkNum={}".format(strnum), selectuli[0])
                        s.get(uri+a,headers=headers,timeout=25)
                        time.sleep(0.1)
                        return self._dohtml(a,mode=4)
                    else:  # 没有验证码
                        print("没有验证码（有题）")
                    print("改章节题爬取完毕")
            else: #  没获取到题目类型，无题目
                if len(nexulli)>0: # 有下一页
                    return self._dohtml(nexulli[0])
                else:  # 无下一页 则
                    imuli = htmlele.xpath('//*[@id="tqcodeimg"]/@src')
                    if len(imuli)>0:# 有验证码
                        selectuli = htmlele.xpath('//*[@id="tqNumNextLbl"]/a/@href')
                        strnum = self.rec(imuli[0])
                        a = re.sub("checkNum=[1234]", "checkNum={}".format(strnum), selectuli[0])
                        return self._dohtml(a,mode=4)
                    else:  # 没有验证码
                        print("没有验证码(无题)")
                    if mode ==4:
                        print("--未加载完全，重打开链接2")
                        return self._dohtml(ul) # 如果是第四类 则重新发送请求
                    elif mode ==3:
                        uli = re.findall("location\.href=['\"]([^'\"]+)['\"]", html)
                        if len(uli) >0:
                            return self._dohtml(uli[0],mode=3)
                    elif mode ==5:
                        print("--未加载完全，重打开链接1")
                        return self._dohtml(ul) # 如果是第五类 则重新发送请求
                    if mode !=6:
                        return self._dohtml(ul,mode=6)
        except Exception as e:
            print(e,"超时，注意>>>")
            print("----",ul)
            return self._dohtml(ul)

    def dooption(self,optionli):
        li = []
        for i in optionli:
            l = re.findall('^[ABCDEF \s](.+)',i,re.DOTALL)
            if len(l) > 0:
                li.append(l[0])
        return li

    def getoption(self,opli1):

        if len(opli1) > 0:
            optionli = [i for i in opli1[0] if len(i) > 0]
        else:
            print("注意该选择题 没获取到选项")
            optionli = []
        if len(optionli) > 6:
            optionli = self.dooption(optionli)
        return optionli

    def getitem(self,small,cls,optionli,ans): # 保存题目到列表
        empli = self.empty_li()
        empli[0] = len(self.zjarray)
        empli[1] = cls

        # # ↓↓ 修改的时候注意要把缓存题库self.yzt_resolver前的small 一起处理
        small = re.sub('\(.{0,12}真题\)|</?u>','',small)
        empli[2] = re.sub('&nbsp;', '', small).lstrip()
        for i, op in enumerate(optionli):
            empli[i + 3] = re.sub('^[ABCDEF]|&nbsp;', '', op)
        if cls == 1 or cls == 2:
            ali = re.findall("^[abcdefABCDEFＡＢＣＤＥＦ \s]{1,6}", ans)
            if cls == 1:
                ali = re.findall("^[abcdefABCDEFＡＢＣＤＥＦ \s]", ans)
            if len(ali) > 0:
                a = ali[0].replace(" ", '')
                a = a.replace("Ａ","A").replace("Ｂ","B").replace("Ｃ","C").replace("Ｄ","D").replace("Ｅ","E").replace("Ｆ","F")
                if len(a)>1:
                    if a[-1] < a[-2]:
                        a=a[:-1]
                empli[9] = a.strip().upper()
            else:
                empli[9] = ''
            empli[10] = re.sub("^[abcdefABCDEFＡＢＣＤＥＦ \s]{1,6}", '', ans).strip()
            if len(self.yzt_resolver)>=20:
                self.yzt_resolver.pop(0)
                self.yzt_resolver.pop(0)
            self.yzt_resolver.append(empli[2])
            self.yzt_resolver.append(empli[9])
        else:
            empli[9] = ans.strip()
        self.zjarray.append(empli)
        print("抓到一个题")

    def commit(self,ul,vst,evtval,cls,smallti,flag=0,opli='',answ="",cnt=0):
        '''

        :param ul: 提交链接
        :param vst: 验证
        :param evtval: 验证
        :param cls: 题目类型
        :param smallti: 小题内容list
        :param flag: 常识题标记
        :param opli: 验证题的选项
        :param answ: 验证题的答案 list
        :param cnt: 第几次验证
        :return:
        '''
        url = uri + ul
        small = smallti[0]
        # # ↓ ↓ 处理相同
        small = re.sub('\(.{0,12}真题\)|</?u>', '', small) #
        ques = re.sub('&nbsp;','',small).lstrip()
        if ques in self.yzt_resolver:
            ind = self.yzt_resolver.index(ques)
            answ = self.yzt_resolver[ind + 1]
            if cnt ==1:
                answ = answ
        else: # 如果答案不在列表中，则提交空答案
            answ = answ
            if flag ==1:
                print("↓↓手动回答生活常识题↓↓↓")
                print(ques, "↓↓")
                print(opli)
                answ = input("请输入正确答案：")
        if cls == 1:  # 选择题从yzt中选
            data = {"__VIEWSTATE": vst, '__EVENTVALIDATION': evtval, 'RBtnL': answ, 'SubmitAnswerBtn': "提交",
                    "adviceTxb": ""}
        elif cls == 2:
            d1 = {}
            for i in answ:
                if i =="A":
                    d1["CkBoxL$0"] = "on"
                elif i =="B":
                    d1["CkBoxL$1"] = "on"
                elif i == "C":
                    d1["CkBoxL$2"] = "on"
                elif i == "D":
                    d1["CkBoxL$3"] = "on"
                elif i == "E":
                    d1["CkBoxL$4"] = "on"
                elif i == "F":
                    d1["CkBoxL$5"] = "on"
            data = {"__VIEWSTATE": vst, '__EVENTVALIDATION': evtval, 'SubmitAnswerBtn': "提交",
                    "adviceTxb": ""}
            data.update(d1)
        else:  # 直接提交
            data = {"__VIEWSTATE": vst, '__EVENTVALIDATION': evtval, 'txtAnswerTxb': '', 'SubmitAnswerBtn': "提交",
                    "adviceTxb": ""}
        res = s.post(url, data=data, headers=headers)
        htmlele = etree.HTML(res.text)

        wrongli = htmlele.xpath('//span[contains(text(),"选择错误")]')
        corli = htmlele.xpath('//span[contains(text(),"回答正确")]')
        uli = re.findall("location\.href=['\"]([^'\"]+)['\"]", res.text)

        ul = uli[0]
        ul = re.sub("https?://www\.datiyi\.com/",'',ul)
        if len(corli) > 0: # 选择正确直接跳转到下一页
            print("--测试题，选择正确，获取下一题")
            return self._dohtml(ul.lstrip("/"))
        if cls ==4 and len(uli)>0: # 问答题测试题 直接提交，跳转到下一题
            print("--直接提交问答测试题，跳转下一题")
            return self._dohtml(ul.lstrip("/"))
        if len(wrongli)>0:
            if cnt ==1:
                self.notdo = 1
                return self._dohtml()

            print("↓↓手动回答题目↓↓↓")
            print(ques,"↓↓")
            print(opli)
            #ans = input("请输入正确答案：")
            ans = random.choice("ABCD")
            return self.commit(ul,vst,evtval,cls,smallti,answ=ans,cnt=1)


    def rec(self,imul):
        imurl = uri + imul
        imbit = s.get(imurl, headers=headers,timeout=25).content
        f = open("cache.gif", "wb+")
        f.write(imbit)
        im = Image.open(f)
        snum = tessocr.recogit(im)
        print("识别... 数字：",snum)
        f.close()
        os.remove("cache.gif")
        if snum in ["1","2","3","4"]:
            return snum
        else:
            return self.rec(imul)

    @staticmethod
    def empty_li():
        array = ['' for i in range(11)]
        return array


if __name__ == '__main__':
    login()
    _getkemu()

    print(">>datiyi END<<")
