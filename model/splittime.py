#!/usr/bin/env python
# coding: utf-8
# Author: liuhuimin
# Date:   2014/03/16
# Func:   main 
# Python Version: 2.6.6


from preprocess import *
from train_test_set import *
from score import *
from statistics import *
from lastweek import *
import numpy as np
import sys
import datetime
def timesplit(brand_user,distance):#distance表示时间间隔
    M=brand_count(brand_user)
    N=(datetime.datetime(2013,8,16)-datetime.datetime(2013,4,14)).days
    print N,'天'
    brand_time={}
    for brand in brand_user.keys():
        brand_time[brand]=[0 for i in range(N)]#最后一位是总数
        for data in brand_user[brand]:
            if data[1]==0 or data[1]==1:
                num=(data[2]-datetime.datetime(2013,4,15)).days
                brand_time[brand][num]+=1
                brand_time[brand][N-1]+=1
    for brand in brand_time.keys():
            if brand_time[brand][N-1]==0:
                del brand_time[brand]
    #print brand_time
    #因为时间间隔不一定正好，所以从最后往前划分，导致最前面的时间可能不够时间间隔的长度
    longth=(N-1)/distance+1
    brand_split_count={}#按时间跨度数量统计
    brand_split_percent={}#按时间跨度百分比统计
    for brand in brand_time.keys():
        brand_split_count[brand]=[0 for i in range((N-1)/distance+1)]
        brand_split_percent[brand]=[0 for i in range((N-1)/distance+1)]
        for i in range((N-1)/distance+1)[::-1]:
            #print 'i:',i
            for j in range(distance)[::-1]:
                num=N-2-j-distance*((N-1)/distance-i)
                if num>=0:
                    brand_split_count[brand][i]+=brand_time[brand][num]
            brand_split_percent[brand][i]=1.0*brand_split_count[brand][i]/brand_time[brand][N-1]
    return brand_split_count,brand_split_percent,longth

def click_num_notbuy(brand_user):
    brand_action=brand_action_count(brand_user)
    brand_clicknum_notbuy=[]
    for brand in brand_action.keys():
        if brand_action[brand][1]==0:
            if brand_action[brand][0]>=100:
                    brand_clicknum_notbuy.append(brand)
                #brand_clicknum_notbuy.append([brand,brand_action[brand][0],brand_action[brand][1]])
    #brand_clicknum_notbuy=sorted(brand_clicknum_notbuy, key=lambda student: student[1],reverse=True) 
    return brand_clicknum_notbuy


def sub_set(brand_user,distance,precent,count):
    brand_split_count,brand_split_percent,longth=timesplit(brand_user,distance)
    sub_brand=[]
    for brand in brand_split_percent.keys():
        if brand_split_percent[brand][longth-1]<=precent and brand_split_count[brand][longth-1]<=count:
            sub_brand.append(brand)         
    return sub_brand
def subtract(prediction_set,sub_brand):
    prenum=0
    for us in prediction_set.keys():
        prenum+=len(prediction_set[us])
    for us in prediction_set.keys():
        listtmp=[val for val in prediction_set[us] if val not in sub_brand]
        if listtmp:
            prediction_set[us]=listtmp
        else:
            del prediction_set[us]
    afternum=0
    for us in prediction_set.keys():
        afternum+=len(prediction_set[us])
    return prediction_set,prenum-afternum
def combine(prediction_set,lastweek):
    count=0
    for us in lastweek.keys():
        if not prediction_set.has_key(us):
            prediction_set[us]=[]
        for brand in lastweek[us]:
            if brand not in prediction_set[us]:
                prediction_set[us].append(brand)
                count+=1
    return prediction_set,count


def get_click_pop_brand_user(user_brand):
    add_user={}
    datet=datetime.datetime(2013,7,15)
    for us in user_brand.keys():
        for brand in user_brand[us]:
            if brand[0]==7868 and brand[2]>datet:
                add_user.setdefault(us, []).append(7868)
            if brand[0]==11196 and brand[2]>datet:
                add_user.setdefault(us, []).append(11196)
            if brand[0]==2683 and brand[2]>datet:
                add_user.setdefault(us, []).append(2683)
            if brand[0]==27791 and brand[2]>datet:
                add_user.setdefault(us, []).append(27791)
            if brand[0]==8689 and brand[2]>datet:
                add_user.setdefault(us, []).append(8689)
    return add_user

