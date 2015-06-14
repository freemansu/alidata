#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/14
# Func:   score 
# Python Version: 2.6.6

from train_test_set import *

# 计算模型准确率
def precision(prediction_set, test_set):
    sum_hitBrands = 0
    sum_pBrands = 0

    for user in prediction_set.keys():
        sum_pBrands += len(prediction_set[user])
        if test_set.has_key(user):
            sum_hitBrands += len([item for item in prediction_set[user] if item in test_set[user]])

    return float(sum_hitBrands)/sum_pBrands


# 计算模型召回率
def recall(prediction_set, test_set):
    sum_hitBrands = 0
    sum_bBrands = 0
    
    for user in test_set.keys():
        sum_bBrands += len(test_set[user])
        if prediction_set.has_key(user):
            sum_hitBrands += len([item for item in prediction_set[user] if item in test_set[user]])

    return float(sum_hitBrands)/sum_bBrands


# 计算F1_score
def F1_score(P, R):
    return (2*P*R) / (P+R)

# 计算prediction_set与test_set中user的交集的元素个数
def user_predict_count(prediction_set, test_set):
    user_count = 0

    for user in prediction_set.keys():
        if user in test_set.keys():
            user_count += 1

    return user_count
