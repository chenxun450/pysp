# -*- coding:utf-8 -*-
import xlrd
import xlwt
import os

# excel字体设置
style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'Tahoma'
font.bold = False
font.italic = False
font.underline = False
style.font = font


def write_xlsx(fpath,fname, con_list): # 参数：('C:\work/',"2010年10月真题",conlist)
    #print os.getcwd()
    if not os.path.exists(fpath):   # fname 为没有后缀名的
        os.mkdir(fpath)
    # print type(fname),fname
    if not fpath.endswith("/"):  # 让fpath 是否带/都可以通过
        fpath = fpath + "/"
    filename = fname + '.xlsx'
    path = os.path.join(fpath, filename)

    if not os.path.exists(path):
        try:
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
            for i in range(len(con_list)):
                for j in range(0,11):
                    worksheet.write(i,j,con_list[i][j])

            workbook.save(path)
            print('写入<%s>excel完毕!'%fname)
        except Exception as e:
            print(e)
        finally:
            pass
    else:
        print('<%s>文件已存在'%fname)


if __name__ == '__main__':
    # examples:
    con_list = [['序号','类型','问题','选项A','选项B','选项C','选项D','选项E','选项F','正确答案','解释']]
    name = 'n'
    write_xlsx("D:\\excel\\",name,con_list)