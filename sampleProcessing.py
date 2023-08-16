# sampleProcessing

import os
import re
import torch


# 自助法 取得大约2/3作为训练集 剩下作为测试集
# 输入所有样本的list 返回训练集的index的list
def getTrainSet(num):
    train_set_index = torch.unique(torch.randint(high=num, size=(num,)))
    print(train_set_index)
    return train_set_index.tolist()


# 样本清洗，返回一个list
# list内的每个元素是类似于如下格式的一个 str 这里只有5言诗
# 檄(李峤)羽檄本宣明,由来敷木声,联翩通汉国,迢递入燕营,毛义持书去,张仪韫璧行,曹风虽觉愈,陈草始知名
# $题目$($作者$)$诗句$
# 诗句中的每句诗通过 英文, 分隔
def getAllPoems():
    path = 'All_samples'
    after_samples = []
    with open(os.path.join(path, 'all_samples.txt'), encoding='gb18030') as f:
        samples = f.read()
        sample_list = samples.split('◎卷.')[1:]
        for i in sample_list:
            try:
                a = i.split('【')[1]
            except BaseException as data:
                print(i)
            else:
                stan = list(filter(None, re.split('，|。|\n\u3000\u3000', a)[1:]))
                title = re.split('】', re.split('，|。|\n\u3000\u3000', a)[0])
                sum_stan = ''
                five_words = True
                for j in stan:
                    sum_stan += j
                    sum_stan += ','
                    if len(j) != 5 and len(j) != 0:
                        five_words = False
                if five_words:
                    stan_sample = title[0] + '(' + title[1] + ')' + sum_stan[0:-1]
                    print(title)
                    print(stan)
                    print(stan_sample)
                    after_samples.append(stan_sample)

    return after_samples


def writeTestSample(sample, index):
    path = 'Test_samples'
    with open(os.path.join(path, f'{index}.txt'), 'w') as file:
        file.write(sample)


def writeTrainSample(sample, index):
    path = 'Train_samples'
    with open(os.path.join(path, f'{index}.txt'), 'w') as file:
        file.write(sample)


def writeSamplesToTxt(samples, train_index):
    assert isinstance(samples, list)
    num = len(train_index)
    num_sam = len(samples)
    index1 = 0
    index2 = 0
    for i in range(train_index[0]):
        writeTestSample(samples[i], index2)
        index2 += 1
    for i in range(num):
        left = train_index[i]
        if i + 1 == num:
            right = num_sam
        else:
            right = train_index[i + 1]
        writeTrainSample(samples[left], index1)
        index1 += 1
        for j in range(right - left - 1):
            writeTestSample(samples[j + left + 1], index2)
            index2 += 1


samples = getAllPoems()
writeSamplesToTxt(samples, getTrainSet(len(samples)))