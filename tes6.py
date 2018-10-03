import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import validation_curve
from sklearn import svm
import os

os.chdir(r'D:\tesseractocr\checkcode')


class open_deal_image:
    '''
    open_image:提供一个打开图片并且灰度化的方法
    image_two_deal:提供一个将图片二值化的方法
    image_noise_deal：提供一个将图片去除噪音的方法
    get_start_index_deal :返回第一个数字的位置
    get_end_index_deal :返回最后一个数字的位置
    split_one_deal:分割验证码的方法
    split_two_deal:细分割
    add_char_deal:提供一个将分割的图片补全的方法'''

    def open_image(self, image_add):
        image = Image.open(image_add).convert('L')
        return image

    def image_two_deal(self, image):
        image_np = np.array(image)
        rows, cols = image_np.shape
        for i in range(rows):
            for j in range(cols):
                if (image_np[i, j] <= 128):
                    image_np[i, j] = 0
                else:
                    image_np[i, j] = 1
        return image_np

    def image_noise_deal(self, image_np):
        rows, cols = image_np.shape
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                num = 0
                if image_np[i - 1, j]: num += 1
                if image_np[i + 1, j]: num += 1
                if image_np[i, j - 1]: num += 1
                if image_np[i, j + 1]: num += 1
                if num >= 3:
                    image_np[i, j] = 1
        return image_np

    def get_start_index_deal(self, image_np):
        self.image_np_var = image_np.var(axis=0)
        for i in range(1, len(self.image_np_var) - 1):
            if self.image_np_var[i] != self.image_np_var[i - 1]:
                return i - 1

    def get_end_index_deal(self, image_np):
        for i in range(len(self.image_np_var) - 1, 0, -1):
            if self.image_np_var[i] != self.image_np_var[i - 1]:
                return i + 1

    def split_one_deal(self, start_num, end_num, image_np):
        image_np_var_deal = self.image_np_var[start_num: end_num]
        var_deal, every_length, image_np_deal_list = [], [], []
        image_np_deal = image_np[:, start_num:end_num]
        number = 0
        for i in range(len(image_np_var_deal)):
            if image_np_var_deal[i] == 0:
                if image_np_var_deal[i - 1] != 0:
                    var_deal.append(image_np_var_deal[number + 1:i])
                    image_np_deal_list.append(image_np_deal[:, number + 1:i])
                    every_length.append(i - number - 1)
                    number = i
                else:
                    number = i
        return image_np_deal_list, every_length

    def split_two_deal(self, image_np_deal_list, every_length):
        g = image_np_deal_list
        d = every_length
        if len(d) < 4:
            leaveout = 4 - len(d)
            if leaveout == 1:
                max_index = d.index(max(d))
                one, two = np.array_split(g[max_index], 2, axis=1)
                g.pop(max_index)
                g.insert(max_index, two)
                g.insert(max_index, one)
            if leaveout == 3:
                result = np.array_split(g[0], 4, axis=1)
                g.pop()
                g.extend(result)
            if leaveout == 2:
                if 0.4 < d[0] / d[1] < 2.5:
                    one, two = np.array_split(g[0], 2, axis=1)
                    three, four = np.array_split(g[1], 2, axis=1)
                    g = [one, two, three, four]
                else:
                    max_index = d.index(max(d))
                    one, two, three = np.array_split(g[max_index], 3, axis=1)
                    g.pop(max_index)
                    g.insert(max_index, three)
                    g.insert(max_index, two)
                    g.insert(max_index, one)
        elif len(d) > 4:
            for i, j in enumerate(d):
                if j == 1:
                    g.pop(i)
        elif len(d) == 4:
            for i, j in enumerate(d):
                if j == 1:
                    g.pop(i)
                    d.pop(i)
                    return self.split_two_deal(g, d)
        return g

    def _split_checkcode(self, one):
        for i in range(18 - one.shape[1]):
            if i % 2:
                one = np.hstack((np.array([1] * 27)[:, np.newaxis], one))
            else:
                one = np.hstack((one, np.array([1] * 27)[:, np.newaxis]))
        one = one.ravel()[np.newaxis, :]
        return one

    def add_char_deal(self, g):
        new_g = [self._split_checkcode(i) for i in g]
        return np.vstack(new_g)


