#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/20
# Func:   建立user模型
# Python Version: 2.6.6
from preprocess import *

# user购买活跃度分布
def user_buy_activity(user_record):
    user_buy_act = dict()
    for user_id, records in user_record.items():
        user_buy_act[user_id] = len(filter(lambda x : x[1]==1, records))

    '''user_buy_act_file = open('../result/user_model/user_buy_activity.txt', 'w')
    for user_id, act in user_buy_act.items():
        user_buy_act_file.write('%s\t%s\n' %(str(user_id), str(act)))
    user_buy_act_file.close()
    '''
    return user_buy_act


# user点击活跃度分布
def user_click_activity(user_record):
    user_click_act = dict()

    for user_id, records in user_record.items():
        user_click_act[user_id] = len(filter(lambda x : x[1]==0, records))

    user_click_act_file = open('../result/user_model/user_click_activity.txt', 'w')
    for user_id, act in user_click_act.items():
        user_click_act_file.write('%s\t%s\n' %(str(user_id), str(act)))
    user_click_act_file.close()

    return user_click_act


# 有购买行为的user数随时间的变化
def user_buy_date(user_record):
    min_date, max_date = find_min_max_date(user_record)
    user_buy = [0] * ((max_date - min_date).days+1)

    def add(x):
        user_buy[(x[2]-min_date).days] = user_buy[(x[2]-min_date).days] + 1

    for user_id, records in user_record.items():
        map(add, filter(lambda x : x[1]==1, records))
    
    user_buy_date_file = open('../result/user_model/user_buy_date.txt', 'w')
    for date, buy in enumerate(user_buy):
        user_buy_date_file.write('%d\t%d\n' %(date, buy))
    user_buy_date_file.close()

    return user_buy


# 有点击行为的user数随时间的变化
def user_click_date(user_brand):
    min_date, max_date = find_min_max_date(user_record)
    user_click = [0] * ((max_date - min_date).days+1)
    def add(x):
        user_click[(x[2]-min_date).days] = user_click[(x[2]-min_date).days] + 1

    for user_id, records in user_record.items():
        map(add, filter(lambda x : x[1]==0, records))

    user_click_date_file = open('../result/user_model/user_click_date.txt', 'w')
    for date, click in enumerate(user_click):
        user_click_date_file.write('%d\t%d\n' %(date, click))
    user_click_date_file.close()

    return user_click


# 用户纠结度
def user_hesitation(user_buy_act, user_click_act):
    user_hesitation = dict()
    for user_id in user_buy_act.keys():
        if user_click_act[user_id] != 0:
            user_hesitation[user_id] = 1.0 * user_buy_act[user_id] / user_click_act[user_id]
        else:
            user_hesitation[user_id] = 1.0 * user_buy_act[user_id]

    user_hesitation_file = open('../result/user_model/user_hesitation.txt', 'w')
    for user_id, hesitation in user_hesitation.items():
        user_hesitation_file.write('%d\t%f\n' %(user_id, hesitation))
    user_hesitation_file.close()


# 统计每个用户的记录条数
def user_record_count(user_record):
    user_record_num = dict()
    for user_id, records in user_record.items():
        user_record_num[user_id] = len(records)

    user_record_num_file = open('../result/user_model/user_record_count.txt', 'w')
    for user_id, record_num in user_record_num.items():
        user_record_num_file.write('%d\t%d\n' %(user_id, record_num))
    user_record_num_file.close()

# 测试
if __name__ == '__main__':
    input_file = open('../dataset/original_data.csv', 'r')
    user_record = read(input_file)
    user_buy_act = user_buy_activity(user_record)
    user_click_act = user_click_activity(user_record)
    user_buy_date(user_record)
    user_click_date(user_record)
    user_hesitation(user_buy_act, user_click_act)
    user_record_count(user_record)
