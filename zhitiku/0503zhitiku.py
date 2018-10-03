# coding:utf-8
import requests as rq
import re
import os,time,random
import write_to_exel as wte
cwd = os.getcwd()
'''
User-Agent: Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; Redmi Note 4X Build/NRD90M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30
Accept-Encoding: gzip
Cookie: _tenant=default; org.springframework.mobile.device.site.CookieSitePreferenceRepository.SITE_PREFERENCE=MOBILE; JSESSIONID=47998EE6535231B2F1121124D4120A59
'''

# http://www.edu-edu.com/exam-admin/home/my/admin/real/questionbank/question/attaches/
gheader1 = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; Redmi Note 4X Build/NRD90M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=69FBA50D2C34956FF886C99C3B701C75; _tenant=default; JSESSIONID=22944F58A0D880FCA84F16F7C81A8F14; JSESSIONID=DCCA42412A3BD96E7718638DBD48A9F8; org.springframework.mobile.device.site.CookieSitePreferenceRepository.SITE_PREFERENCE=MOBILE",
           }
gheader = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; Redmi Note 4X Build/NRD90M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip",}
s = rq.session()


def sendurl(url0,headers):
    res = rq.get(url0,headers=headers)
    try:
        res.json()
        return res.text,res.content,res.json(),res.status_code
    except Exception as e:
        return res.text,res.content,'',res.status_code


def sendurl1(url0,headers):              # 保存会话状态
    res = s.get(url0,headers=headers)
    try:
        res.json()
        return res.text,res.content,res.json(),res.status_code
    except Exception as e:
        return res.text,res.content,'',res.status_code

def auth():                  # 登录验证 ， 保存cookie，供本次爬虫试用
    data = {"userid":"15527301530","password":"11980389","service":"http://www.edu-edu.com/exam-admin/cas_security_check"}
    url0 = 'http://www.edu-edu.com/cas/client/get_tgt'  # post
    url1 = 'http://www.edu-edu.com/exam-admin/cas_security_check?' #st=ST-404-MhLEdabcam2eNEUpdnFrQnJERqPQQLCbCrg
    res = s.post(url=url0, data=data, headers=gheader)
    print(s.cookies,'\nPOST 结果',res.text,[(item,value) for item,value in res.cookies.iteritems()])
    tgt, st = res.json()["tgt"], res.json()["st"]
    data1 = {'st':st,"site_preference":"mobile","ct":"client"}
    res1 = s.get(url=url1,params=data1,headers=gheader)
    print(s.cookies,"\nget请求认证",res1.text)
    # res2 = s.get('http://www.edu-edu.com/exam-admin/home/my/real/exam/view/result/json/117?page=1&pageCount=10&site_preference=mobile&ct=client',headers=gheader)
    # print(s.cookies,"\n试卷：",res2.text)
    # res3 = s.get('http://www.edu-edu.com/exam-admin/home/my/real/exam/all/questions/details/json/1_1219022_1525683804764',headers=gheader)
    # print(s.cookies,"\n试卷内容：",res3.text)

