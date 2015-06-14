#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/16
# Func:   main 
# Python Version: 2.6.6


from preprocess import *
from train_test_set import *
from score import *
from statistics import *
from model_PID import *
from model_UID import *
from lastweek import *
from splittime import *

if __name__ == '__main__':

    input_file = open('original_data.csv', 'r')
    prediction_file = open('predict_nnnew.txt', 'w')
    user_brand, brand_user, counts = read(input_file)
    train_set, test_set = get_train_test_set(user_brand, find_last_month(user_brand))
    lastweek=getlastweek(user_brand)
    predictfile=open('predict_PID.txt','r')
    prediction=predictfile.read()
    prediction_data=prediction.split('\n')
    #print lastweek
    #print prediction_data
    prediction_set={}
    for data in prediction_data:
        dat=data.split('\t')
        #print dat
        brand=[int(i) for i in dat[1].split(',')]

        #dat[1].split(',')
        user=int(dat[0])
        prediction_set[user]=brand






    #print lastweek
    # 使用模型产生预测结果
    '''
    prediction_set = model_PID(user_brand)
    prediction_set = combine(prediction_set,lastweek)
    firstset,secondset=splitdata(user_brand,7,15)
    prediction_set=getnewpairs(firstset,secondset)
    prediction_set=model_UID(train_set)'''
    prediction_set = combine(prediction_set,lastweek)
    #print prediction_set
     # 写入到prediction文件
    for user in prediction_set.keys():
        prediction_line = str(user) + '\t' + str(prediction_set[user][0])
        for brand in prediction_set[user]:
            if not brand == prediction_set[user][0]:
                prediction_line += ',' + str(brand)
        prediction_line += '\n'
        prediction_file.write(prediction_line)
    prediction_file.close()
    #print prediction_set
    #print prediction_set
    print 'predict count = ' + str(user_count(prediction_set))
    print 'test_set count = ' + str(user_count(test_set))
    print 'user count = ' + str(user_predict_count(prediction_set, test_set))
    P = precision(prediction_set, test_set)
    print 'P  = ' + str(P)
    R = recall(prediction_set, test_set)  
    print 'R  = ' + str(R)              
    F1 = F1_score(P, R)
    u_p = user_predict_count(prediction_set, test_set) / float(user_count(prediction_set))
    print 'user precision = ' + str(u_p)
    
    
    print 'F1 = ' + str(F1_score(P, R))
   
   
   