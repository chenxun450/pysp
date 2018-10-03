# coding:utf-8

import requests as req
import re,time,os
from write_to_exel import write_xlsx as writexcel

headers = {
"Accept-Encoding":"gzip",
#"referer":"https://servicewechat.com/wxbc7a043b05e0bbe5/15/page-frame.html",
"reqchannel":"MASTER",
"charset":"utf-8",
'content-type':'application/json',
#"authorization":"eyJhbGciOiJIUzUxMiJ9.eyJhIjpudWxsLCJzIjoibzJFSVYwWkxVc2NQcWpCUklRTkswOGtjYkZ2WSIsImMiOjE1MjY5NTcyMDIwMjgsImUiOjE1MjgyNTMyMDIwMjgsImkiOjEzOTU1NX0.s62yyh9vqyO3hq2BtBbMupCcbQfdljA8cr_a8V4NE_twE6MthZ0-85aN0TTmw3xWcMCHY5s9gBMC7BHsbuBMRQ",
"User-Agent":"Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4X Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.143 Crosswalk/24.53.595.0 XWEB/151 MMWEBSDK/19 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060637) NetType/WIFI Language/zh_CN MicroMessenger/6.6.6.1300(0x26060637) NetType/WIFI Language/zh_CN",
"Connection":"Keep-Alive",
}

s = req.session()
headers1 = headers.copy()
headers1['authorization'] = 'eyJhbGciOiJIUzUxMiJ9.eyJhIjpudWxsLCJzIjoibzJFSVYwWkxVc2NQcWpCUklRTkswOGtjYkZ2WSIsImMiOjE1MjgxMDU1ODE5NTMsImUiOjE1Mjk0MDE1ODE5NTMsImkiOjEzOTU1NX0.I7KBcMsB2gnUpyEtmTABd1Q5kcUs2hKUVNkYw83wShCiyW9TYAftvL-uk67fWQrGX7nAzh5Sope88PzGwH2iGw'

def time1():
    return str(int(time.time()))+'000'

def sendurl(url,head):               # 保存会话
    res = s.get(url,headers=head,verify=False)
    try:
        res.json()
        return res.text, res.content, res.json(), res.status_code
    except Exception as e:
        return res.text,res.content,'',res.status_code

class Paper():
    def __init__(self,cls,paperid,planid):
        self.cls = cls    #  试卷类别
        self.paperid = paperid
        self.paper_array = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]
        self.run(paperid,planid)

    def run(self,paperid,planid):

        if self.cls:  # 根据试卷类别 获取试卷内容
            _, _,papercon, code = sendurl('https://exam.sunlands.site/api/s1/questionTypes/examQuestion?planType=SIMULATION_EXAM&needHistory=0&needAnswer=0&needError=0&stratumId={}'.format(paperid),headers1)
            data = {"answerPlanId": planid, "planType": "SIMULATION_EXAM", "duration": 0, "chapterId": paperid,
                    "assignmentId": paperid, "examPaperId": paperid, "questions": []}

        else:
            _, _, papercon, code = sendurl('https://exam.sunlands.site/api/s1/questionTypes/examQuestion?planType=CHAPTER_PRACTICE&needHistory=0&needAnswer=0&needError=0&stratumId={}'.format(paperid),headers1)
            data = {"answerPlanId": planid, "planType": "CHAPTER_PRACTICE", "duration": 0, "chapterId": paperid,
                    "assignmentId": paperid, "examPaperId": paperid, "questions": []}

        # 构建post 的json数据，获取 答案的planid
        for each in papercon:
            d = {}
            d["questionId"] = each["questionId"]
            d["answerDesc"] = ''
            d["duration"] = 0
            d["questionType"] = each["questionType"]
            data["questions"].append(d)
        res = s.post('https://exam.sunlands.site/api/s1/userAnswer', json=data, headers=headers1,verify=False)
        try:
            d = res.json()
            ansid = d["userAnswerId"]
        except Exception as e:
            print('--没有获取到答案id-', e)
            print('---', res.text())
            ansid = ''

        # 根据答案id 获取答案
        _, _, json_answer, code = sendurl(
            'https://exam.sunlands.site/api/s1/userAnswer/{}?userAnswerId={}&infoType=answerDone'.format(ansid, ansid),
            headers1)  # userId 139555 answerPlanId391206
        ansli = json_answer["questions"]

        if len(ansli) == len(papercon):
            qsli = zip(papercon,ansli)
        else:
            print("注意！！！检查")
            qsli = zip(papercon,ansli)

        # 解析试卷内容和答案
        for item,ans in qsli:
            ali = self.empty_li()
            ali[0] = len(self.paper_array)
            if item['questionType'] == "MULTIPLE_ANSWER":
                ali[1] = 2
            elif item['questionType'] == "SINGLE_ANSWER":
                ali[1] = 1
            else:
                ali[1] = 4

            for i, option in enumerate(item['options']):
                if i > 5:
                    print('选项超过6个，忽略')
                else:
                    ali[3 + i] = option["optionDesc"]
            ali[2] = item['questionDesc']
            ali[9] = ans["correctAnswer"].strip()
            ali[10] = ans["correctAnswerDesc"].strip()
            self.paper_array.append(ali)

    @staticmethod
    def empty_li():
        array = ['' for i in range(11)]
        return array