class Paper():
    def __init__(self,examid,fname):                         # 初始化试卷
        self.url = 'http://www.edu-edu.com/exam-admin/home/my/real/exam/start/json/' + str(examid)
        self.fname = fname
        # self.headers1 = gheader
        # self.headers1["Cookie"] = "_tenant=default; org.springframework.mobile.device.site.CookieSitePreferenceRepository.SITE_PREFERENCE=MOBILE; JSESSIONID=6F0A7E9A222FB8AAEB49C637E14A66A9"
        self.bigs = {}
        self.res,_,self.json,_ = sendurl1(self.url,gheader)
        self.paper_classid = ''
        self.paper_array = [['序号','类型','问题','选项A','选项B','选项C','选项D','选项E','选项F','正确答案','解释']]
        self.paper_array1 = [['序号','类型','问题','选项A','选项B','选项C','选项D','选项E','选项F','正确答案','解释']]
        self.imgli = []
        self.run()

    def _deal_res(self):
        # print('》获取的试卷内容如下《','\n',self.json)
        self.userexam_id = self.json['userExamId']
        url = 'http://www.edu-edu.com/exam-admin/home/my/real/exam/all/questions/details/json/'+ self.userexam_id
        _,_,json1,_ = sendurl1(url,gheader)
        if not json1:
            print('没有返回json,第77')
            pass
        d = json1["details"]
        if json1["success"]:
            self.bigs = d
        else:
            print("没有请求到数据,第83")

    def get_papper_classid(self):               # 判断试卷类型
        pass

    def parse_bigs(self, big, smali,coid=0):                   # 解析题目。coid 为备用文档的标记
        if big == "singles":
            cls = 1
        elif big == "multis":
            cls = 2
        elif big == "texts":
            cls = 4
        else:
            cls = 0
            print("WTF?")
        for each in smali:

            li = self.empty_li()
            li[1] = cls
            if coid:                      # bak备份的excel文件
                li[0] = len(self.paper_array1)
                li[2] = re.sub('\</?p\>|[(（]本小题.{1,4}分[）)]\n|[(（]本小题.{1,4}分[）)]','',each["title"])
                li[2] = re.sub('^\d{1,3}[、.．](?=[\D])','',li[2])
                li[2] = re.sub('upload/file/\d{1,7}/(\w{1,10})\?__id=(.{1,32}\.\w{1,4})','\g<1>_\g<2>',li[2], flags=re.I)
                li[9] = each['answer'].strip()
                li[9] = re.sub('upload/file/\d{1,7}/(\w{1,10})\?__id=(.{1,32}\.\w{1,4})','\g<1>_\g<2>', li[9], flags=re.I)
                li[10] = each["hint"]
                li[10] = re.sub('upload/file/\d{1,7}/(\w{1,10})\?__id=(.{1,32}\.\w{1,4})','\g<1>_\g<2>', li[10], flags=re.I)
                if isinstance(each["questionChoices"],list):
                    for i,choice in enumerate(each["questionChoices"]):
                        if i >= 6:
                            print("选项太多，请注意")
                            pass
                        li[i+3] = re.sub('^[A-F][、.．]?','',choice["content"])
                        li[i+3] = re.sub('upload/file/\d{1,7}/(\w{1,10})\?__id=(.{1,32}\.\w{1,4})','\g<1>_\g<2>', li[i+3], flags=re.I)
                else:
                    if cls != 4:
                        print(li[0],"--没有选项：",each["questionChoices"])

                # l = [str(i) for i in li]
                # str1 = ''.join(l)
                # img = re.findall("<img.{0,30}src=\"(.{10,100}?)\".*?>", str1, flags=re.I)
                # for i in img:
                #     if i not in self.imgli:
                #         self.imgli.append(i)
                self.paper_array1.append(li)
            else:
                li[0] = len(self.paper_array)
                li[2] = re.sub('\</?p\>|[(（]本小题.{1,4}分[）)]\n|[(（]本小题.{1,4}分[）)]', '', each["title"])
                li[2] = re.sub('^\d{1,3}[、.．](?=[\D])', '', li[2])
                li[9] = each['answer'].strip()
                li[10] = each["hint"]
                if isinstance(each["questionChoices"], list):
                    for i, choice in enumerate(each["questionChoices"]):
                        if i >= 6:
                            print("选项太多，请注意")
                            pass
                        li[i + 3] = re.sub('^[A-F][、.．]?', '', choice["content"])
                else:
                    if cls != 4:
                        print(li[0], "--没有选项：", each["questionChoices"])

                l = [str(i) for i in li]
                str1 = ''.join(l)
                img = re.findall("<img.{0,30}src=\"(.{10,100}?)\".{0,50}?>", str1, flags=re.I)
                for i in img:
                    if i not in self.imgli:
                        self.imgli.append(i)
                self.paper_array.append(li)


    def save_img(self):                         # 图片的保存 和 分类
        print(self.fname,'试题图片个数：',len(self.imgli),self.imgli)
        for uri in self.imgli:
            url = 'http://www.edu-edu.com/exam-admin/home/my/admin/real/questionbank/question/attaches/' + uri
            _, content, _, code = sendurl1(url, gheader)
            if code != 200:
                print("--code:",code,"图片未请求到",uri)
                if "ANSWER" not in uri:
                    _, content, _, code = sendurl1(url, gheader)
                    print("----重新获取该图片")
            else:
                a,b = re.findall('(?<!//)(?<=/)([^/]{1,32}?)\?.{1,5}=([^/]{1,32}?\..{2,4})',uri)[0]
                imgname = a + "_" + b
                print("正在下载图片：",imgname,end='|')
                path = cwd + "/zhitiku/" + self.fname + '_img/'
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(path+imgname,'wb') as f:
                    f.write(content)
        print('\n')

    def run(self):
        try:
            self._deal_res()
            self.parse_bigs("singles",self.bigs["singles"])
            self.parse_bigs("multis",self.bigs["multis"])
            self.parse_bigs("texts",self.bigs["texts"])
            self.parse_bigs("singles", self.bigs["singles"],coid=1)
            self.parse_bigs("multis", self.bigs["multis"],coid=1)
            self.parse_bigs("texts", self.bigs["texts"],coid=1)
            #self.save_img()

        except Exception as e:
            print(">>注意：",e)

    @staticmethod
    def empty_li():
        array = ['' for i in range(11)]
        return array

    def __str__(self):
        return self.paper_array


