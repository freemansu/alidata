#!/usr/bin/env python
# coding: utf-8
# Author: suyu
# Date:   2014/03/16
# Func:   实现兴趣度模型(PID)
# Python Version: 2.6.6

from preprocess import *
from statistics import *
from user_model import *

import numpy as np

# 实现矩阵补全方法
def model_MC(user_record):
    brand_record = transform(user_record)
    
    # 4种action的权重
    w = np.array([0.06, 0.32, 0.30, 0.32])
    
    user_ids = sorted(user_record.keys())
    brand_ids = brand_ids = sorted(brand_record.keys())

    # action_矩阵
    (A0, A1, A2, A3) = action_matrixs(user_record)
    A = A0*w[0] + A1*w[1] + A2*w[2] + A3*w[3]

    #use LMaFit to complete the low-rank and sparse matrix A
    

    # 估计矩阵A的秩rank, 改估计不会影响最终结果，但会影响计算时间
    rank = 30