def worker(cls,subname='',):
    # 对试卷进行处理
    cwd = os.getcwd()
    fpath = cwd + "/shangtiku"

    # 根据获取 PlanId   # {"answerPlanId":446289,"chapterPractice":true,"highWrongPractice":true,"randomPractice":true,}
    _, _, ansplan, _ = sendurl('https://exam.sunlands.site/api/s3/answerPlans', headers1)
    planid = ansplan['answerPlanId']

    if cls:
        _, _, examsli, code = sendurl('https://exam.sunlands.site/api/s3/questionTypes/examPapers', headers1)
        for exam in examsli:
            paperid = exam["examPapersId"]
            papername = exam["examPaperName"]
            try:
                print('试卷名字',papername)
                date = str(re.findall('\d{4}',papername)[0])
            except:
                date = '7001'
                print("没有获取到时间")
            if date[0] == '1' or date[0] == '0':
                year,month = date[0:2],date[2:]
                papername = '20'+ year + '年' + month + '月' +re.sub('\d{4}','',papername)
            else:
                pass
            if "模拟" in papername:
                papercls = 1
            else:
                papercls = 0
            p = Paper(cls,paperid,planid)
            time.sleep(0.1)
            writexcel(fpath,papername,p.paper_array)

    else:
        _, _, examsli0, code = sendurl('https://exam.sunlands.site/api/s1/questionTypes/chapters?planType=CHAPTER_PRACTICE',headers1)
        for exam in examsli0['chapters']:
            paperid = exam["chapterId"]
            papername = exam["chapterName"]

            if "模拟" in papername:
                papercls = 1
            else:
                papercls = 0
            p = Paper(cls,paperid,planid)
            time.sleep(0.1)
            papername = subname + papername
            writexcel(fpath,papername,p.paper_array)
            # 最终写入excel。。 结束

def shangtiku():
    '''
    程序入口
    :return:
    '''
    _, _, typesli, code = sendurl('https://exam.sunlands.site/api/s1/examTypes', headers1)
    print(typesli)
    ali = typesli[0]['items']
    subdict = {}
    subli = []

    cwd = os.getcwd()
    if os.path.exists(cwd+'/shangtiku'):
        os.makedirs(cwd+'/shangtiku')

    for t in ali:
        typename = t['primaryCategories']
        typeid = t['examTypeId']
        _, _, subsli, code = sendurl('https://exam.sunlands.site/api/s1/subjects?examTypeId={}'.format(typeid),headers1)    # 获取科目列表 subid
        for u in subsli:
            subdict[u['subjectName']] = u['subjectId']
            subli.append([u['subjectName'],u['subjectId']])

    for subname,subid in subli:
        res = s.put('https://exam.sunlands.site/api/s3/users/subjects?subjectId={}'.format(subid),headers=headers1,verify=False)
        print('切换到下一个科目',res.text)
        time.sleep(0.3)
        worker(1,)           # 处理试卷>>
        worker(0,subname)           # 处理章节习题>>

    print(">>END<<")
if __name__ == '__main__':
    shangtiku()




