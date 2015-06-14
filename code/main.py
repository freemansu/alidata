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

if __name__ == '__main__':

    input_file = open('../dataset/original_data.csv', 'r')

    user_brand, brand_user, counts = read(input_file)

    train_set, test_set = get_train_test_set(user_brand)
    
    # 使用模型产生预测结果
    w1 = np.arange(0.1, 1.0, 0.1)
    w2 = np.arange(0.1, 1.0, 0.1)
    w3 = np.arange(0.1, 1.0, 0.1)
    
    test_file = open('../result/test_result.txt', 'w')
    '''
    c = 0
    for i in w1:
        for j in w2:
            for k in w3:
                if i+j+k<1:
                    w = np.array([i,j,k,1-i-j-k])
                    prediction_set = model_PID(train_set, w)

                    P = precision(prediction_set, test_set)
                    R = recall(prediction_set, test_set)
                    
                    F1 = F1_score(P, R)

                    out_line = str(w) + '  ' + str(P) + '  ' + str(R) + '  ' + str(F1) + '\n'
                    test_file.write(out_line)
                    c += 1
                    print c
    '''
    prediction_set = model_PID(train_set)

    P = precision(prediction_set, test_set)
    R = recall(prediction_set, test_set)
    F1 = F1_score(P, R)
    new_user = new_user(train_set, test_set)

    print 'user num = ' + str(user_count(user_brand))
    print 'brand num = ' + str(user_count(brand_user))
    print 'predict count = ' + str(user_count(prediction_set))
    print 'train set count = ' + str(user_count(train_set))
    print 'test_set count = ' + str(user_count(test_set))
    print 'user count = ' + str(user_predict_count(prediction_set, test_set))
    print 'new user = ' + str(len(new_user))

    u_p = user_predict_count(prediction_set, test_set) / float(user_count(prediction_set))
    print 'user precision = ' + str(u_p)
    print 'P  = ' + str(P)
    print 'R  = ' + str(R)
    print 'F1 = ' + str(F1_score(P, R))
    
