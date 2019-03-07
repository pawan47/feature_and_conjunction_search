#!/usr/bin/env python
# coding: utf-8

# In[426]:


import numpy as np
import random
import cv2
import matplotlib.pyplot as plt


# In[427]:


def genMat(size):
    
    return np.array([[[255]*3]*size*10]*size*10)


# In[428]:


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


# In[429]:


red_tri = cv2.resize(cv2.cvtColor(cv2.imread('red_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_tri = cv2.resize(cv2.cvtColor(cv2.imread('blue_tri.png'), cv2.COLOR_BGR2RGB), (72, 72))
red_sqr = cv2.resize(cv2.cvtColor(cv2.imread('red_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))
blue_sqr = cv2.resize(cv2.cvtColor(cv2.imread('blue_sqr.png'), cv2.COLOR_BGR2RGB), (72, 72))


# In[431]:


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


# In[432]:


M, req_points = genFeatureSearchTemp(7, 72)


# In[433]:


# req_points ### first point is a triangle


# In[434]:


plt.imshow(M)

print('First point is a triangle and remaining are squares\n')

print(req_points)

plt.show()

# In[420]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




