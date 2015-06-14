#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/20
# Func:   建立brand模型
# Python Version: 2.6.6

from preprocess import *

# brand购买流行度分布
def brand_buy_popularity(brand_record):
    brand_buy_pop = dict()
    for brand_id, records in brand_record.items():
        brand_buy_pop[brand_id] = len(filter(lambda x : x[1]==1, records))

    brand_buy_pop_sorted = sorted(brand_buy_pop.items(), key=lambda x:x[1], reverse=True)

    brand_buy_pop_file = open('../result/brand_model/brand_buy_popularity.txt', 'w')
    for brand_id, pop in brand_buy_pop_sorted:
        brand_buy_pop_file.write('%d\t%d\n' %(brand_id,  pop))
    brand_buy_pop_file.close()

    return brand_buy_pop


# brand点击流行度分布
def brand_click_popularity(brand_record):
    brand_click_pop = dict()

    for brand_id, records in brand_record.items():
        brand_click_pop[brand_id] = len(filter(lambda x : x[1]==0, records))

    brand_click_pop_sorted = sorted(brand_click_pop.items(), key=lambda x:x[1], reverse=True)

    brand_click_pop_file = open('../result/brand_model/brand_click_popularity.txt', 'w')
    for brand_id, pop in brand_click_pop_sorted:
        brand_click_pop_file.write('%d\t%d\n' %(brand_id, pop))

    return brand_click_pop


# brand购买次数和点击次数之比
def brand_buy_by_click(brand_buy_pop, brand_click_pop):
    buy_by_click = dict()

    for brand_id in brand_buy_pop.keys():
        if brand_click_pop[brand_id]:
            buy_by_click[brand_id] = 1.0 * brand_buy_pop[brand_id] / brand_click_pop[brand_id]
        else:
            buy_by_click[brand_id] = float('Inf')
    
    buy_by_click_file = open('../result/brand_model/brand_buy_by_click.txt', 'w')
    brand_buy_pop_sorted = sorted(brand_buy_pop.items(), key=lambda x:x[1], reverse=True)
    for brand_id, buy in brand_buy_pop_sorted:
        buy_by_click_file.write('%d\t%d\t%d\t%f\n' % (brand_id, buy, brand_click_pop[brand_id], buy_by_click[brand_id]))
    buy_by_click_file.close()

    return buy_by_click


# 被购买的brand数随时间的变化
def brand_buy_date(brand_record):
    min_date, max_date = find_min_max_date(user_brand)
    brand_buy = [0] * (max_date - min_date).days

    for records in brand_values.values():
        map(lambda x : brand_buy[(x[2]-min_date).days]+1, filter(lambda x : x[1]==1, records))

    return brand_buy


# 被点击的brand数随时间的变化
def brand_click_date(brand_user):
    min_date, max_date = find_min_max_date(user_brand)
    brand_click = [0] * (max_date - min_date).days

    for records in brand_record.values():
        map(lambda x : brand_click[(x[2]-min_date).days]+1, filter(lambda x : x[1]==0, records))

    return brand_click


# 测试
if __name__ == '__main__':
    input_file = open('../dataset/original_data.csv', 'r')
    user_record = read(input_file)
    brand_record = transform(user_record)
    brand_buy_pop = brand_buy_popularity(brand_record)
    brand_click_pop = brand_click_popularity(brand_record)
    brand_buy_by_click(brand_buy_pop, brand_click_pop)
