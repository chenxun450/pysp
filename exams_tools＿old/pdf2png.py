# coding:utf-8
import PyPDF2
import PythonMagick
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ManImage:
    """
    Manipulate Image Object
    """

    def __init__(self, i_file, o_dire):
        """
        init args
        :param i_file: (str) input pdf file (eg: "/home/file.pdf")
        :param o_dire: (str) output image directory (eg: "/home/")
        """
        self.i_file = i_file
        self.o_dire = o_dire

    def __str__(self):
        traceback = "Executing under {0.argv[0]} of {1.i_file} into {2.o_dire}......".format(sys, self, self)
        return traceback

    def playpdf(self, ds):
        """
        split pdf file
        :param ds: (int) set ds = 1024 ~= 1MB output under my test
        :return: splited PNG image file
        """
        pdf = PyPDF2.PdfFileReader(file(self.i_file, "rb"))

        pages = pdf.getNumPages()
        print('Totally get ***{0:^4}*** pages from "{1.i_file}", playpdf start......'.format(pages, self))
        try:
            for i in range(pages):
                image = PythonMagick.Image()

                image.density(str(ds)) # 设置 文件大小
                image.read(self.i_file + '[' + str(i) + ']')
                image.magick("PNG")
                image.write(self.o_dire + str(i + 1) + ".png")
                print("{0:>5}     page OK......".format(i + 1))
        except Exception as e:
            print(str(e))
