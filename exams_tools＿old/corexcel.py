# coding:utf-8
import os,re
import xlrd
import write_to_exel as wte
from tkinter import filedialog

path = "D:/"
def exceldone(path):
    li = os.listdir(path)

    for paper in li:
        filename = path + '/' +paper
        data = xlrd.open_workbook(filename).sheets()[0]

        for li in data._cell_values:        # 更正第9列的错误
            li[9] = re.sub('\,','',li[9])
        array = data._cell_values
        path1 = r"C:\Users\HIAPAD\Desktop\shangtiku0612"
        if not os.path.exists(path1):
            os.makedirs(path1)
        wte.write_xlsx(path1,paper,array)

if __name__ == '__main__':
    path = filedialog.askdirectory(initialdir=r"C:\Users\HIAPAD\Desktop")
    if path:
        exceldone(path)