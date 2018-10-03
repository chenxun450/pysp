#coding:utf-8
import os,re,time
import xlwt,xlrd
from xlutils.copy import copy as cp
from write_to_exel import write_xlsx as wte

def rename0(path):
    fi = os.listdir(path)
    files = []
    p = re.compile(r"<>")
    for i in fi:
        if "xlsx" in i:
            files.append(i)
    for f in files:
        d = p.sub("",f)
        os.renames(f,d)

def emparray():
    a = []
    for i in range(11):
        a.append("")
    return a

def read2sheet(pat):
    workbook = xlrd.open_workbook(pat)
    sheet = workbook.sheet_by_index(0)
    wb = cp(workbook)
    ws = wb.get_sheet(0)

    for i,_ in enumerate(sheet.get_rows()):
        if "模考" in sheet.cell_value(i,9):
            ws.write(i,9,"")
    return wb

def mod(path):
    # todo ('C:\\Users\\HIAPAD\\Desktop\\todo\\学前教育原理\\已传', [], ['1504-全国-学前教育原理.xlsx', '1510-全国-学前教育原理.xlsx'])
    gen = os.walk(path)
    for p,_,fnames in gen:
        for fname in fnames:
            pat = p + "/" + fname
            print(pat)
            wb = read2sheet(pat)
            wb.save(pat)

if __name__ == '__main__':
    path = input("请输入路径：")
    print(path)
    mod(path)