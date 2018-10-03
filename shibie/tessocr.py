from PIL import Image,ImageDraw
from pytesseract import pytesseract as pt
import os
cwd = os.getcwd()

def clearnoise2(im, G, N, Z):
    '''
    去噪算法
    :param im: im object
    :param G:  阈值
    :param N:  邻域噪点的数量，小于但不等于N的数量的噪点
    :param Z:  降噪次数
    :return:
    '''
    draw = ImageDraw.Draw(im)

    for i in range(0,Z):
        for x in range(1, im.size[0] - 1):
            for y in range(1, im.size[1] - 1):
                color = getPixel(im, x, y, G, N)

                if color != None:
                    draw.point((x,y),color)


def getPixel(image,x,y,G,N):
    '''
    获取像素
    :param image: image object
    :param x: axis x
    :param y: axis y
    :param G: 阈值
    :param N:
    :param mode: 模式1为 取下邻点的值，2为自己
    :return:
    '''
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False
    nearDots = 0
    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1
    if nearDots < N:
        return image.getpixel((x-1,y-1))
    else:
        return None


def clearnoise(imarr,size,N):
    '''
    # 去噪算法2：
    :param imarr: 图片数组
    :param size: 图片大小
    :param N: 噪点数量
    :return:
    '''
    for i in range(size[0]-2):
        for j in range(size[1]-2):
            num = 0
            if imarr[i+2,j+2] == 0:
                num += 1
            if imarr[i+1,j+2] == 0:
                num += 1
            if imarr[i,j+2] == 0:
                num += 1
            if imarr[i,j+1] == 0:
                num += 1
            if imarr[i+2,j+1] == 0:
                num += 1
            if imarr[i+2,j] == 0:
                num += 1
            if imarr[i+1,j] == 0:
                num += 1
            if imarr[i,j] == 0:
                num += 1
            if num > N:
                pass
            else:
                imarr[i+1,j+1] = 255
            if imarr[i,j+1] == 255 and imarr[i+2,j+1] ==255:
                imarr[i + 1, j + 1] = 255


def recogit(imgobject=None):
    '''
    # 程序入口，识别模块
    :param imgobject: 图片对象
    :return: nearest:最可能的值，result :  [48, '4', '4_0.txt', 48, '4', '4_0.txt']
    '''
    if not imgobject:
        im = Image.open('D:/workspace/captcha/40.png')
    else:
        im = imgobject
    im = im.convert("L")
    size = im.size
    img_array = im.load()
    for i in range(size[0]):
        for j in range(size[1]):
            if i != 0 and j != 0 and i != 44 and j != 59:  # 把边界变为纯白
                if(img_array[i,j] >250):
                    # print('像素点：%d,%d,%d'%(i,j,img_array[i,j]))
                    img_array[i,j] = 255
                else:
                    img_array[i,j] = 0
            else:
                img_array[i,j] = 255

    # 去除噪点
    clearnoise(img_array,size,3)
    clearnoise(img_array, size,3)
    clearnoise(img_array, size, 3)
    clearnoise2(im, 140, 3, 1)
    clearnoise(img_array, size,3)

    s = pt.image_to_string(im, lang="dt", config="-psm 7")
    return s


if __name__ == '__main__':
    p = "D:/workspace/captcha"
    li = os.listdir(p)
    for i in li:
        im = Image.open(p+"/"+i)
        s = recogit(im)
        print(i,s)
