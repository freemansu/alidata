#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/14
# Func:   计算成绩 
# Python Version: 2.6.6


# 计算模型准确率
def precision(prediction_set, test_set):
    sum_hitBrands = 0
    sum_pBrands = 0
    for user_id, brand_ids in prediction_set.items():
        sum_pBrands += len(brand_ids)
        sum_hitBrands += len(brand_ids & test_set.get(user_id, set())
    return (float)sum_hitBrands/(float)sum_pBrands


# 计算模型召回率
def recall(prediction_set, test_set):
    sum_hitBrands = 0
    sum_bBrands = 0
    for user_id, brand_ids in test_set.items():
        sum_bBrands += len(brand_ids)
        sum_hitBrands += len(brand_ids & prediction_set.get(user_id, set()))

    return 1.0*sum_hitBrands / sum_bBrands


# 计算F1_score
def F1_score(P, R):
    return (2.0*P*R) / (P+R)


# 计算prediction_set与test_set中user的交集
def user_predict_count(prediction_set, test_set):
    return set(prediction_set.keys()) & set(test_set.keys())


# 计算在测试集不在训练集的user
def new_user(train_set, test_set):
    return set(test_set.keys()) - set(prediction_set.keys())
