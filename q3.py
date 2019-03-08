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
from q3_functions import *    # contains fucntions for Q3



def q2_para(type_=0,rand_point = 90): #0 = feature search 1 = conjucture search 
    
    if type_ == 0:
        plt.title('Feature Search')
        M_feature, req_points,in_col = genFeature(rand_point, 72,True,False)  # make a image for feature search
        
        random.shuffle(req_points)

        ti = time.time()         # start time for beacause it will start searching for the feature now
        if in_col == False:
            shape_map_f(M_feature, req_points)    # if it is a shape featrue search 
        else:
            color_map_f(M_feature, req_points)   # if it is a color feature search
    else:
        plt.title('Conjunction Search')
        shape_odd_ = 0 #square                   # choose shapefor odd feature, 0 == square,1 == triangle 
        color_odd_ = 0 #redwww                   # choose color for odd feature, 0 == red, 1 == Blue
        Mm,req_points = conjucmake(rand_point, shape_odd = shape_odd_, color_odd = color_odd_)  # making image for the conjunction search

        ti = time.time()
        runconj(Mm,req_points, shape_odd = shape_odd_, color_odd = color_odd_) # running conjuction search
    return ti
        

# it will run feature search and conjuction search in i no of shape for 20 times and takes its average


xx = [5*(i+1) for i in range(10)]
fet = []
con = []
for i in xx:
    p = 0
    for _ in range(20):
        st = q2_para(0,i)           # feature search in i no of objects
        p += time.time() - st
    p = p/20                        ## takes average
    fet.append(p)
    p=0
    for _ in range(20):
        st = q2_para(1,i)         # conjuctuin search in i no of objects
        p += time.time() -st
    p = p/20
    con.append(p)
    print(i)
#plot graphs
plt.plot(xx, fet, 'r-', label = 'Feature Search')
plt.plot(xx, con, 'b-', label = 'Conjunction Search')
plt.legend()
plt.show()
