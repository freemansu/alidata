#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/13
# Func:   实现统计功能
# Python Version: 2.6.6

from preprocess import *


# 统计user数
def user_count(user_brand):
    return len(user_brand)


# 统计brand数
def brand_count(brand_user):
    return len(brand_user)


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

# user对各个brand的action统计
def user_brand_action_count(user_brand):
    user_brand_action = {}

    for user in user_brand.keys():
        brand_action = {}
        action = [0,0,0,0]
        for record in user_brand[user]:
            if not brand_action.has_key(record[0]):
                action = [0, 0, 0, 0]
                action[record[1]] += 1
                brand_action[record[0]] = action
            else:
                brand_action[record[0]][record[1]] += 1
            
            #print brand_action[record[0]]

        user_brand_action[user] = brand_action

    return user_brand_action
