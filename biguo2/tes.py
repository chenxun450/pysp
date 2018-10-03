import requests
from requests_toolbelt.multipart import MultipartEncoder
# "X-CSRF-TOKEN":" 9HJB9MwNrmPvV1rnbbpi021YIeHuLGzxe9D0S8Yl",

def req2():
    headers = {
    "X-CSRF-TOKEN":"9HJB9MwNrmPvV1rnbbpi021YIeHuLGzxe9D0S8Yl",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With":"XMLHttpRequest",
    "Referer":"http://www.biguotk.com/admin/login",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    "Cookie":"XSRF-TOKEN=eyJpdiI6Im4yRVwvTlA2RExzYXllV1BcL3I1SERsQT09IiwidmFsdWUiOiJ1b0x5WnF6bkI2bUNveENvdmlPK2ZaeEpcL1BJVXB1b3hQV1NLVlNUdGhxdWJZSXFFUjN3M2RRRFwvaUNZVzFBVWF3NURjVmJGYVwvUzl3NzJOQndvMkUrdz09IiwibWFjIjoiMWNhYjRjMTQ5YmExZjlkZmFjZGM2MTJmZDRhMDBlN2M0YTRlZWQzMTE5NGZmNDM5ZGNhNjYxN2U4YTUwMDM4OSJ9; laravel_session=wvGGZsyHrxYeGkXyzH1L5jOgdAMVRiAXbEMbxUAJ"}
    url = "http://www.biguotk.com/admin/login/20186663312"
    formdata = {"account":"cx450","password":"11980389",}
    res = requests.post(url,formdata,headers=headers)
    print(res.text)
    res.xpath("//script[re:test(string(.),'href=\"[^\"]*?(?:pdf|xlsx)\"')]").re('href="([^\"]*?(?:pdf|xlsx))"')

    cookiejar = res.cookies
    for item in cookiejar:
        print(item.name,item.value)

