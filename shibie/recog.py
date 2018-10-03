from PIL import Image,ImageDraw
import os
cwd = os.getcwd()

# 加载字库模块
def load():
    path0 = cwd + "/字库"
    path1 = cwd + "/竖形字库"
    charli0 = os.listdir(path0)
    charli1 = os.listdir(path1)
    print(charli0,charli1)
    dli0 = {}   #  字库中的字符集
    dli1 = {}   # 竖形字库中的字符集
    for eachfile in charli0:
        with open(path0 + "/" + eachfile, 'r') as b:
            str0 = b.read()
            key,_ = eachfile.split("_")
            if key not in dli0.keys():
                dli0[key] = [str0,]
            else:
                dli0[key] = dli0[key] + [str0,]
    for eachfile in charli1:
        with open(path1 + "/" + eachfile, 'r') as b:
            str1 = b.read()
            key, _ = eachfile.split("_")
            if key not in dli1.keys():
                dli1[key] = [str1, ]
            else:
                dli1[key] = dli1[key] + [str1, ]
    return dli0,dli1

def recognize0(way,result,codeli,strli):
    if way == 'H':
        print("识别中···")
    else:
        print("\n识别中···")
    count = 10000
    Mach = ''
    name = ''
    for k,way,codestr1 in codeli:
        for key,vli in strli.items():
            for i,v in enumerate(vli):
                pacenum = editdistance(codestr1,v)  # （识别的特征，字库的特征）
                if count > pacenum:  # 匹配度
                    count = pacenum
                    Mach = key
                    name = key+"_"+str(i)+ ".txt"
        result.append(count)
        result.append(Mach)
        result.append(name)
        print("可能为：",Mach, end='')
        count = 10000

def editdistance(str1, str2):  # args（识别的特征，字库的特征）
    lenth1 = len(str1)
    lenth2 = len(str2)
    Array = [[0] * lenth2 for i in range(lenth1)]
    for i in range(lenth1):
        for j in range(lenth2):
            if str1[i] == str2[j]:
                if i == 0 and j == 0:
                    Array[i][j] = 0
                elif i != 0 and j == 0:
                    Array[i][j] = Array[i - 1][j]
                elif i == 0 and j != 0:
                    Array[i][j] = Array[i][j - 1]
                else:
                    Array[i][j] = Array[i - 1][j - 1]
            else:
                if i == 0 and j == 0:
                    Array[i][j] = 1
                elif i != 0 and j == 0:
                    Array[i][j] = Array[i - 1][j] + 1
                elif i == 0 and j != 0:
                    Array[i][j] = Array[i][j - 1] + 1
                else:
                    Array[i][j] = min(Array[i][j - 1], Array[i - 1][j], Array[i - 1][j - 1]) + 1

    current = max(Array[lenth1 - 1][lenth2 - 1], abs(lenth2 - lenth1))
    return current

# 保存图片的特征值
def savepicode(im, crop_list, way,fname):
    for k,blockimg in enumerate(crop_list):
        Crop_img = im.crop(blockimg)
        size = Crop_img.size
        crop_imload = Crop_img.load()
        Crop_img.show()
        s = "_0"
        if "_" not in fname:
            code = fname[:-4] + s + '.txt'
            c = fname[:-4]
        else:
            c,_ = fname.split("_")
            code = c + s + ".txt"
        if way == "H":
            path0 = "./"+"字库/"+code
        else:
            path0 = "./"+"竖形字库/"+code
        i = 0
        while 1:
            if os.path.exists(path0):
                path0 = "./"+"字库/" + c +"_"+ str(i) + ".txt"
            else:
                break
        codestr = '' # 验证码特征值
        if way == "H":
            for i in range(size[0]):
                for j in range(size[1]):
                    if crop_imload[i, j] > 0:
                        codestr = codestr + "1"
                    else:
                        codestr = codestr + '0'
            with open(path0,'a') as f:
                f.write(codestr)
        else:
            for j in range(size[1]):
                for i in range(size[0]):
                    if crop_imload[i, j] > 0:
                        codestr = codestr + "1"
                    else:
                        codestr = codestr + '0'
            with open(path0,'a') as f:
                f.write(codestr)

def getpicode(im, crop_list, way):
    codeli = []
    for k,blockimg in enumerate(crop_list):
        Crop_img = im.crop(blockimg)
        size = Crop_img.size
        Crop_img.show()
        crop_imload = Crop_img.load()
        codestr = ''
        if way == "H":
            Name = "H"
            for i in range(size[0]):
                for j in range(size[1]):
                    if crop_imload[i,j]>0:
                        codestr = codestr + "1"
                    else:
                        codestr = codestr + '0'
        else:
            Name = 'N'
            for j in range(size[1]):
                for i in range(size[0]):
                    if crop_imload[i, j] > 0:
                        codestr = codestr + "1"
                    else:
                        codestr = codestr + '0'
        codeli.append((k,way,codestr))
    return codeli

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


def _save2code(path = r'C:\Users\HIAPAD\Pictures\ico',fname = "2_2.png"):
    '''
    # 手动录入字库模块
    :param path: 文件夹路径，尾部不带斜杠
    :param fname: 文件名 不带路径
    :return: 无返
    '''
    im = Image.open(path + "/" + fname)
    im = im.convert("L")
    size = im.size
    img_array = im.load()
    for i in range(size[0]):
        for j in range(size[1]):
            if i != 0 and j != 0 and i != 44 and j != 59:  # 把边界变为纯白
                if (img_array[i, j] > 250):
                    # print('像素点：%d,%d,%d'%(i,j,img_array[i,j]))
                    img_array[i, j] = 255
                else:
                    img_array[i, j] = 0
            else:
                img_array[i, j] = 255
    cropli = imagecrop(img_array)
    savepicode(im, cropli, "H",fname)
    savepicode(im, cropli, "N",fname)

def imagecrop(img_array):
    '''
    # ↓↓ 自定义切割图片处
    :param img_array: im.load()的返回值
    :return: 返回切割box (left,top,right,down)
    '''
    right = "c"
    for i in range(45):
        for j in range(60):
            if img_array[44-i,j] == 0:
                # 右边界值
                right = 44-i
                break
        if right != "c":
            break
    topp = "c"
    for j in range(60):
        for i in range(45):
            if img_array[i,j] == 0:
                # 上边界值
                topp = j
                break
        if topp != "c":
            break
    cropli = []
    if topp+30 < 59 and right-24 > 0:
        cropli.append((right-20,topp,right+1,topp+27))
    else:
        print("注意：切割的图片有问题")
    # ↑↑ 切割图片
    return cropli

# 加载字库
dliH,dliN = load()

def recogit(imgobject=None):
    '''
    # 程序入口，识别模块
    :param imgobject: 图片对象
    :return: nearest:最可能的值，result :  [48, '4', '4_0.txt', 48, '4', '4_0.txt']
    '''
    if not imgobject:
        im = Image.open('D:/workspace/captcha/34.png')
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
    # im.show()
    im.save(r"C:\Users\HIAPAD\Pictures\ico\cache.png")
    cropli = imagecrop(img_array)

    result = []
    codeli1 = getpicode(im,cropli,"H")
    recognize0("H",result,codeli1,dliH)
    codeli2 = getpicode(im,cropli,"N")
    recognize0("N",result,codeli2,dliN)
    nearest = ""
    if result[0] <= result[3]:
        nearest = result[1]
    else:
        nearest = result[4]
    print("\n",result,"\n最可能的是：",nearest)
    return nearest,result

if __name__ == '__main__':
    recogit()
    #_save2code()