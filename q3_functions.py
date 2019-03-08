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


def genMat(size):
	
	return np.array([[[255]*3]*size*10]*size*10)


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




def shape_map_f(M, req_points):
	

	for i in req_points:
		flag, corners = detect(M[i[0]:i[0]+72, i[1]:i[1]+72,:])
		if flag == 1:
			#print('detected triangle at point', i)
			break


def color_map_f(M, req_points):
	for i in req_points:
		
		flag = detect_col(M[i[0]:i[0]+72, i[1]:i[1]+72,:])
		if flag == 1:
			#print('blue color detected at point',i)
			break




def genFeature(random_nums, size=72,in_shape = True,in_col = False):
	req_points = []
	
	M = genMat(size)

	points = getPoints(random_nums, size)
	sel_list = random.sample(range(100), random_nums)
	
	x = points[sel_list[0]][0]
	y = points[sel_list[0]][1]
	
	req_points.append((x,y))
	dec = .6
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

	
	return M, req_points,in_col



red_tri = cv2.resize(cv2.cvtColor(cv2.imread('red_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_tri = cv2.resize(cv2.cvtColor(cv2.imread('blue_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
red_sqr = cv2.resize(cv2.cvtColor(cv2.imread('red_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_sqr = cv2.resize(cv2.cvtColor(cv2.imread('blue_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))



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


# In[16]:


def shape_map(M, req_points):
	flags = []
	for i in req_points:
		flag, corners = detect(M[i[0]:i[0]+72, i[1]:i[1]+72,:])
		
		if flag == 0:
			flags.append(0)

		if flag == 1:
			flags.append(1)
	return flags




def color_map(M, req_points):
	flags =[]
	for i in req_points:
		
		flag = detect_col(M[i[0]:i[0]+72, i[1]:i[1]+72,:])

		if flag == 0:
			flags.append(0)
		if flag == 1:
			flags.append(1)
	return flags



def conjucmake(random_nums, size=72,shape_odd = 0,color_odd = 0):  # 0 == red  0 == square,
	
	req_points = []
	
	M = genMat(size)

	points = getPoints(random_nums, size)
	sel_list = random.sample(range(100), random_nums)
	
	x,y = points[sel_list.pop()]
	req_points.append((x,y))
	
	
	M[x:x+72, y:y+72] = make_shape(shape_odd,color_odd)
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
	
	return M,req_points
	


def runconj(M,req_points_,shape_odd = 0,color_odd = 0):
	random.shuffle(req_points_ )
	shape_flag = shape_map(M,req_points_)
	color_flag = color_map(M,req_points_)
	
	
	for i in range(len(shape_flag)):
		time.sleep(0.035)

		if shape_flag[i] == shape_odd:
			if color_flag[i] ==color_odd:

				break
	
	if shape_odd == 0:
		if color_odd ==0:
			k = 'Red Square'
		else:
			k = 'Blue Square'
	else:
		if color_odd == 0:
			k = 'Red Triangle'
		else:
			k = 'Blue Triangle'

	#print(k,'is detected at',req_points_[i])
		