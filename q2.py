#!/usr/bin/env python
# coding: utf-8

# In[437]:


import numpy as np
import random
import cv2
import matplotlib.pyplot as plt


# In[438]:


def genMat(size):
    
    return np.array([[[255]*3]*size*10]*size*10)


# In[439]:


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


# In[440]:


def trans(a):
    return .299*a[:,:,0] + .402*a[:,:,1] + .299*a[:,:,2]

def give_non_zero(mat):
    co = []
    for i in range(72):
        for j in range(72):
            if mat[i,j] > 0:
                co.append([i,j])
    return co

def detect_sq(image):
    g_kernel = cv2.getGaborKernel((8,8), 4.0, 0, 5, 0, 0)
    g_ = cv2.getGaborKernel((8,8), 4.0,np.pi/2 , 5, 0, 0)
    mj = cv2.filter2D(image,0, g_kernel)  * cv2.filter2D(image,0, g_)
    corner = give_non_zero(mj)
    return corner


def detect_tri(image):
    corners = []
    #================detect top corner====================
    h_ = cv2.getGaborKernel((9,9), 6.1,5*np.pi/6 , 8.9, 0, 0)
    g_ = cv2.getGaborKernel((9,9), 6.1,1*np.pi/6 , 8.9, 0, 0)

    mj =  (cv2.bitwise_not(cv2.filter2D(image, 0, h_)) * cv2.bitwise_not(cv2.filter2D(image, 0, g_)) )
    mj = mj.astype('uint8')
    top_corner = give_non_zero(mj)
    
    if len(top_corner) ==2:
        top_corner = top_corner[1]
    if len(top_corner) > 2:
        top_corner = []
    
    #==============detect side corners1===================
    
    i_ = cv2.getGaborKernel((9,9), 6,1*np.pi/2 , 7.1, 0, 0)
    g_ = cv2.getGaborKernel((9,9), 6.1,1*np.pi/6 , 8.9, 0, 0)

    mj =  (((cv2.filter2D(image, 0, i_)))* cv2.bitwise_not(cv2.filter2D(image, 0, g_))) /2
    mj = mj.astype('uint8')
    side_corner1 = give_non_zero(mj)
    
    if len(side_corner1) == 1:
        side_corner1 = side_corner1[0]
        
    #==============detect side corner2===================
    
    i_ = cv2.getGaborKernel((9,9), 6,1*np.pi/2 , 7.1, 0, 0)
    g_ = cv2.getGaborKernel((9,9), 6.1,5*np.pi/6 , 8.9, 0, 0)

    mj =  (((cv2.filter2D(image, 0, i_)))* cv2.bitwise_not(cv2.filter2D(image, 0, g_))) /2
    mj = mj.astype('uint8')
    side_corner2 = give_non_zero(mj)
    
    if len(side_corner2) == 1:
        side_corner2 = side_corner2[0]
    
    corner = [top_corner,side_corner1,side_corner2]
    return corner
        
def detect(image):
    im = trans(image)
    im = im.astype('uint8')
    img = cv2.resize(im,(72,72))
    sq_corner = detect_sq(img) 
    tri_corner = detect_tri(img)
    flag = 0
    if len(sq_corner)>0:
        flag = 1
        print('its a square')
        return flag,sq_corner
    elif len(tri_corner)>0:
        flag = 2
        print('its a triagle')
        return flag,tri_corner
    else:
        print('empty')
        return flag,[]

# ml = red_sqr



# plt.imshow(ml, cmap="gray")

# flag,corners = detect(ml)

# if flag == 1:
#     plt.title("Detected Square using gabor filter")

# if flag == 2:
#     plt.title("Detected triangle using gabor filter")


# In[441]:


def runFeatureSearch(M, req_points):
    for i in req_points:
        flag, corners = detect(M[i[0]:i[0]+72, i[1]:i[1]+72,:])
        
        if flag == 1:
            print('detected square at point', i)

        if flag == 2:
            print('detected triangle at point', i)
    
    


# In[442]:


def genFeatureSearchTemp(random_nums, size):
    req_points = []
    
    M = genMat(size)
    points = getPoints(random_nums, size)
    sel_list = random.sample(range(100), random_nums)
    
    x = points[sel_list[0]][0]
    y = points[sel_list[0]][1]
    
    req_points.append((x,y))

    M[x:x+72, y:y+72, :] = red_tri

    for i in sel_list[1:]:
        x = points[i][0]
        y = points[i][1]
        M[x:x+72, y:y+72] = red_sqr    
        req_points.append((x,y))
    
    return M, req_points


# In[443]:


red_tri = cv2.resize(cv2.cvtColor(cv2.imread('red_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_tri = cv2.resize(cv2.cvtColor(cv2.imread('blue_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
red_sqr = cv2.resize(cv2.cvtColor(cv2.imread('red_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_sqr = cv2.resize(cv2.cvtColor(cv2.imread('blue_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))


# In[450]:


M_feature, req_points = genFeatureSearchTemp(9, 72)


# In[ ]:


print('Choosing 9 points', 'First point is always a triangle')


# In[451]:


print("req_points", req_points, '\n') ### first point is a triangle


# In[453]:


runFeatureSearch(M_feature, req_points)

plt.imshow(M_feature)
plt.show()
# In[ ]:





# In[ ]:





# In[ ]:




