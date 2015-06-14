#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/13
# Func:   将原始数据集分成训练集合测试集
# Python Version: 2.6.6

from preprocess import *

# 找到最后一个月
def find_last_month(user_brand):
    last_month = 1

    for user in user_brand.keys():
        for record in user_brand[user]:
            if record[2].month > last_month:
                last_month = record[2].month

    return last_month

# 把最后一个月的数据作为测试集, 其余数据作为训练集
def get_train_test_set(user_brand, last_month):

    train_set = {}
    test_set = {}

    for user in user_brand.keys():
        for record in user_brand[user]:
            if record[2].month < 7 or (record[2].month == 7 and record[2].day<16 ):
                if not train_set.has_key(user):
                    train_set[user] = [record]
                else:
                    train_set[user].append(record)
            else:
                if record[1] == 1:
                    if not test_set.has_key(user): 
                        test_set[user] = [record[0]]
                    else:
                        if not record[0] in test_set[user]:    # test_set里brand列表去重
                            test_set[user].append(record[0])
        
    return (train_set, test_set)

# 将训练数据集写入文件
def train2file(train_set, output_file):
    for user in train_set.keys():
        for record in train_set[user]:
            outline = str(user) + ',' + str(record[0]) + ',' + str(record[1]) + \
                    str(record[2].month) + '.' + str(record[2].day) + '\n'
            output_file.write(outline)

    output_file.close()

# 将测试数据集写入文件
def test2file(test_set, output_file):
    for user in test_set.keys():
        outline = str(user) + '\t'
        for i in range(len(test_set[user])):
            if i < len(test_set[user])-1:
                outline += str(test_set[user][i]) + ','
            else:
                outline += str(test_set[user][i]) + '\n'
        output_file.write(outline)

    output_file.close()


if __name__ == '__main__':
    
    # t_alibaba_data_utf8.csv去掉了原来数据文件的第一行，并转换成utf-8编码

    input_file = open('../dataset/original_data.csv', 'r')
    
    train_file = open('../dataset/train_set.txt', 'w')
    test_file  = open('../dataset/test_set.txt', 'w')

    user_brand, brand_user, counts = read(input_file)

    last_month = find_last_month(user_brand)

    train_set, test_set = get_train_test_set(user_brand, last_month)

    train2file(train_set, train_file)
    test2file(test_set, test_file)
