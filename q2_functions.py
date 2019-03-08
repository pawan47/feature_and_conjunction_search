#!/usr/bin/env python
# coding: utf-8


import numpy as np
import random
import cv2
import matplotlib.pyplot as plt
from detect import detect
from detect_col import detect_col
import random

# generate base image

def genMat(size):
    
    return np.array([[[255]*3]*size*10]*size*10)

#generate random points for experiments

def getPoints(random_nums, size):
    points = []
    x = 0
    t = [x]
    for i in range(9):
        x = x + size
        t.append(x)
    for i in t:
        for j in t:
            points.append((i, j))
            
    return points


# shape map for feature search

def shape_map_f(M, req_points):
    
    x_ = []
    y_ = []
    for i in req_points:
        flag, corners = detect(M[i[0]:i[0]+72, i[1]:i[1]+72,:])
        
        if flag == 0:
            print('detected square at frame', i, (i[0], i[1] + 72), (i[0] + 72, i[1]), (i[0] + 72, i[1] + 72))
            x_.append([i[1]+36, i[0] + 36])
            # plt.scatter(i[1]+36, i[0] + 36, c = 'r', label = 'square', marker = 's')

        elif flag == 1:
            print('detected triangle at frame', i, (i[0], i[1] + 72), (i[0] + 72, i[1]), (i[0] + 72, i[1] + 72))
            y_.append([i[1]+36, i[0] + 36])
            # plt.scatter(i[1]+36, i[0] + 36, c = 'b', label = 'triangle', marker = '^')
        else:
            print('detected background at frmae', i, (i[0], i[1] + 72), (i[0] + 72, i[1]), (i[0] + 72, i[1] + 72))

    plt.scatter(*zip(*x_), c = 'r', label = 'square', marker = 's')
    plt.scatter(*zip(*y_), c = 'b', label = 'triangle', marker = '^')
    # plt.savefig('fig5.jpg')



# color map for feature search

def color_map_f(M, req_points):
    for i in req_points:
        
        flag = detect_col(M[i[0]:i[0]+72, i[1]:i[1]+72,:])

        if flag == 0:
            print('red color detected at frame',i, (i[0], i[1] + 72), (i[0] + 72, i[1]), (i[0] + 72, i[1] + 72))
        if flag == 1:
            print('blue color detected at frame',i, (i[0], i[1] + 72), (i[0] + 72, i[1]), (i[0] + 72, i[1] + 72))



# generate image containg different shape of color for feature search

def genFeature(random_nums, size=72,in_shape = True,in_col = False):
    req_points = []
    
    M = genMat(size)

    points = getPoints(random_nums, size)
    sel_list = random.sample(range(100), random_nums)
    
    x = points[sel_list[0]][0]
    y = points[sel_list[0]][1]
    
    req_points.append((x,y))
    dec = random.uniform(0,1)
    if in_shape == True:
        if dec >.5:
            M[x:x+72, y:y+72, :] = red_tri
            for i in sel_list[1:]:
                x = points[i][0]
                y = points[i][1]
                M[x:x+72, y:y+72] = red_sqr    
                req_points.append((x,y))
        else:
            M[x:x+72, y:y+72, :] = blue_tri
            for i in sel_list[1:]:
                x = points[i][0]
                y = points[i][1]
                M[x:x+72, y:y+72] = blue_sqr  
                req_points.append((x,y))

    if in_col == True:
        if dec > .5:
            M[x:x+72, y:y+72, :] = blue_sqr
            for i in sel_list[1:]:
                x = points[i][0]
                y = points[i][1]
                M[x:x+72, y:y+72] = red_sqr    
                req_points.append((x,y))
        else:
            M[x:x+72, y:y+72, :] = red_tri
            for i in sel_list[1:]:
                x = points[i][0]
                y = points[i][1]
                M[x:x+72, y:y+72] = blue_tri 
                req_points.append((x,y))
            #make an thresholding function

    # plt.imshow(M)
    # plt.savefig('fig4.jpg')

    return M, req_points,in_col


