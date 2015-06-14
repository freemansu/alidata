#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/20
# Func:   测试驱动 
# Python Version: 2.6.6


from preprocess import *
from train_test_set import *
from score import *
from statistics import *
from model_PID import *
from brand_model import *
from user_model import *
from user_brand_model import *
from visualization import *

if __name__ == '__main__':

    input_file = open('../dataset/original_data.csv', 'r')
    

    user_brand, brand_user, counts = read(input_file)

    brand_pop = brand_popularity(brand_user)
    brand_pop_plot(brand_pop)


    user_act = user_activity(user_brand)
    user_act_plot(user_act)


    act_pop = activity_popularity(user_brand, brand_user)
    activity_popularity_plot(act_pop)


    day_user_buy = user_buy_date(user_brand)
    user_buy_date_plot(day_user_buy)


    day_user_click = user_click_date(user_brand)
    user_click_date_plot(day_user_click)
    
    day_brand_buy = brand_buy_date(brand_user, user_brand)
    brand_buy_date_plot(day_brand_buy)

    day_brand_click = brand_click_date(brand_user, user_brand)
    brand_click_date_plot(day_brand_click)
    '''
    print 'predict count = ' + str(user_count(prediction_set))
    print 'test_set count = ' + str(user_count(test_set))
    print 'user count = ' + str(user_predict_count(prediction_set, test_set))
    
    u_p = user_predict_count(prediction_set, test_set) / float(user_count(prediction_set))
    print 'user precision = ' + str(u_p)
    print 'P  = ' + str(P)
    print 'R  = ' + str(R)
    print 'F1 = ' + str(F1_score(P, R))
    '''
