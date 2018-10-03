# coding:utf-8
import chardet
from exams_tools＿old import write_to_exel
import win32com
import subprocess
import re
import os
import shutil


def list_dir():
    path = os.getcwd()
    path1 = '/'.join(path.split('/')[0:-1])
    path2 = path1 + '/examsspider/moni0/doc/*.doc'
    obj = os.popen('ls %s' % path2)
    li = obj.readlines()
    return li


def big_title(big, num, conlist):
    if "单项选择" in big:
        cls = 1
        return split_small(big, cls,num,conlist)
    elif "多项选择" in big:
        cls = 2
        return split_small(big, cls,num,conlist)
    elif "判断题" in big:
        cls = 3
        return split_small(big, cls,num,conlist)
    else:
        cls = 4

        return split_small(big, cls,num,conlist)


def split_small(big, cls, num, conlist):
    # 大题分割成多个小题
    if cls != 4:
        p = re.compile("第\d*?题\.|第\d*?题")
        li = p.split(big)
    else:
        p = re.compile("第\d*?题\.|第\d*?题")
        li = p.split(big)

    for small in li[1:]:
        p1 = re.compile("共\d+?分")
        if len(p1.findall(small)):
            continue
        if not len(small):
            continue
        res_li = split_pieces(small, cls, num)
        conlist.append(res_li)
        num += 1

    return num, conlist


def split_pieces(small,cls,num):
    # 题干答案分割
    p = re.compile("【正确答案】答案|【正确答案】答:|【正确答案】|【答案】|【参考答案】|答：|【解析】|答案：|答案")
    ques = p.split(small)[0]
    emp_li = empty_li()
    if len(p.split(small)) > 1:
        ans = p.split(small)[1]
        emp_li[9] = ans
    if len(p.split(small)) > 2:
        anas = p.split(small)[2]
        emp_li[10] = anas

    emp_li[0] = num

    if cls == 1:

        emp_li[1] = 1
        li = deal_option(ques)
        for i in range(len(li)):
            emp_li[i + 2] = li[i]

    elif cls == 2:
        emp_li[1] = 2
        li = deal_option(ques)
        for i in range(len(li)):
            emp_li[i + 2] = li[i]

    elif cls == 3:
        emp_li[1] = 3
        emp_li[2] = ques

    elif cls == 4:
        emp_li[1] = 4
        emp_li[2] = ques
    return emp_li


def deal_option(ques):
    # 选择题 选项处理
    p = re.compile("A\.|B\.|C\.|D\.|E\.|F\.|A、|B、|C、|D、|E、|F、|A．|B．|C．|D．|E．|F．")
    p1 = re.compile("[ABCDEF]")
    li = p.split(ques)
    li = [x for x in li if len(x)]

    return li


def empty_li():
    array = ['' for i in range(11)]
    return array


### word 文档 *****处理
def doc2text(x):
    # fname + .doc
    p = re.compile("\.doc|\.pdf")
    path,docname = os.path.split(x)

    fname = p.sub('',docname)
    print(fname)
    if docname.endswith('.doc'):
        output = subprocess.check_output(["antiword",x])
        return output, fname
    elif docname.endswith('.pdf'):
        output = pdf_2_text(x)
        return output, fname
    # print(output)


