#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/13
# Func:   数据预处理
# Python Version: 2.6.6

import sys
import datetime

# 设置默认字符编码
reload(sys)
sys.setdefaultencoding('utf-8')


# 将一行字符串处理成包含各个字段的列表
def line_process(line):
    user_id_str, brand_id_str, action_type_str, date_str = line.split(',')    #分割line

    # 将读到的string转换为整数
    user_id = int(user_id_str)
    brand_id = int(brand_id_str)
    action_type = int(action_type_str)
    
    # 处理日期
    date_str = date_str.replace(u'月', '.').replace(u'日', '')    #将X月YY替换成X.YY
    year = 2013    #假设年份是2013年
    month, day = date_str.split('.')
    visit_date = datetime.datetime(year, int(month), int(day))    #转换成datetime对象

    # 返回一条记录
    return [user_id, brand_id, action_type, visit_date]
    

# 读取数据文件，保持数据到user_brand, brand_user字典
def read(input_file):

    # 将整个文件一次全部读入内存
    records = input_file.readlines()
    input_file.close()

    # user_brand是包含所有数据的以user_id为key的字典
    # brand_user是包含所有数据的以brand_id为key的字典
    user_brand = {}
    brand_user = {}

    # record_count保存记录条数
    record_count = len(records)

    # action_counts保存各个action的记录条数
    action_counts = [0, 0, 0, 0]

    for line in records:
        user_id, brand_id, action_type, visit_date = line_process(line)

        # 各个action计数
        action_counts[action_type] += 1

        # 写user_brand字典记录
        if not user_brand.has_key(user_id):
            user_brand[user_id] = [[brand_id, action_type, visit_date]]
        else:
            user_brand[user_id].append([brand_id, action_type, visit_date])

        # 写brand_user字典记录
        if not brand_user.has_key(brand_id):
            brand_user[brand_id] = [[user_id, action_type, visit_date]]
        else:
            brand_user[brand_id].append([user_id, action_type, visit_date])
    
    # counts合并所有计数值
    counts = action_counts
    counts.append(record_count)

    return (user_brand, brand_user, counts)

# 将user_brand字典转换到brand_user字典
def transform(user_brand):
    brand_user = {}
    for user in user_brand.keys():
        for record in user_brand[user]:
            if not brand_user.has_key(record[0]):    #record[0]为brand
                brand_user[record[0]] = [[user, record[1], record[2]]]
            else:
                brand_user[record[0]].append([user, record[1], record[2]])

    return brand_user
