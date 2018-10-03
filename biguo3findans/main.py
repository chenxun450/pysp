# coding:utf-8
import os,time,re
import xlrd,xlwt
from xlutils.copy import copy as cp


def get_excels(path):
    gen = os.walk(path)
    li = []
    for p, _, fnames in gen:
        for fname in fnames:
            pat = p + "/" + fname
            li.append((p+"/",fname))
    return li

def get_ans(title,option):
    '''

    :param title:
    :param option:
    :return:
    '''
def from_shangxueba():
    #todo http://zhannei.baidu.com/cse/search?q=...&s=7601079239767839919&nsid=1
    pass

def from_wendaku():
    #todo
    pass

def from_ppkao():
    # todo
    pass

def from_baidu():
    # mofangge.com   www.gaodun.com
    pass

def read2sheet(fpath):
    workbook = xlrd.open_workbook(fpath)
    sheet = workbook.sheet_by_index(0)
    wb = cp(workbook)
    ws = wb.get_sheet(0)

    for i,_ in enumerate(sheet.get_rows()):
        if not sheet.cell_value(i,9):
            print("值为：",sheet.cell_value(i,9))
            num = sheet.cell_value(i,0)
            cls = sheet.cell_value(i,1)
            title = sheet.cell_value(i,2)
            option1 = sheet.cell_value(i,3)
            ansis = sheet.cell_value(i,10)
            
            # 获取该题的答案！！

            print("正在给",num,".",title,"查找答案")
            ws.write(i,9,"")

    wb.save(fpath)

def search_work():
    '''
    主线工作
    mod1:获取目录下所有excel文件
    mod2:对文件进行读取
    mod3:数据处理 获取需要填写答案的题目  返回标记的内容和行列号
    mod4:根据题目查找答案
    mod5:写入excel
    :return:
    '''
    path = input("请输入路径：")
    xlsxs = get_excels(path)
    for pat,fname in xlsxs:
        fpath = pat + fname
        read2sheet(fpath)


if __name__ == '__main__':
    search_work()
