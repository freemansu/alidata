#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/20
# Func:   建立user brand关系模型
# Python Version: 2.6.6

from preprocess import *
from statistics import *
from user_model import *
from brand_model import *

# user活跃度与brand流行度之间的关系
def activity_popularity(user_brand, brand_user):
    
    user_act = user_activity(user_brand)
    brand_pop = brand_popularity(brand_user)

    brand_pop_dict = {}
    for item in brand_pop:
        brand_pop_dict[item[0]] = item[1]

    # 同一act值的user列表
    act_users = {}
    for item in user_act:
        if act_users.has_key(item[1]):
            act_users[item[1]].append(item[0])
        else:
            act_users[item[1]] = [item[0]]

    act_pop = []
    # 统计同一act的所有user购买过的brand的平均流行度
    user_brand_action = user_brand_action_count(user_brand)
    for act in act_users.keys():
        # user列表
        brand_count = 0
        pop = 0
        for user in act_users[act]:
            # 同一user购买brand列表
            for brand in user_brand_action[user].keys():
                if user_brand_action[user][brand][1] > 0:
                    brand_count += 1
                    pop += brand_pop_dict[brand]
        if brand_count == 0:
            act_pop.append([act, 0])
        else:
            act_pop.append([act, 1.0*pop/brand_count])

    return act_pop
