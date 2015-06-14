#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/13
# Func:   实现统计功能
# Python Version: 2.6.6

from preprocess import *
import numpy as np
import math
import datetime
import sys

# 统计user关注(点击,购买等4种action)的brand数
def user_brand_count(user_brand):
    user_brand_num = {}

    for user in user_brand.keys():
        user_brand_num[user] = len(user_brand[user])


#统计brand被多少user关注
def brand_user_count(brand_user):
    brand_user_num = {}

    for brand in brand_user.keys():
        brand_user_num[brand] = len(brand_user[brand])

# brand点击数, 购买数, 收藏数, 进入购物车次数
def brand_action_count(brand_user):
    brand_action = {}
    
    for (brand,user_action_date) in brand_user.items():
        
        brand_action[brand] = [0, 0, 0, 0]
        
        for i in range(len(user_action_date)):
            brand_action[brand][user_action_date[i][1]] += 1
    
    return brand_action


# user 的点击数, 购买数, 收藏数, 购物车次数
def user_action_count(user_brand):
    user_action_num = {}

    for user in user_brand.keys():
        action = [0, 0, 0, 0]
        for record in user_brand[user]:
                action[record[1]] += 1
        user_action_num[user] = action

    return user_action_num

# user对各个brand的action统计
def user_brand_action_count(user_brand):
    user_brand_action = {}

    for user in user_brand.keys():
        brand_action = {}
        action = [0,0,0,0]
        for record in user_brand[user]:
            if not brand_action.has_key(record[0]):
                action[record[1]] += 1
                brand_action[record[0]] = action
            else:
                brand_action[record[0]][record[1]] += 1
            
            #print brand_action[record[0]]

        user_brand_action[user] = brand_action

    return user_brand_action

# 无购买行为的user

# 从未被购买过的brand




# 找到最小和最大的日期
def find_min_max_date(user_record):
    min_date = datetime.date.max
    max_date = datetime.date.min
    for records in user_record.values():
        if min([record[2] for record in records]) < min_date:
            min_date = min([record[2] for record in records])
        if max([record[2] for record in records]) > max_date:
            max_date = max([record[2] for record in records])

    return (min_date, max_date)


# 统计user对brand的action矩阵
def action_matrixs(user_record):
    brand_record = transform(user_record)

    user_num = len(user_record)
    brand_num = len(brand_record)

    A0 = np.zeros((user_num, brand_num))
    A1 = np.zeros((user_num, brand_num))
    A2 = np.zeros((user_num, brand_num))
    A3 = np.zeros((user_num, brand_num))

    user_ids = sorted(user_record.keys())
    brand_ids = sorted(brand_record.keys())
    date_start=datetime.date(2013,4,14)
    for user_id, records in user_record.items():
        for record in records:
            if record[1] == 0:
                #A0[user_ids.index(user_id)][brand_ids.index(record[0])] += math.log((record[2]-date_start).days)
                #A0[user_ids.index(user_id)][brand_ids.index(record[0])] += 1.0*((record[2]-date_start).days)/10
                A0[user_ids.index(user_id)][brand_ids.index(record[0])] += math.exp(1.0*((record[2]-date_start).days)/40)-1
            elif record[1] == 1:
                #A1[user_ids.index(user_id)][brand_ids.index(record[0])] += math.log((record[2]-date_start).days)
                #A1[user_ids.index(user_id)][brand_ids.index(record[0])] += 1.0*((record[2]-date_start).days)/10
                A1[user_ids.index(user_id)][brand_ids.index(record[0])] += math.exp(1.0*((record[2]-date_start).days)/40)-1
            elif record[1] == 2:
                #A2[user_ids.index(user_id)][brand_ids.index(record[0])] += math.log((record[2]-date_start).days)
                #A2[user_ids.index(user_id)][brand_ids.index(record[0])] += 1.0*((record[2]-date_start).days)/10
                A2[user_ids.index(user_id)][brand_ids.index(record[0])] += math.exp(1.0*((record[2]-date_start).days)/40)-1
            else:
                #A3[user_ids.index(user_id)][brand_ids.index(record[0])] += math.log((record[2]-date_start).days)
                #A3[user_ids.index(user_id)][brand_ids.index(record[0])] += 1.0*((record[2]-date_start).days)/10
                A3[user_ids.index(user_id)][brand_ids.index(record[0])] += math.exp(1.0*((record[2]-date_start).days)/40)-1

    # 输出到文件
    '''A0_file = open('../result/statistics/A0.txt', 'w')
    A1_file = open('../result/statistics/A1.txt', 'w')
    A2_file = open('../result/statistics/A2.txt', 'w')
    A3_file = open('../result/statistics/A3.txt', 'w')
    for col in A0:
        A0_file.write(' '.join(map(str, col)) + '\n')
    A0_file.close()
    for col in A1:
        A1_file.write(' '.join(map(str, col)) + '\n')
    A1_file.close()
    for col in A2:
        A2_file.write(' '.join(map(str, col)) + '\n')
    A2_file.close()
    for col in A3:
        A3_file.write(' '.join(map(str, col)) + '\n')
    A3_file.close()
    '''
    return (A0, A1, A2, A3)

# 测试
if __name__ == '__main__':
    input_file = open('../dataset/original_data.csv', 'r')
    user_record = read(input_file)
    action_matrixs(user_record)
