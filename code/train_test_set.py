#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/13
# Func:   将原始数据集分成训练集合测试集
# Python Version: 2.6.6
from preprocess import *
from statistics import *
from datetime import timedelta

# 分离训练集与测试集
# train_months为训练集月份列表, 例如[1, 2]表示第1个月和第2个月
# test_months表示测试集列表,解释同上
def get_train_test_set(user_record, train_months, test_months):
    min_date, max_date = find_min_max_date(user_record)
    train_date_list = list()
    test_date_list = list()

    for month in train_months:
        if month == 4:
            train_date_list += [min_date+timedelta(days=d) for d in range((month-1)*30, month*30+2)]
        else:
            train_date_list += [min_date+timedelta(days=d) for d in range((month-1)*30, month*30)]

    for month in test_months:
        if month == 4:
            test_date_list += [min_date+timedelta(days=d) for d in range((month-1)*30, month*30+2)]
        else:
            test_date_list += [min_date+timedelta(days=d) for d in range((month-1)*30, month*30)]

    # train_set形式与user_record一致
    # test_set以user_id为key, brand_id的set为value
    train_set = {}
    test_set = {}
    for user_id, records in user_record.items():
        train_records = [record for record in records if record[2] in train_date_list]
        test_records = [record for record in records if record[2] in test_date_list and record[1] == 1]
        if not train_records:
            train_set[user_id] = train_records
        if not test_records:
            test_set[user_id] = set(record[0] for record in test_records)
        
    return (train_set, test_set)


# 将测试数据集写入文件
def test2file(test_set, output_file):
    for user_id, brand_ids in test_set.items():
        output_file.write('%d\t%s\n' %(user_id, ','.join(map(str, brand_ids))))

    output_file.close()


# main
if __name__ == '__main__':
    input_file = open('../dataset/original_data.csv', 'r')
    train_file = open('../dataset/train_set.txt', 'w')
    test_file  = open('../dataset/test_set.txt', 'w')

    user_record = read(input_file)

    train_months = [1, 2, 3]
    test_months = [4]
    train_set, test_set = get_train_test_set(user_record, train_months, test_months)

    write(train_set, train_file)
    test2file(test_set, test_file)
