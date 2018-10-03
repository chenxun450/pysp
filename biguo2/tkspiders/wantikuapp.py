# coding:utf-8
import json
import os
import re
import time

import requests

from tools import write_excel

headers = {"Token":"20180124164434-f6f8a27f448dce6eaec4ac5416c8cf5b",
"UserAgent":"android/3.8.7.0",
"SubjectParentId":"549",
"SubjectMergerId":"-1",
"SubjectLevel":"0",
"VersionNumber":"3870",
"UserId":"16041346",
"SubjectId":"557",
"FakesubjectParentId":"549",
"DeviceNumberHeader":"861936bb-dbf2-3198-b83a-1a4f6b5a831c",
"TiKuType":"0",
"WNKSubjectParentId":"0",
"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 7.0; Redmi Note 4X MIUI/V9.0.5.0.NCFCNEI)",
"Host":"api.566.com",
"Connection":"Keep-Alive",
"Accept-Encoding":"gzip"}

def get_html(url):
    res = requests.get(url, headers=headers)
    return res

# 科目管理 http://api.566.com/api/User/UserSubjectNew   返回  SubjectId
def get_subject():
    url = "http://api.566.com/api/User/UserSubjectNew"
    res = get_html(url).text
    res = json.loads(res)
    sub_li =  res["SubjectEntities"]
    li = [(x["SubjectId"],x["SubjectName"])for x in sub_li]
    return li

# 获取真题 http://api.566.com/APP/exam8/Tiku/GetPapers/556/16831728/1/GetRealList/_android/76660416f32131a8315d7316381f3bce  返回json
def get_papers(sub_id,i):
    url0 = "http://api.566.com/APP/exam8/Tiku/GetPapers/"+str(sub_id)+"/16041346/1/GetRealList/_android/76660416f32131a8315d7316381f3bce"
    url1 = "http://api.566.com/api/Imitate/Papers?UserId=16041346&SubjectId="+str(sub_id)+""
    if i == 1:
        url = url0
        res = get_html(url).text
        #print url
        dict_res = json.loads(res)["GetPapersResult"]
        li = [(x["PaperId"], x["PaperName"]) for x in dict_res["EntityList"]]
        return li
    else:
        url = url1
        res = get_html(url).text
        #print url
        title_li = json.loads(res)["Papers"]
        li = [(x["PaperId"],x["PaperName"]) for x in title_li]
        return li
# 获取模拟 http://api.566.com/api/Imitate/Papers?UserId=16041346&SubjectId=550 参数subjectid
# http://api.566.com/APP/exam8/Tiku/Paper/550/16041346/90906400/GetArticleList/_android/e0a4084ece3e68431d7ccf80b84e13eb
# http://api.566.com/APP/exam8/Tiku/Paper/557/16831728/161879918/GetArticleList/_android/e0a4084ece3e68431d7ccf80b84e13eb


class Paper():
    def __init__(self,sub_id,paper_id,paper_name,i,uli):
        self.sub_id = str(sub_id)
        self.paper_id = str(paper_id)
        self.paper_name = paper_name
        self.dir = os.getcwd()
        self.uli = uli
        self.url0 = "http://api.566.com/APP/exam8/Tiku/Paper/"+self.sub_id+"/16041346/"+self.paper_id+"/GetArticleList/_android/e0a4084ece3e68431d7ccf80b84e13eb"
        self.url1 = "http://api.566.com/api/Paper/ImitateExam/?PaperId="+self.paper_id+"&UserId=16041346&UserExamPaperId=0"
        if i ==1:
            self.url = self.url0
        elif i ==2:
            self.url = self.url1
        self.paper_content = None
        self.path = os.getcwd()
        self.i = i
        self.paper_array = [['序号','类型','问题','选项A','选项B','选项C','选项D','选项E','选项F','正确答案','解释']]

    def get_paper(self):
        if self.url in self.uli:
            raise Exception('该链接已下载！！！')
        res = get_html(self.url).text
        dict_res = json.loads(res)["PaperResult"]
        self.paper_content = dict_res["PaperEntity"]


    def get_paper2(self):
        if self.url in self.uli:
            raise Exception('该链接已下载！！！')
        res = get_html(self.url).text
        self.paper_content = json.loads(res)["PaperEntity"]

    def parse(self):
        title_num = 1

        big_li = self.paper_content["TKQuestionsBasicEntityList"]
        for big in big_li:
            # print big
            if "单项选择" in big["QuestionTitle"] or "单选题" in big["QuestionTitle"]:
                cls = 1
            elif "多选题" in big["QuestionTitle"] or "多项选择" in big["QuestionTitle"]:
                cls = 2
            elif "判断题" in big["QuestionTitle"]:
                cls = 3
            else:
                cls = 4
            small_li = big["QuestionsEntityList"]
            for small in small_li:
                #print small
                piece_li = self.array11()
                piece_li[0] = title_num
                piece_li[1] = cls
                piece_li[2] = re.sub('\<\/?\w{0,5}\>|\xe3\x80\x80','',small["FormatContent"]).strip()
                piece_li[9] = re.sub('\<\/?\w{0,5}\>|\xe3\x80\x80','',''.join(small["QuestionsAnswerEntity"]["AnswerArray"])).strip()
                piece_li[10] = re.sub('\<\/?\w{0,5}\>|\xe3\x80\x80','',small["QuestionsAnswerEntity"]["FormatContent"]).strip()
                if cls == 1 or cls == 2:
                    for i,option in enumerate(small["QuestionContentKeyValue"]):
                        if i <= 5:
                            piece_li[i+3] = small["QuestionContentKeyValue"][i]["Value"].strip()
                        else:
                            print("注意>>> 选项过多，请检查%s第%d题"%(self.paper_name, title_num))
                self.paper_array.append(piece_li)
                # print str(piece_li).decode("unicode-escape")
                title_num += 1

    def run(self,):
        if self.i ==1:
            self.get_paper()
        else:
            self.get_paper2()
        time.sleep(0.3)
        self.parse()

    @staticmethod
    def array11():
        array = []
        for i in range(1, 12):
            array.append('')
        return array


def wantiku(signal1): # 万题库爬虫入口

    li1 = get_subject()
    cwd = os.getcwd()
    # if not os.path.exists(cwd+"/wantiku.url"):

    with open(cwd+"/wantiku.uri",'r+') as f1:  # 读取爬取过的链接
        conf = f1.read()
        f1.close()
    # print(conf)
    uli = conf.split(',')
    print("万题库app已爬过的链接数：",len(uli))
    f = open(cwd+"/wantiku.uri",'a+')
    for subid,subname in li1:
        for i in [1,2]:
            li2 = get_papers(subid,i)
            for paperid,papername in li2:
                if "英语" in papername or "外语" in papername or "数" in papername:
                    print('英语数学试卷>>跳过')
                    continue
                signal = signal1
                signal.wait()
                try:
                    paper = Paper(subid,paperid,papername,i,uli)  # 创建试卷对象，并下载试卷
                    paper.run()
                    array = paper.paper_array

                    if len(array)<10:
                        continue
                    else:
                        if i == 1:   # 写入下载过的链接到 uri文件中
                            f.write(paper.url0+',')
                            f.flush()
                            print("写入URL0")
                        else:
                            f.write(paper.url1+",")
                            f.flush()
                            print("写入url1")
                except Exception as e:
                    print(e)
                    continue
                fpath = cwd+'/wantiku'
                if not os.path.exists(fpath):
                    os.mkdir("./wantiku")
                write_excel.write_xlsx(fpath, papername, array)

    f.close()
    print("万题库>>END<<")
if __name__ == '__main__':
    wantiku(1)