def req1():
    headers = {
    "X-CSRF-TOKEN":"fRQiJBkLt9Wri0LKmyp7hqaQB8XqhOzkmL71lBeL",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With":"XMLHttpRequest",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    "Cookie":"XSRF-TOKEN=eyJpdiI6IlpZYTVsUlVTbE9Bc21IXC9wNHhFQWFRPT0iLCJ2YWx1ZSI6ImRpOUkrQUNiSW50aTR5WVpIQk5iUW1OUnZlbmkyZHZCTVVcL2VveTZZWlQzVFV6RjhTVUE3czRyYkhwTlI0Z1hTakNKdDJQT0hKS1BueTNJZk15RmxJZz09IiwibWFjIjoiMzFjZjdiZWMyNTBiMWJkNDg3YzhjZDlmYjFiODQ0MzdkOWY2YjQyZjg2OWQ5MjIzZThiNGYwYzg4OTRhNjBlNCJ9; laravel_session=b21Rz9SsdQkCUqANwYpZejKhQ5HbU073uTIhzfvR"
    }

    url = "http://www.biguotk.com/admin/login/20186663312"
    res = requests.get(url,headers=headers)
    print(res.text)
    m = MultipartEncoder(fields=[('_token', 'fRQiJBkLt9Wri0LKmyp7hqaQB8XqhOzkmL71lBeL'),("exampaper_id",'1443')],
                         boundary='----WebKitFormBoundaryn6sq91D3XNAYKd9D')
    files = [('excel', ('2014年10月《中国近现代史纲要》真题.xlsx', 'xx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))]
    #with open(r"D:\workspace\project\pyqt\biguo2\wantiku\2014年10月《中国近现代史纲要》真题.xlsx",'rb') as f:
    #    con = f.read()

    #data = {'------WebKitFormBoundarysjHbIbuyVHS6H0x1 Content-Disposition: form-data; name="_token"':'fRQiJBkLt9Wri0LKmyp7hqaQB8XqhOzkmL71lBeL',
    #        '------WebKitFormBoundarysjHbIbuyVHS6H0x1 Content-Disposition: form-data; name="exampaper_id"':'1442',
    #        '------WebKitFormBoundarysjHbIbuyVHS6H0x1 Content-Disposition: form-data; name="excel"; filename="2014年10月《中国近现代史纲要》真题.xlsx" Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet	':con
    #        }

    res2 = requests.post('http://www.biguotk.com/admin/exam_real',data=m,headers=headers,)
    print(res2.text)

# req1()
# l = []
#
# for x in [1, 2, 3]:
#     d = {'num': 0, 'sqrt': 0}
#     d['num'] = x
#     d['sqrt'] = x*x
#     l.append(d)
#     print(l)
#     print(id(d))
# print(l)
#   http://www.biguotk.com/admin/exam_important?code=12656 押密
#   http://www.biguotk.com/admin/exams_vip/16402/edit?code=12656 vip题
#   http://www.biguotk.com/admin/exam/16402/edit?code=12656练习
#   http://www.biguotk.com/admin/exam_simu_paper?code=12656模拟             \u65b0\u589e\u8bd5\u5377\u6210\u529f
#1. http://www.biguotk.com/admin/exam_real_paper?code=12656  >添加试题post /admin/exam_real_paper para：year=2000&month=1&code=12656
#  http://www.biguotk.com/admin/exam_real?id=1440 》获取到已有试卷的id 年月
# /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]  试卷名称的xpath //table/tbody/tr/td[1]  GET
def req3():
    headers = {
        "X-CSRF-TOKEN": "fRQiJBkLt9Wri0LKmyp7hqaQB8XqhOzkmL71lBeL",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cookie": "XSRF-TOKEN=eyJpdiI6IlpZYTVsUlVTbE9Bc21IXC9wNHhFQWFRPT0iLCJ2YWx1ZSI6ImRpOUkrQUNiSW50aTR5WVpIQk5iUW1OUnZlbmkyZHZCTVVcL2VveTZZWlQzVFV6RjhTVUE3czRyYkhwTlI0Z1hTakNKdDJQT0hKS1BueTNJZk15RmxJZz09IiwibWFjIjoiMzFjZjdiZWMyNTBiMWJkNDg3YzhjZDlmYjFiODQ0MzdkOWY2YjQyZjg2OWQ5MjIzZThiNGYwYzg4OTRhNjBlNCJ9; laravel_session=b21Rz9SsdQkCUqANwYpZejKhQ5HbU073uTIhzfvR"
    }
    m = MultipartEncoder(
        fields=[('exampaper_id', '1441'),
                 ("excel",
                  ('1.xlsx',
                  open("D:\workspace\project\pyqt\\biguo2\wantiku\\1.xlsx", 'rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
                ],boundary='----WebKitFormBoundaryetr1Sq6VzYVCK9H5')
    headers1 = {
        #"X-CSRF-TOKEN": "vZjHj7mzQ2HSCZT43OowXBp6HaQodNmg6khkifjF",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Content-Type": "multipart/form-data;charset=UTF-8;boundary=----WebKitFormBoundaryetr1Sq6VzYVCK9H5",
        #"boundary":"----WebKitFormBoundaryetr1Sq6VzYVCK9H5",
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        #"Cookie":"XSRF-TOKEN=eyJpdiI6IndDbEVsem1ZeGgzZm53VE5qbUxydkE9PSIsInZhbHVlIjoiV05ta05KZDViN2hmTXpyZ1R0NzJBVWowK2ZLblk0ellibWhxTXVabTYzSTRXQmY5dGgreGdlNmZsNm04UlRTNEFSWGF6SVZ1VFNTdHVBXC9EUVhNa2x3PT0iLCJtYWMiOiI2YmM1YzkwZTE2YzA3NDlmMWQwYTM5MGJjZGQ0NGJkMzI4MTViNGZkNDNiMjFhNGMzZjFjMWVkNmJhOTQ4Zjc1In0%3D;laravel_session=fH8AD4X67jQM2XFMSEKzvoFgLez16hPd9geX4s11"
    }
    reqs = requests.Session()
    url = 'http://bg.dengming.pro/admin/exam_real'
    with open("D:\workspace\project\pyqt\\biguo2\wantiku\\1.xlsx",'rb') as f:
        con = f.read()
    #m = {'exampaper_id':'1441','excel':("1.xlxs",con)}
    #res_major = reqs.get('http://bg.dengming.pro/api/test',files=file,headers=headers1)
    res = reqs.post('http://bg.dengming.pro/api/test',data=m, headers=headers1)
    print(res.text)

def num2str(num):
    if len(num)<5:
        b = ""
        for a in range(5):
            if 5 - a > len(num):
                b = b + "0"
            else:
                return b + num
    else:
        return num

import csv,jieba
filename = "D:/workspace/project/pyqt/biguo2/courses.csv"
with open(filename) as f:
    reader = csv.reader(f)
    a = list(reader)
print(a)
# li = []
# for i,each in enumerate(a):
#     if i > 0 and len(each):
#         cut_ = jieba.cut(each[2])
#         a = each[2]
#         each[2] = [item for item in cut_ if len(item)>1]
#         each[2].append(a)
#         each[1] = num2str(str(each[1]))
#         li.append(each)
#     elif i == 0:
#         li.append(each)
#     else:
#         pass

import win32com.client as cl
import time

# xl = cl.Dispatch("Excel.Application")
# xl.Visible = -1
# xl.Workbooks.Open("D:\workspace\project\pyqt\\biguo2\wantiku\\1.xlsx")
# ms = xl.Worksheets(1)
# LastRow = ms.usedrange.rows.count
# print(LastRow)
# time.sleep(1)
# print(ms)
# time.sleep(1)
# xl.quit()


# with open(filename,'w',newline='') as f:
#     w = csv.writer(f)
#     w.writerows(li)

# b = [item[2:0:-1]for item in li]
# print(dict(b[1:]))
import re
s = "《薪酬管理》2017新大纲真题（四）"
s = re.sub('\d{2,4}(?!年)(?!月)|大纲|真题|模拟','',s)
s1 = "思想道德修养与法律基础"
out = [item for item in jieba.cut(s) if len(item)>1]
out1 = [i for i in jieba.cut(s1) if len(i) >1]
num = 0

def trans(id):
    print('haha')

print(a)
poli = []
poli1 = []
for b in a:
    if b[0] != "id":
        count = 0
        for i in out1:
            if i in eval(b[2]):
                count += 1
        if count >= 2*len(out1) // 3:
            num += 1
            print(a.index(b), b[1], 'wa')
            #if b[1] not in poli:
            if b[1] not in poli:
                poli.append(b[1])
                poli1.append(eval(b[2])[-1])
            print(num)
if len(poli)>1:
    print("识别出多个")
    for i,j in zip(poli,poli1):
        print(i,j)

elif len(poli) == 1:
    print(poli[0],poli1[0])

else:
    print('无法识别科目，请填写')