# coding:utf-8
from exams_tools＿old import write_to_exel
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter,HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import subprocess
import re
import sys
import os
import shutil



def list_dir():
    path = os.getcwd()
    path1 = '/'.join(path.split('/')[0:-1])
    path2 = path1 + '/examsspider/moni0/pdf/*.pdf'
    obj = os.popen('ls %s' % path2)
    li = obj.readlines()
    return li


def big_title(big, num, conlist):
    if "单项选择" in big or "单选题" in big:
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
        p = re.compile("第\d*?.{0,4}题\.|第\d*?.{0,4}题")
        li = p.split(big)
    else:
        p = re.compile("第\d*?.{0,4}题\.|第\d*?.{0,4}题")
        li = p.split(big)

    for small in li[1:]:
        p1 = re.compile("共\d+?分")
        if len(p1.findall(small)):
            print(11111, str(p1.findall(small)).decode("unicode-escape").encode("iso-8859-1"))
            continue
        if not len(small):
            print(22222, len(small))
            continue
        res_li = split_pieces(small, cls, num)
        if not res_li:
            print(33334, res_li)
            continue
        conlist.append(res_li)
        num += 1
    return num, conlist


def split_pieces(small,cls,num):
    # 题干答案分割
    p = re.compile("【正确答案】答案|【正确答案】答:|【正确答案】|【答案】|【参考答案】|答：|【解析】|答案：|答案|\[解析\]|［解析］")
    ques = p.split(small)[0]
    emp_li = empty_li()
    if len(p.split(small)) == 2:
        ans = p.split(small)[1]
        emp_li[9] = ans.strip().strip("_").strip()
    elif len(p.split(small)) > 2:
        ans = p.split(small)[1] or p.split(small)[2]
        anas = p.split(small)[2]
        emp_li[9] = ans.strip().strip("_").strip()
        emp_li[10] = anas.strip().strip("_").strip()

    emp_li[0] = num

    if cls == 1:

        emp_li[1] = 1
        li = deal_option(ques)
        for i in range(len(li)):
            emp_li[i + 2] = li[i].strip().strip("_").strip()

    elif cls == 2:
        emp_li[1] = 2
        li = deal_option(ques)

        for i in range(len(li)):
            emp_li[i + 2] = li[i].strip().strip("_").strip()

    elif cls == 3:
        emp_li[1] = 3
        emp_li[2] = ques.strip().strip("_").strip()

    elif cls == 4:
        emp_li[1] = 4
        emp_li[2] = ques.strip().strip("_").strip()
    if not emp_li[2]:
        return None
    return emp_li


def deal_option(ques):
    # 选择题 选项处理
    p = re.compile("A\.|B\.|C\.|D\.|E\.|F\.|A、|B、|C、|D、|E、|F、|A．|B．|C．|D．|E．|F．")
    p1 = re.compile("A|B|C|D|E|F")
    li = p.split(ques)
    if len(li)<5:
        li = p1.split(ques)
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
        text = pdf2text(x)
        output = pdftext_first(text)
        return output, fname
    else:
        raise Exception("**What???**")
    # print(output)


