# coding:utf-8
import copy
from PIL import Image,ImageEnhance

im = Image.open('d:/workspace/captcha/0.png')
im = im.convert('RGB')
im4 = Image.open('d:/1.gif')

class ImageSequence:
    def __init__(self, im):
        self.im = im
    def __getitem__(self, ix):
        try:
            if ix:
                self.im.seek(ix)
            return self.im
        except EOFError:
            raise IndexError # end of sequence

imS = ImageSequence(im4)


from PIL import ImageDraw,ImageFont
from pytesseract import pytesseract as pt

path = "D:\workspace\captcha\\"
img = Image.open(path+"34.png")
img = img.convert("L")
s = pt.image_to_string(img,lang="dt",config="-psm 7")
print(s)
# 1、合并图片
# 2、生成box文件
# tesseract dty.dt.exp0.tif dty.dt.exp0 -l eng -psm 7 batch.nochop makebox
# 3、修改box文件
# 4、生成font_properties
# echo dt 0 0 0 0 0 >font_properties
# 5、生成训练文件
# tesseract dty.dt.exp0.tif dty.dt.exp0 -l eng -psm 7 nobatch box.train
# 6、生成字符集文件
# unicharset_extractor dty.dt.exp0.box
# 7、生成shape文件
# shapeclustering -F font_properties -U unicharset -O dty.unicharset dty.dt.exp0.tr
# 8、生成聚集字符特征文件
# mftraining -F font_properties -U unicharset -O dty.unicharset dty.dt.exp0.tr
# 9、生成字符正常化特征文件
# cntraining dty.dt.exp0.tr
# 10、更名
# rename normproto dt.normproto
# rename inttemp dt.inttemp
# rename pffmtable dt.pffmtable
# rename unicharset dt.unicharset
# rename shapetable dt.shapetable
# 11、合并训练文件，生成dt.traineddata
# combine_tessdata dt.