def findregular(user_brand):
    datea=datetime.datetime(2013,5,1)
    dateb=datetime.datetime(2013,7,31)
    brand4=[]
    brand8=[]
    for us in user_brand.keys():
        for brand in user_brand[us]:
            if brand[1]==1 and brand[2]<datea:
                if brand[0] not in brand4:
                    brand4.append(brand[0])
    for us in user_brand.keys():
        for brand in user_brand[us]:
            if brand[1]==1 and brand[2]>dateb:
                if brand[0] not in brand8:
                    brand8.append(brand[0])
    brandregular=[val for val in brand4 if val in brand8]
    return brandregular
def del_user_brand(prediction_set ,del_brand):
    prenum=0
    for us in prediction_set.keys():
        prenum+=len(prediction_set[us])

    for us in prediction_set.keys():
        if del_brand.has_key(us):
            listtmp=[val for val in prediction_set[us] if val not in del_brand[us]]
            if listtmp:
                prediction_set[us]=listtmp
            else:
                del prediction_set[us]
    
    afternum=0
    for us in prediction_set.keys():
        afternum+=len(prediction_set[us])
    return prediction_set,prenum-afternum
if __name__ == '__main__':


    input_file=open('../dataset/original_data.csv','r')
    user_brand,brand_user,counts=read(input_file)
    #print brand_split_count,brand_split_percent
    buynotclick=0
    u_b_a = user_brand_action_count(user_brand)
    for us in u_b_a:
        for brand in u_b_a[us]:
            if u_b_a[us][brand][0]<=0 and u_b_a[us][brand][1]>0:
                buynotclick+=1

    print 'count buy not click',buynotclick




    lastweek=getlastweek(user_brand)
    #未处理预测结果文件
    predictfile=open('../result/predict_PID.txt','r')
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
    predictnum=0
    for us in prediction_set.keys():
        predictnum+=len(prediction_set[us])
    print 'previous predict num',predictnum
    #brand_clicknum_notbuy=click_num_notbuy(brand_user)
    #print brand_clicknum_notbuy
    add_user=get_click_pop_brand_user(user_brand)
    #print add_user
    sub_brand=sub_set(brand_user, 30, 0, 1000)
    #减去最后一个月没浏览的数据
    prediction_set,subnum=subtract(prediction_set, sub_brand)
    print 'subnum which is not exist in the last month:',subnum
    #合并最后几天浏览的数据
    prediction_set,count = combine(prediction_set,lastweek)
    print 'conbine lastweek data:',count
    #合并最后20天购买的品牌数据
    #last_month=get_lastmonth(user_brand)
   # prediction_set,count = combine(prediction_set,last_month)
    #print 'conbine last_month buy data',count
    #减去点击数最多但没有购买过的商品
    #prediction_set,subnum=subtract(prediction_set, brand_clicknum_notbuy)
    #print 'click_notbuy:',subnum
    
    #为浏览过最流行购买品牌的用户添加最流行品牌
    prediction_set,count = combine(prediction_set,add_user)
    print 'popular brand add:',count
    #写文件，最终预测结果
    brandregular=findregular(user_brand)
    #print brandregular

    user_brand23=get23(user_brand)
    prediction_set,count=combine(prediction_set, user_brand23)
    print 'add 23 action',count


    predictnum=0
    for us in prediction_set.keys():
        predictnum+=len(prediction_set[us])
    print 'all predict num',predictnum
    prediction_file = open('../result/predict_final.txt', 'w')
    for user in prediction_set.keys():
        prediction_line = str(user) + '\t' + str(prediction_set[user][0])
        for brand in prediction_set[user]:
            if not brand == prediction_set[user][0]:
                prediction_line += ',' + str(brand)
        prediction_line += '\n'
        prediction_file.write(prediction_line)
    prediction_file.close()
    predictfile.close()
    input_file.close()

    
