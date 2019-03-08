#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
import cv2
import matplotlib.pyplot as plt
from detect import detect
from detect_col import detect_col
import random
import time
from q3_functions import *



def q2_para(type_=0,rand_point = 90): #0 = feature
    
    if type_ == 0:
        plt.title('Feature Search')
        M_feature, req_points,in_col = genFeature(rand_point, 72,True,False)
        
        random.shuffle(req_points)

        ti = time.time()
        if in_col == False:
            shape_map_f(M_feature, req_points)
        else:
            color_map_f(M_feature, req_points)
    else:
        plt.title('Conjunction Search')
        shape_odd_ = 0 #square
        color_odd_ = 0 #redwww
        Mm,req_points = conjucmake(rand_point, shape_odd = shape_odd_, color_odd = color_odd_)

        ti = time.time()
        runconj(Mm,req_points, shape_odd = shape_odd_, color_odd = color_odd_)
    return ti
        



xx = [5*(i+1) for i in range(10)]
fet = []
con = []
for i in xx:
    p = 0
    for _ in range(20):
        st = q2_para(0,i)
        p += time.time() - st
    p = p/20
    fet.append(p)
    p=0
    for _ in range(20):
        st = q2_para(1,i)
        p += time.time() -st
    p = p/20
    con.append(p)
    print(i)

print(fet,con)
plt.plot(fet,xx)
plt.plot(con,xx)
plt.show()