# 给个处理好的图片的矩阵存在x
x = []
for i in range(180):
    a = open_deal_image()
    add = str(i) + '.gif'
    image = a.open_image(add)
    image_np = a.image_two_deal(image)
    image_np = a.image_noise_deal(image_np)
    start_num = a.get_start_index_deal(image_np)
    end_num = a.get_end_index_deal(image_np)
    image_np_deal_list, every_length = a.split_one_deal(start_num, end_num, image_np)
    g = a.split_two_deal(image_np_deal_list, every_length)
    x.append(a.add_char_deal(g))

x = np.vstack([x[i] for i in range(180)])

# 打开验证码的答案
class_ = list('0123456789abcdefghijklmnopqrstuvwxyz')
y_class = {i: class_[i] for i in range(36)}
y_class2 = {class_[i]: i for i in range(36)}
str1 = ''
with open('checkcode.txt', 'r') as f:
    for i in f.readlines():
        str1 += i
y = str1.replace('\n', '')
new_yy = [y_class2[i] for i in y]

# 验证曲线


param_name = 'C'
param_range = np.logspace(-2, 2)
train_scores, test_scores = validation_curve(svm.SVC(gamma=0.001), x, np.array(new_yy),
                                             param_name=param_name, param_range=param_range, cv=10)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.semilogx(param_range, train_scores_mean, label='train', color='r')
ax.fill_between(param_range, train_scores_mean - train_scores_std,
                train_scores_mean + train_scores_std, alpha=0.2, color='r')
ax.semilogx(param_range, test_scores_mean, label='test', color='g')
ax.fill_between(param_range, test_scores_mean - test_scores_std,
                test_scores_mean + test_scores_std, alpha=0.2, color='g')
ax.legend(loc='best')
plt.show()

param_name = 'gamma'
param_range = np.linspace(0, 1)
train_scores, test_scores = validation_curve(svm.SVC(C=100), x, np.array(new_yy),
                                             param_name=param_name, param_range=param_range, cv=10)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(param_range, train_scores_mean, label='train', color='r')
ax.fill_between(param_range, train_scores_mean - train_scores_std,
                train_scores_mean + train_scores_std, alpha=0.2, color='r')
ax.plot(param_range, test_scores_mean, label='test', color='g')
ax.fill_between(param_range, test_scores_mean - test_scores_std,
                test_scores_mean + test_scores_std, alpha=0.2, color='g')
ax.legend(loc='best')
plt.show()

# 学习曲线
from sklearn.model_selection import learning_curve

train_sizes = np.linspace(0.1, 1.0, endpoint=True, dtype='float')
abs_train_sizes, train_scores, test_scores = learning_curve(svm.SVC(gamma=0.001, C=100), x, np.array(new_yy), cv=10,
                                                            train_sizes=train_sizes)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(abs_train_sizes, train_scores_mean, label='train', color='r')
ax.fill_between(abs_train_sizes, train_scores_mean - train_scores_std,
                train_scores_mean + train_scores_std, alpha=0.2, color='r')
ax.plot(abs_train_sizes, test_scores_mean, label='test', color='g')
ax.fill_between(abs_train_sizes, test_scores_mean - test_scores_std,
                test_scores_mean + test_scores_std, alpha=0.2, color='g')
ax.set_xlim(0, 1000)
ax.legend(loc='best')
plt.show()

# 通过上面的图确定的系数



def modtrain(a, new_yy, i):
    svc = svm.SVC(gamma=0.001, C=100)
    svc.fit(a[:i * 4], np.array(new_yy[:i * 4]))
    # print(svc.score(a[:i*4],np.array(new_yy[:i*4])))
    print(svc.score(a[i * 4:], np.array(new_yy[i * 4:])))
    y_predict = svc.predict(a[i * 4:])
    y_true = np.array(new_yy[i * 4:])
    return y_predict, y_true


y_predict, y_true = modtrain(x, new_yy, 140)
y_predict_class = [y_class[i] for i in y_predict]
y_true_class = [y_class[i] for i in y_true]
result_char = ''.join(y_predict_class)
true_char = ''.join(y_true_class)

count = 0
for i in range(0, 160, 4):
    if result_char[i:i + 4] == true_char[i:i + 4]:
        count += 1
print(count)
print(count / 40)
