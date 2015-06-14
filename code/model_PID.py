#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/16
# Func:   实现兴趣度模型(PID)
# Python Version: 2.6.6

from preprocess import *
from train_test_set import *
from statistics import *
from user_model import *
import numpy as np
import math

# 计算各action的权重
def weight(user_brand):
    user_action_num = user_action_count(user_brand)

    # N 为用户数
    N = user_count(user_brand)
    
    B = np.zeros((N, 4))

    i = 0
    for user in user_action_num.keys():
        B[i][:] = user_action_num[user]
        i += 1

    # 标准化B
    norm_B = np.zeros((N, 4))
    for i in range(N):
        for j in range(4):
            norm_B[i][j] = float(B[i][j] - np.min(B[i][:])) / (np.max(B[i][:]) - np.min(B[i][:]))
        #    norm_B[i][j] = float( np.max(B[i][:]) - B[i][j]) / (np.max(B[i][:]) - np.min(B[i][:]))
        #print norm_B[:][i]

    #print B[:][0]
    # H 信息熵

    H = np.array([0.0, 0.0, 0.0, 0.0])

    for j in range(4):
        tmp1 = np.array(norm_B[:][j]) / np.sum(norm_B[:][j])
        tmp = np.zeros(4)
        for i in range(4):
            if not tmp1[i] > 0:
                tmp[i] = 0.0
            else:
                tmp[i] = tmp1[i] * np.log(tmp1[i])
        
        #print tmp
        H[j] = -np.sum(tmp) / np.log(4)
        #print H[j]

    # W 权重
    W = np.array([0.0, 0.0, 0.0, 0.0])
    for j in range(4):
        W[j] = (1 - H[j]) / (4 - np.sum(H))

    print W

    return W




# 实现兴趣度模型,trian_set为user_record类型的字典
def model_PID(user_record):
    # 4种action的权重
    w = np.array([0.1, 0.46, 0.1, 0.34])

    brand_record = transform(user_record)
    user_ids = sorted(user_record.keys())
    brand_ids = brand_ids = sorted(brand_record.keys())
    # action_矩阵
    (A0, A1, A2, A3) = action_matrixs(user_record)
    A = A0*w[0] + A1*w[1] + A2*w[2] + A3*w[3]

    # 用户平均一个月的购买数
    user_buy_num = dict()
    for user, num in user_buy_activity(user_record).items():
        user_buy_num[user] = num / 4.0
    user_buy_num = sorted(user_buy_num.iteritems(), key=lambda d:d[1], reverse=True)
    user_will_buy = dict(filter(lambda x:x[1] >= 0, user_buy_num))
    
    # 预测
    prediction_set = dict()
    for i, data in enumerate(A):
        if user_ids[i] in user_will_buy.keys():
            indexs = np.argsort(data)[::-1][0 : int(user_will_buy[user_ids[i]])+2] # 从大到小排序的序号
            prediction_set[user_ids[i]] = map(lambda x:brand_ids[x], indexs)

    # 将prediction_set写入到prediction文件
    prediction_file = open('../result/predict_PID.txt', 'w')
    for user_id, brand_ids in prediction_set.items():
        prediction_file.write('%d\t%s\n' %(user_id, ','.join(map(str, brand_ids))))
    prediction_file.close()
    
    return prediction_set


# 测试
if __name__ == '__main__':
    input_file = open('../dataset/original_data.csv', 'r')
    user_record = read(input_file)
    model_PID(user_record)