# In[12]:


red_tri = cv2.resize(cv2.cvtColor(cv2.imread('red_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_tri = cv2.resize(cv2.cvtColor(cv2.imread('blue_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
red_sqr = cv2.resize(cv2.cvtColor(cv2.imread('red_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_sqr = cv2.resize(cv2.cvtColor(cv2.imread('blue_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))



# making shape of different color for conjucture search 

def make_shape(shape_odd,color_odd):
    if shape_odd == 0:
        if color_odd ==0:
            return red_sqr
        else:
            return blue_sqr
    else:
        if color_odd == 0:
            return red_tri
        else:
            return blue_tri


# shape map for conjucture search 

def shape_map(M, req_points):
    flags = []
    for i in req_points:
        flag, corners = detect(M[i[0]:i[0]+72, i[1]:i[1]+72,:])
        
        if flag == 0:
            flags.append(0)

        if flag == 1:
            flags.append(1)
    return flags


# color map for conjucture map

def color_map(M, req_points):
    flags =[]
    for i in req_points:
        
        flag = detect_col(M[i[0]:i[0]+72, i[1]:i[1]+72,:])

        if flag == 0:
            flags.append(0)
        if flag == 1:
            flags.append(1)
    return flags


# making image for conjucture search

def conjucmake(random_nums, size=72,shape_odd = 0,color_odd = 0):  # 0 == red  0 == square,
    
    req_points = []
    
    M = genMat(size)

    points = getPoints(random_nums, size)
    sel_list = random.sample(range(100), random_nums)
    
    x,y = points[sel_list.pop()]
    req_points.append((x,y))
    # r, s = x, y
    
    M[x:x+72, y:y+72] = make_shape(shape_odd,color_odd)
    plt.scatter(y+36, x+36, c = 'r', label = 'square', marker = 's')
    #print(shape_odd,color_odd)
    
    random_nums -=1
    kk = int(random_nums/2)
    k = random.randint(0,kk)
    
    random_nums -= k
    #print(k)
    #print(sel_list)
    
    for i in range(k):
        pp = sel_list.pop()
        x,y = points[pp]
        M[x:x+72, y:y+72] = make_shape(shape_odd,1 -color_odd)
        #print(1-shape_odd,color_odd)
        req_points.append((x,y))
    
    
    
    
    
    k = random.randint(0,random_nums)
    #print(k)
    for i in range(k):
        pp = sel_list.pop()
        x,y = points[pp]
        M[x:x+72, y:y+72] = make_shape(1-shape_odd,1-color_odd)
        #print(shape_odd,color_odd)
        req_points.append((x,y))
        
    #print(random_nums)
    for i in range(k,random_nums):
        pp = sel_list.pop()
        x,y = points[pp]
        M[x:x+72, y:y+72] = make_shape(1-shape_odd,color_odd)
        #print(1-shape_odd,color_odd)
        req_points.append((x,y))

    # plt.imshow(M)
    # plt.savefig('fig6.jpg')    
    # plt.scatter(s+36, r+36, c = 'r', label = 'square', marker = 's')
    # plt.savefig('fig7.jpg')

    return M,req_points
    


def runconj(M,req_points_):
    
    shape_flag = shape_map(M,req_points_) # making shape map for the image
    color_flag = color_map(M,req_points_) # making color map for the image
    dete = []
    
    for i in range(len(shape_flag)):
        if shape_flag[i] == 0:
            k = 'red'
        else:
            k='blue'
        if color_flag[i] ==0:
            k += ' square'
        else:
            k += ' triangle'

        tu = req_points_[i]
        print(k,'is detected at frame', tu, (tu[0], tu[1] + 72), (tu[0] + 72, tu[1]), (tu[0] + 72, tu[1] + 72))
        dete.append(k)







