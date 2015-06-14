#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/13
# Func:   数据预处理
# Python Version: 2.6.6

import sys
#from datetime import datetime, date
import datetime
# 设置默认字符编码
reload(sys)
sys.setdefaultencoding('utf-8')


# 将一行字符串处理成包含各个字段的列表
def line_process(line):
    user_id_str, brand_id_str, action_type_str, date_str = line.split(',')    #分割line
    date_str = date_str.replace(u'月', '.').replace(u'日', '')    #将X月YY替换成X.YY
    month, day = date_str.split('.')
    visit_date = datetime.date(2013, int(month), int(day))

    return [int(user_id_str), int(brand_id_str), int(action_type_str), visit_date]
    

# 读取数据文件，保持数据到user_record
# user_record是包含所有数据的以user_id为key的字典
def read(input_file):
    user_record = dict()
    for line in input_file.readlines():
        user_id, brand_id, action_type, visit_date = line_process(line)
        user_record.setdefault(user_id, []).append([brand_id, action_type, visit_date])
    input_file.close()

    return user_record


# 将字典中的记录按日期排序
def sort_by_date(data):
    for records in data.values():
        records.sort(key=lambda x : (x[2], x[0], x[1]))
    return data


# 将字典中的记录按record[0]排序
def sort_by_record0(data):
    for records in data.values():
        records.sort(key=lambda x : (x[0], x[2], x[1]))
    return data


# 将字典写入文件
def write(data, output_file):
    for key, records in data.items():
        for record in records:
            output_file.write('%d,%d,%d,%d月%d日\n' % \
                    (key, record[0], record[1] ,record[2].month, record[2].day))

    output_file.close()


# 将user_record字典转换到brand_record字典
# brand_record是包含所有数据的以brand_id为key的字典
def transform(user_record):
    brand_record = dict()
    for user_id, records in user_record.items():
        for record in records:
            brand_record.setdefault(record[0], []).append([user_id, record[1], record[2]])

    return brand_record


# 测试
if __name__ == '__main__':
   input_file = open('../dataset/original_data.csv', 'r')
   user_by_date_file = open('../result/preprocess/user_record_date.txt', 'w')
   brand_by_date_file = open('../result/preprocess/brand_record_date.txt', 'w')
   user_by_brand_file = open('../result/preprocess/user_record_brand.txt', 'w')
   brand_by_user_file = open('../result/preprocess/brand_record_user.txt', 'w')
   user_record = read(input_file)
   brand_record = transform(user_record)
   write(sort_by_date(user_record), user_by_date_file)
   write(sort_by_date(brand_record), brand_by_date_file)
   write(sort_by_record0(user_record), user_by_brand_file)
   write(sort_by_record0(brand_record), brand_by_user_file)