### PDF 文档 *******处理
def pdf_2_text(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()

    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    with open(path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, ):
            interpreter.process_page(page)
        text = retstr.getvalue()

        text = re.sub('',"^",text)
        text = re.sub(' ','^',text)
        text = re.sub('\^\^','_',text)
        text = re.sub("\n","&",text)
        print(text)
        text = re.sub('本题&?分数\^?&?\d+?\^?&?分','',text) #本题分数^1^&分 本题&分数^&6^分&

        li = re.findall('&\d+\.\d+&|&\d+?&',text)
        for x in li:
            text = re.sub(x,'*'+x[1:-1]+'*',text)
        text = re.sub("\s","",text)
        text = re.sub('&一、|&二、|&三、|&四、|&五、|&六、|&七、|&八、|&九、|&一[\^|\_]|&二[\^|\_]|&三[\^|\_]|&四[\^|\_]|&五[\^|\_]|&六[\^|\_]|&七[\^|\_]|&八[\^|\_]|&九[\^|\_]',"&&&第一题",text)
        text = re.sub("&\d+?\^|&\d+?\.|&\d+?．","&&&第1题",text)
        p = re.compile('\^?【www.Stegs.net\^?Www.GSKS.cc】\^?QQ\^?交流群:35167222\^?各类考试\^?历年试题答案免费直接\^?下载&?|教材购买：\^?http://www\.stegs\.net/so\.html&?|【独家提供QQ905363546】|http:\/\/zikao5\.com|我自考网|自考题库购买：http:\/\/www\.zikao5.com\/tiku\/index\.html|【独家提供】|QQ 交流群:35167222|支持网站持续免费提供试题，收藏本网各分站网址请到【Www\.BCER\.com\.cn】。。谢谢！|支持网站持续免费提供试题，收藏本网各分站网址请到【Www\.BCER\.com\.cn】。新浪微博：熊猫仁在|甘肃考试\|自考网|【www.Stegs.net Www.GSKS.cc】|各类考试 历年试题答案免费直接 下载|支持网站持续免费提供试题，收藏本网各分站网址请到【Www.BCER.com.cn】。新浪微博：熊猫仁在|^第.+?页.*?（?共.+?页）?|\xc2\a0|你的得分|修改分数|\^')
        text = p.sub('', text)
        text = re.sub("\)页.*?共\(.*?页.*?&",'',text) #)页5共(页2第^题试流物代现与务商子电^#51900浙& &)页5共(页5第^题试流物代现与务商子电^#51900浙&^
        # text = re.sub("&\^","",text)
        # text = re.sub("&", "", text)
        text = re.sub("&&&","\n",text)
        text = re.sub("&", "", text)
        text = re.sub("修改分数|你的得分|【你的答案】",'',text)
        # text = re.sub("\^"," ",text)
        print(text)
        print("*"*50)

    device.close()
    retstr.close()

    return text


def handle_doc(text):
    # 用第1题替换小题号
    p0 = re.compile("\\n\d+\.|\\n\d+、|\\n\d+．")
    text = p0.sub('第1题',text)
    # 去除试卷的空格图片等多余的格式文本
    p = re.compile("你的得分.*?\[pic\]|\||\xc2\xa0|\\t|\\v")
    text1 = p.sub("", text)
    # print(text1)
    if text1.count("[pic]") > 1:
        raise Exception("图片文档，暂不处理")

    # 对文本第二次去除文本
    p1 = re.compile("【你的答案】|本题.*?\d+?分|你的得分|分数|www.zikao5.com|www.zikao5.cn|http://|我自考网整理|zikao5.com|zikao5.cn|我自考网|【QQ.*?】|\[pic\]")
    text2 = p1.sub("",text1)
    # print(text1)

    # 对文本按照大题进行分段
    p2 = re.compile("一、|二、|三、|四、|五、|六、|七、|八、|九、")
    li = p2.split(text2) # 用了split后注意 列表是否有空元素
    print(str(li).decode("unicode-escape").encode("iso-8859-1").encode('utf-8'))
    return li


def get_array(li):
    # 提取试卷名,答案数组
    con_list = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]
    str1 = li[0]
    p3 = re.compile("\d*年.*?试题|\d*年.*?试卷|\d*年.*?密卷|\d*年.*?模拟")
    fname = len(p3.findall(str1)) and p3.findall(str1)[0]
    print(fname)
    num = 1
    for big in li[1:]:
        num,con_list = big_title(big,num,con_list)
    return fname, con_list


def trans():
    # 程序入口
    file_li = ["01.docx"]# list_dir()
    for x in file_li:
        x = x.strip()
        try:
            text, fname0 = doc2text(x)
            if "英语" in text:
                raise Exception('暂不处理英语')
            li = handle_doc(text)
            if len(li):
                fname, array = get_array(li)
                if not fname:
                    print(">>>Here!!")
                    fname = fname0
                for li in array:
                    print(str(li).decode("unicode-escape").encode("iso-8859-1").encode('utf-8'))
                write_to_exel.write_xlsx(fname, array)
        except Exception as e:
            print(e)
            pathx = '/home/cxdp/Desktop/undo/'
            if not os.path.exists(pathx):
                os.mkdir(pathx)
            shutil.copy(x, '/home/cxdp/Desktop/undo/')

if __name__ == '__main__':
    trans()
