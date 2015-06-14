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
import numpy as np
import sys
import datetime
def repeat(user_brand):
    repeat_user={}
    repeat_buy={}

    u_b_a = user_brand_action_count(user_brand)
    for us in u_b_a.keys():
        for brand in u_b_a[us]:
            if u_b_a[us][brand][1]>=2:
                repeat_user.setdefault(brand, [0,0,0])[0]+=1
                repeat_user.setdefault(brand, [0,0,0])[1]+=1
            elif u_b_a[us][brand][1]==1:
                repeat_user.setdefault(brand, [0,0,0])[1]+=1
    for brand in repeat_user.keys():
        repeat_user[brand][2]=1.0*repeat_user[brand][0]/repeat_user[brand][1]

    for us in u_b_a.keys():
        for brand in u_b_a[us]:
            if u_b_a[us][brand][1]>=2:
                repeat_buy.setdefault(brand, [0,0,0])[0]+=(u_b_a[us][brand][1]-1)
                repeat_buy.setdefault(brand, [0,0,0])[1]+=u_b_a[us][brand][1]
            elif u_b_a[us][brand][1]==1:
                repeat_buy.setdefault(brand, [0,0,0])[1]+=1
    for brand in repeat_buy.keys():
        repeat_buy[brand][2]=1.0*repeat_buy[brand][0]/repeat_buy[brand][1]

    print len(repeat_user),repeat_user
    print len(repeat_buy),repeat_buy
if __name__ == '__main__':


    input_file=open('original_data.csv','r')
    user_brand,brand_user,counts=read(input_file)
    repeat(user_brand)