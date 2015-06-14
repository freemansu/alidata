#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/20
# Func:   数据可视化
# Python Version: 2.6.6

from preprocess import *
from train_test_set import *
from score import *
from statistics import *
from brand_model import *

import numpy as np
import math
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
zhfont = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/cjkuni-ukai/ukai.ttf')

# brand流行度图
# brand_pop在brand_model中生成
def brand_pop_plot(brand_pop):
    freq_user = {}

    for item in brand_pop:
        # 这里只截取购买次数小于30次的brand，这样看得清楚点
        if item[1] < 30 and item[1]>0:
            if freq_user.has_key(item[1]):
                freq_user[item[1]] += 1
            else:
                freq_user[item[1]] = 1

    x = freq_user.keys()
    y = [freq_user[k] for k in x]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x, y, 'o')

    ax.set_title(u'品牌流行度', fontproperties=zhfont)
    ax.set_xlabel(u'购买次数', fontproperties=zhfont)
    ax.set_ylabel(u'品牌数', fontproperties=zhfont)
    plt.savefig('../result/figures/brand_popularity.png')


# user活跃度图
def user_act_plot(user_act):
    user_buy = {}

    for item in user_act:
        if user_buy.has_key(item[1]):
            user_buy[item[1]] += 1
        else:
            user_buy[item[1]] = 1

    x = user_buy.keys()
    y = [user_buy[k] for k in x]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.plot(x, y, 'o')

    ax.set_title(u'用户活跃度', fontproperties=zhfont)
    ax.set_xlabel(u'购买次数', fontproperties=zhfont)
    ax.set_ylabel(u'用户数', fontproperties=zhfont)
    plt.savefig('../result/figures/user_activity.png')


# user活跃度与brand流行度之间的关系
def activity_popularity_plot(act_pop):
    x = [item[0] for item in act_pop]
    y = [item[1] for item in act_pop]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x, y, 'o')

    ax.set_title(u'用户活跃度与品牌流行度的关系', fontproperties=zhfont)
    ax.set_xlabel(u'用户活跃度', fontproperties=zhfont)
    ax.set_ylabel(u'品牌平均流行度', fontproperties=zhfont)
    plt.savefig('../result/figures/activity_popularity.png')


# 有购买行为的user数随时间的变化
def user_buy_date_plot(day_user):
    x = [day for day in range(len(day_user))]
    y = [day_user[i] for i in x]
    avg1 = [sum(y[0:30])/30.0] * 30
    avg2 = [sum(y[30:60])/30.0] * 30
    avg3 = [sum(y[60:90])/30.0] * 30
    avg4 = [sum(y[90:122])/32.0] * 32
    avgy = avg1 + avg2 +avg3 +avg4

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x, y, 'o')
    ax.plot(x, avgy)

    ax.set_title(u'有购买行为的用户数随时间变化', fontproperties=zhfont)
    ax.set_xlabel(u'时间', fontproperties=zhfont)
    ax.set_ylabel(u'用户数', fontproperties=zhfont)
    plt.savefig('../result/figures/user_buy_date.png')


# 有点击行为的user数随时间的变化
def user_click_date_plot(day_user):
    x = [day for day in range(len(day_user))]
    y = [day_user[i] for i in x]
    avg1 = [sum(y[0:30])/30.0] * 30
    avg2 = [sum(y[30:60])/30.0] * 30
    avg3 = [sum(y[60:90])/30.0] * 30
    avg4 = [sum(y[90:122])/32.0] * 32
    avgy = avg1 + avg2 +avg3 +avg4

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x, y, 'o')
    ax.plot(x, avgy)

    ax.set_title(u'有点击行为的用户数随时间变化', fontproperties=zhfont)
    ax.set_xlabel(u'时间', fontproperties=zhfont)
    ax.set_ylabel(u'用户数', fontproperties=zhfont)
    plt.savefig('../result/figures/user_click_date.png')


# 被购买的brand数随时间的变化
def brand_buy_date_plot(day_brand):
    x = [day for day in range(len(day_brand))]
    y = [day_brand[i] for i in x]
    avg1 = [sum(y[0:30])/30.0] * 30
    avg2 = [sum(y[30:60])/30.0] * 30
    avg3 = [sum(y[60:90])/30.0] * 30
    avg4 = [sum(y[90:122])/32.0] * 32
    avgy = avg1 + avg2 +avg3 +avg4

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x, y, 'o')
    ax.plot(x, avgy)

    ax.set_title(u'被购买的品牌数随时间变化', fontproperties=zhfont)
    ax.set_xlabel(u'时间', fontproperties=zhfont)
    ax.set_ylabel(u'品牌数', fontproperties=zhfont)
    plt.savefig('../result/figures/brand_buy_date.png')


# 被点击的brand数随时间的变化
def brand_click_date_plot(day_brand):
    x = [day for day in range(len(day_brand))]
    y = [day_brand[i] for i in x]
    avg1 = [sum(y[0:30])/30.0] * 30
    avg2 = [sum(y[30:60])/30.0] * 30
    avg3 = [sum(y[60:90])/30.0] * 30
    avg4 = [sum(y[90:122])/32.0] * 32
    avgy = avg1 + avg2 +avg3 +avg4
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x, y, 'o')
    ax.plot(x, avgy)

    ax.set_title(u'被点击的品牌数随时间变化', fontproperties=zhfont)
    ax.set_xlabel(u'时间', fontproperties=zhfont)
    ax.set_ylabel(u'品牌数', fontproperties=zhfont)
    plt.savefig('../result/figures/brand_click_date.png')
