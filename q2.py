#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
import cv2
import matplotlib.pyplot as plt
from detect import detect
from detect_col import detect_col
import random

from q2_functions import *



def q2_para(type_=0,rand_point = 90): #0 = feature
    
    if type_ == 0:
        plt.title('Feature Search')
        M_feature, req_points,in_col = genFeature(rand_point, 72,True,False)
        print('ppp')
        if in_col == False:
            shape_map_f(M_feature, req_points)
        else:
            color_map_f(M_feature, req_points)
        plt.imshow(M_feature)
        plt.legend()
        plt.show()
    else:
        plt.title('Conjunction Search')
        shape_odd_ = 0 #square
        color_odd_ = 0 #redwww
        Mm,req_points = conjucmake(rand_point, shape_odd = shape_odd_, color_odd = color_odd_)
        runconj(Mm,req_points)
        plt.imshow(Mm)
        plt.show()
        
while True:

	choice = int(input('enter 0 for Feature Search, 1 for Conjunction Search and 2 to exit\n')) # 0,1,2=exit
	rand_point = int(input('enter the number of points. This number should not be more than 100\n'))
	if choice == 2:
		break
	q2_para(choice,rand_point)


# import time
# st = time.time()
#q2_para(0)
# print(st-time.time())
# st = time.time()
#q2_para(1)
# print(st-time.time())