def deal_paper(fpath,examli,subname):

    for examid,year,month in examli:    ### examli
        url = 'http://www.edu-edu.com/exam-admin/home/my/real/exam/start/json/' + str(examid)
        ### >>>加入爬虫平台所需的功能
        #if url not in zhitikuurl:                  # subname ↓
        fname = str(year) + "年" + str(month) + "月" + subname 
        p = Paper(examid,fname)
        # con_list = p.paper_array
        # wte.write_xlsx(fpath=fpath,fname=fname,con_list=con_list)
        wte.write_xlsx(fpath,"bak"+fname,p.paper_array1)
        # 写完文件后，需把url 写入zhitiku.uri中
        # else:
        #    print("该试卷已下载过")


def zhitiku():
    fpath = cwd + "/zhitiku"
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    ### 此处需添加一个zhitiku.uri 作为下载过的列表文件
    #
    url1 = 'http://www.edu-edu.com/exam-admin/real/public/subjects/json'
    headers1 = gheader
    _,_,json1,status1 = sendurl(url0=url1,headers=headers1)

    try:
        publi = [(item["code"],item['id'],item['name']) for item in json1["subjectMap"]["public"]]  # 获取要下载的科目列表
        majli = [(item["code"],item['id'],item['name']) for item in json1["subjectMap"]["major"]]

        print("公共课：",publi,'\n',"专业课：",majli)
        subli = publi + majli
        auth()  # 进行验证

        for code,id,subname in subli:
            url2 = "http://www.edu-edu.com/exam-admin/real/public/exams/json/" + str(id)
            _,_,json2,status2 = sendurl1(url2,headers1)
            # print("试卷json：",json2["exams"])
            examli = []
            for item in json2["exams"]:
                li = re.findall(r"(\d{2,4})年(\d{1,2})月",item["examTitle"])
                if len(li) > 0:
                    i = item["examId"],li[0][0],li[0][1]
                    examli.append(i)

                else: # 没获取到年月
                    i = item["examId"],random.randint(3000,9999),random.randint(13,99)
                    examli.append(i)
            # 根据科目获取试卷列表 [(examid,nian,yue)]
            deal_paper(fpath, examli,subname)
    except Exception as e:
        print(e,"*注意*")

    print('>>>End<<<')

if __name__ == '__main__':
    zhitiku()
