#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/21
# Func:   实现基于用户的协同过滤算法(Collaborative Filtering)
# Python Version: 2.6.6

from preprocess import *
from train_test_set import *
from score import *
from statistics import *

import numpy as np
import math


# 用户相似度
def user_similarity(user_brand):

    brand_user = transform(user_brand)

    # U_S为用户相似度矩阵
    U_S = {}

    C = {}
    N = {}
    for brand, records in brand_user.items():
        for record_u in records:
            if N.has_key(record_u[0]):
                N[record_u[0]] += 1
            else:
                N[record_u[0]] = 1
            for record_v in records:
                if record_u[0] == record_v[0]:
                    continue
                if C.has_key(record_u[0]):
                    if C[record_u[0]].has_key(record_v[0]):
                        C[record_u[0]][record_v[0]] += 1
                    else:
                        C[record_u[0]][record_v[0]] = 1
                else:
                    C[record_u[0]] = {record_v[0]:1}


    # 计算相似度矩阵U_S
    for u, related_users in C.items():
        U_S[u] = {}
        for v, cuv in related_users.items():
            U_S[u][v] = cuv / math.sqrt(N[u] * N[v])

    return U_S
    


# 实现基于用户协同过滤算法(Collaborative Filtering)
def model_user_CF(user_brand):
    rank = {}
    return prediction_set



if __name__ == '__main__':
    input_file = open('../dataset/original_data.csv', 'r')
    user_brand, brand_user, counts = read(input_file)

    user_similarity(user_brand)