### PDF 文档 *******处理
def pdf2text(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()

    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    with open(path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, ):
            interpreter.process_page(page)
        text = retstr.getvalue()
    device.close()
    retstr.close()
    return text

def pdftext_first(text):

    text = re.sub('',"^",text)
    text = re.sub(' ','^',text)
    text = re.sub('\^\^\^\^','_',text)
    text = re.sub("\n","&",text)

    text = re.sub("&8、\^", '', text)  # 去掉文本中的多余的特殊题号

    cls_num = 1 # 默认试卷类型
    text = re.sub('本题[&^]{0,4}分数[/^&]{0,4}\d+?[/^&]{0,4}分|【\^?独家提供\^?QQ905363546】\^?！', '', text) #本题分数^1^&分 本题&分数^&6^分&
    li0 = re.findall('&\d+?\^[天,个]', text)
    for x in li0:
        text = re.sub(x, '*' + x[1:], text)
    li = re.findall('&\d+\.\d+&|&\d+?&',text)
    for x in li:
        text = re.sub(x,'*'+x[1:-1]+'*',text)
    text = re.sub("\s","",text)
    p0 = re.compile('&.{0,30}?答案&')
    li1 = p0.findall(text)
    # print(str(li1).decode("unicode-escape").encode("iso-8859-1"))
    if len(li1):
        text = re.sub(li1[-1],"|答案|"+li1[-1][1:-1],text)
        cls_num = 2

    text = re.sub('&一、|&二、|&三、|&四、|&五、|&六、|&七、|&八、|&九、|&一[/^_]|&二[/^_]|&三[/^_]|&四[/^\_]|&五[/^\_]|&六[/^\_]|&七[/^\_]|&八[/^\_]|&九[/^\_]',"&a&第一题",text)
    for x in re.findall("&\d+?、",text):
        text = re.sub(x,"第"+x[1:-3]+"题",text)
    # text = re.sub("&\d{1,2}\^|&\d+?\.|&\d+?．|&\d{1,2}、","&a&第"+\d+"题",text)
    l = re.findall("&\d{1,2}\^|&\d+?\.|&\d+?．",text)
    for x in l:
        text = re.sub(x,'第'+x[1:]+"题",text)

    p = re.compile('\^?【www.Stegs.net\^?Www.GSKS.cc】\^?QQ\^?交流群:35167222\^?各类考试\^?历年试题答案免费直接\^?下载&?|教材购买：\^?http://www\.stegs\.net/so\.html&?|【独家提供QQ905363546】|http:\/\/zikao5\.com|我自考网|自考题库购买：http:\/\/www\.zikao5.com\/tiku\/index\.html|【独家提供】|QQ 交流群:35167222|支持网站持续免费提供试题，收藏本网各分站网址请到【Www\.BCER\.com\.cn】。。谢谢！|支持网站持续免费提供试题，收藏本网各分站网址请到【Www\.BCER\.com\.cn】。新浪微博：熊猫仁在|甘肃考试\|自考网|【www.Stegs.net Www.GSKS.cc】|各类考试 历年试题答案免费直接 下载|支持网站持续免费提供试题，收藏本网各分站网址请到【Www.BCER.com.cn】。新浪微博：熊猫仁在|^第.+?页.*?（?共.+?页）?|\xc2\a0|你的得分|修改分数|\^')
    text = p.sub('', text)
    text = re.sub("\)页.*?共\(.*?页.*?&",'', text) #)页5共(页2第^题试流物代现与务商子电^#51900浙& &)页5共(页5第^题试流物代现与务商子电^#51900浙&
    # text = re.sub("&\^","",text)
    # text = re.sub("&", "", text)
    text = re.sub("&a&","\n",text)
    text = re.sub("&", "", text)
    text = re.sub("修改分数|你的得分|【你的答案】|【独家提供QQ905363546】|我自考网|【独家提供】|http://zikao5.com|第\d{1,2}页|共\d{1,2}页|\(P?\d*\)",'',text)
    # text = re.sub("\^"," ",text)

    if cls_num == 2:
        para = text.split("|答案|")
        astr = para[0]
        bstr = para[1]
        for x in re.findall('第一题|第\d+?题|第\d+?、题|第\d+?题\.|第\d+?．题',astr):
            astr= re.sub(x,"&a&"+x[0:-3]+"^题", astr)
        li2 = re.findall("第\d+?题|第\d+?、题|第\d+?题\.|第\d+?．题", bstr)
        for x in li2:
            bstr = re.sub(x,'&a&' + x[0:-3]+'^题【答案】', bstr)
        li3 = astr.split('&a&')
        print(str(li3).decode("unicode-escape").encode("iso-8859-1"))

        # 对单选，多选答案排序
        bstr = re.sub('第一题','&b&第一题',bstr)
        li4 = re.split('&b&',bstr)
        print(str(li4).decode("unicode-escape").encode("iso-8859-1"))
        li6 = []
        for x in li4:
            if "单项选择" in x or "单选题" in x:
                print(x)
                x = x.split('&a&')[0] + ''.join(sorted(x.split('&a&')[1:], key=sort_it))
                li6.append(x)
            elif "多项选择" in x:
                x = x.split('&a&')[0] + ''.join(sorted(x.split('&a&')[1:], key=sort_it))
                li6.append(x)
            li6.append(x)
        bstr = ''.join(li6)
        li7 = re.split('第.{0,9}题',bstr)
        li5 = []
        for x in zip(li3,li7):
            li5.append(''.join(list(x)))
        text = ''.join(li5)
    print(text)
    print("*" * 50)
    return text

# 排序函数
def sort_it(x):
    x = re.findall('第\d+',x)[0][3:]
    return int(x)



def handle_doc(text):
    # 用第1题替换小题号
    p0 = re.compile("\\n\d+\.|\\n\d+、|\\n\d+．")
    text = p0.sub('第1题',text)
    # 去除试卷的空格图片等多余的格式文本
    p = re.compile("你的得分.*?\[pic\]|\||\xc2\xa0|\\t|\\v|\(P\d+\~P?\d+\)")
    text1 = p.sub("", text)
    print(text1)
    if text1.count("[pic]") > 1:
        raise Exception("图片文档，暂不处理")

    # 对文本第二次去除文本
    p1 = re.compile("【你的答案】|本题.*?\d+?分|你的得分|分数|www.zikao5.com|www.zikao5.cn|http://|我自考网整理|zikao5.com|zikao5.cn|我自考网|【QQ.*?】|\[pic\]|【独家提供QQ905363546】")
    text2 = p1.sub("",text1)
    # print(text1)

    # 对文本按照大题进行分段
    p2 = re.compile("第一\^?题|一、|二、|三、|四、|五、|六、|七、|八、|九、")
    li = p2.split(text2) # 用了split后注意 列表是否有空元素
    print(str(li).decode("unicode-escape").encode("iso-8859-1").encode('utf-8'))
    return li


def get_array(li):
    # 提取试卷名,答案数组
    con_list = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]
    str1 = li[0]
    p3 = re.compile("\d*年.*?试题|\d*年.*?试卷|\d*年.*?密卷|\d*年.*?模拟")
    fname = len(p3.findall(str1)) and p3.findall(str1)[0]
    # fname 为试题名
    if "数" in fname or '物理' in fname or "英语" in fname or "力学" in fname or "外语" in fname or "日语" in fname or "语言学" in fname:
        raise Exception('暂不处理数学，物理，英语')
    print(fname)

    num = 1
    for big in li[1:]:
        num,con_list = big_title(big,num,con_list)
    print(str(con_list).decode("unicode-escape").encode("iso-8859-1"))
    return fname, con_list


def main():
    # 程序入口
    file_li = list_dir()
    for x in file_li:
        x = x.strip()
        try:
            text, fname0 = doc2text(x)  #fname0 为文件名
            if "数" in fname0 or '物理' in fname0 or "英语" in fname0 or "力学" in fname0 or "外语" in fname0 or "日语" in fname0 or "语言学" in fname0:
                raise Exception('暂不处理数学，物理，英语')
            li = handle_doc(text)
            if len(li):
                fname, array = get_array(li)
                if not fname:
                    print(">>>Here!!")
                    fname = fname0
                #for li in array:
                #    print(str(li).decode("unicode-escape").encode("iso-8859-1").encode('utf-8'))
                write_to_exel.write_xlsx(fname, array)
        except Exception as e:
            print(e)
            pathx = '/home/cxdp/Desktop/undo/'
            if not os.path.exists(pathx):
                os.mkdir(pathx)
            shutil.copy(x, '/home/cxdp/Desktop/undo/')

if __name__ == '__main__':
    main()