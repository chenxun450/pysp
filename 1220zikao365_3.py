# -*- coding:utf-8 -*-
import re
import sys
import time
import BeautifulSoup as bs3
from bs4 import BeautifulSoup as Bs4
from lxml import etree
from exams_tools＿old import write_to_exel, request_any
import os
import re


url1 = 'http://member.zikao365.com/tk/phone/paper/getPaperParts.shtm?time=2017-12-23%2015:48:21&courseID={}&pkey=79699f69cd373b08e9949274545dc988'
url2 = 'http://member.zikao365.com/tk/phone/question/getPaperQuestionInfos.shtm?time=2017-12-23%2015:48:22&pkey=2cbaba9b70a9dbbdecf4e092753ea52b&paperID={}'
url3 = 'http://member.zikao365.com/tk/phone/question/getPaperQuestionOptions.shtm?time=2017-12-23%2015:48:22&pkey=2cbaba9b70a9dbbdecf4e092753ea52b&paperID={}'

p1 = re.compile(r"<br  />")
# courseid 1451 paperid 8496
# with open('1course.shtm','r') as f:
#     html1 = f.read()

# with open('2part.shtm','r') as f:
#     html2 = f.read()

# with open('3info.shtm','r') as f:
#     html3 = f.read()
# http://member.zikao365.com/tk/phone/question/getPaperQuestionInfos.shtm?&time=2017-12-20%2015:04:56&updateTime=1999-01-01%2000:00:00&pkey=4f8bf8eb5aad5cba7f5bd0949fde95bd&paperID=

# with open('4option.shtm','r') as f:
#     html4 = f.read()


# xpath不能提取到注释
# dom = etree.HTML(html3)
# l = dom.xpath('')

def get_array(array,dict2):
    con_list = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]

    j = 0
    for li in array:
        question_li = array11()

        j += 1
        question_li[0] = j
        if li[2] == 1 or li[2] == "1":
            li2 = dict2[li[0]]
            question_li[1] = 1
            question_li[2] = li[4]
            for x in range(len(li2)):
                if len(li2) > 6:
                    raise Exception('选项过多')
                question_li[x + 3] = li2[x]
            question_li[9] = li[5].strip()
            if len(li) > 6:
                question_li[10] = li[6]

        elif li[2] == 2 or li[2] == '2':
            li2 = dict2[li[0]]
            question_li[1] = 2
            question_li[2] = li[4]
            for x in range(len(li2)):
                if len(li2) > 6:
                    raise Exception('选项过多')
                question_li[x + 3] = li2[x]
            question_li[9] = li[5].strip()
            if len(li) > 6:
                question_li[10] = li[6]

        else:
            question_li[1] = 4
            question_li[2] = li[4]
            question_li[9] = li[5]
            if len(li) > 6:
                question_li[10] = li[6]
        con_list.append(question_li)

    return con_list


def array11():
    array = []
    for i in range(1,12):
        array.append('')
    return array


def li2dict(li):
    # examples : {questionid: [,,,]}
    dict1 = {}
    for i in range(len(li) // 2):
        if li[2*i] in dict1:
            dict1[li[2*i]] = dict1[li[2*i]] + [li[2*i+1]]
        else:
            dict1[li[2*i]] = [li[2*i +1]]
    return dict1


def html1_handle(html):

    soup = bs3.BeautifulSoup(html)
    li1 = [x.string for x in soup.findAll('courseid')]
    li2 = [x.string for x in soup.findAll('sitecoursename')]
    sub_dict = dict(zip(li1,li2))
    # example: {1305:语文} 76科目
    return sub_dict


def html2_handle(html):
    # 获取该courseid 下的所有试卷
    soup = bs3.BeautifulSoup(html)
    paperli = list(set([x.string for x in soup.findAll("paperid")]))

    return paperli


def html3_handle(html,courseid,coursename):

    soup = bs3.BeautifulSoup(html)
    soup1 = Bs4(html,'lxml')
    if len(soup1.findAll("img")):
        with open('未爬取科目.txt','w+') as f:
            str1 = courseid + "|" + coursename + "\r\n"
            f.write(str1)
        time.sleep(1)
        raise Exception("有图片，无法解析")

    for tag in soup.findAll('status'):
        tag.string = "1*"
    for tag in soup.findAll('count'):
        tag.string = "1*"
    for tag in soup.findAll('score'):
        tag.string = "1*"
    ali = soup.findAll(text=True)
    bli = []
    for x in ali:
        if x.isspace():
            pass
        else:
            x += '||'
            bli.append(x)

    astr = ' '.join(bli)
    bstr = p1.sub('', astr)

    cli = bstr.split("1*||")

    array1 = []
    p = re.compile(r"<.*?>")
    p2 = re.compile(r"参见教材.*?。|参见教材P\d*|参考教材.*?。|参考教材P\d*")
    for x in cli:

        if x.isspace():
            pass
        else:
            xli = x.split("||")
            dli = []
            for x in xli:
                if len(x):
                    a = p2.sub('', x)
                    str1 = p.sub('', a).strip()
                    if not str1.isspace():
                        dli.append(str1)
            if len(dli) > 3:
                array1.append(dli)
    print(array1)
    return array1
    # examples: [[questionid,partid,cls,1,question,answer,anasis],[],[]]


def html4_handle(html):

    soup = bs3.BeautifulSoup(html)
    for x in soup.findAll('sequence'):
        x.string = '*1*'
    li = [x.string for x in soup.findAll(text=True)][1:]
    ali = []
    for l in li:
        # 去掉空格元素
        if l not in ['\n','A','B','C','D','E','F','G','F','*1*']:
            ali.append(l)

    if len(ali[0]) <= 4 and ali[0].isdigit():
        ali = ali[1:]
    # 列表转换字典
    dict = li2dict(ali)
    print(dict)
    # examples : {questionid: [,,,]}
    return dict


def main():
    # con_list = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释'],]
    dict1 = html1_handle(html1) # example: {1305:语文}
    for courseid in dict1:
        url = url1.format(courseid)
        name = dict1[courseid]
        print(url)
        print("准备下载:{},{}".format(name, courseid))
        if not os.path.exists('/home/cxdp/Desktop/tiku'):
            os.mkdir('/home/cxdp/Desktop/tiku')
        filename = name + '1.xlsx'
        path = os.path.join('/home/cxdp/Desktop/tiku/', filename)
        if os.path.exists(path):
            print("已下载过该科目试卷")
            continue
        html2 = request_any.get_html(url)
        time.sleep(1)
        paperli = html2_handle(html2) # [paperid,]

        try:
            if "英语" in name:
                raise Exception("暂不录入英语")
            i = 0
            for paperid in paperli:
                i += 1
                url4 = url2.format(paperid)
                url5 = url3.format(paperid)
                print(url4,url5)
                html3 = request_any.get_html(url4)
                time.sleep(1)
                html4 = request_any.get_html(url5)
                time.sleep(1)
                print("正在下载科目{}，试卷{}".format(name, i))
                array = html3_handle(html3, courseid, name)
                # examples: [[questionid,partid,cls,1,question,answer,anasis],[],[]]
                dict2 = html4_handle(html4)
                # examples : {questionid: [,A,,B,,C,,D]}
                con_list = get_array(array, dict2)
                fname = name + str(i)
                write_to_exel.write_xlsx(fname, con_list)

        except Exception as e:
            print(e)
if __name__ == '__main__':
    main()
