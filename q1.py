import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mping
import random 


# loading images
blue_tri = cv2.imread('blue_tri.png')[:,:,::-1]
blue_sqr = cv2.imread('blue_sqr.png')[:,:,::-1]
red_sqr = cv2.imread('red_sqr.png')[:,:,::-1]
red_tri = cv2.imread('red_tri.png')[:,:,::-1]

#function to transform image to a color independent(single channel)
def trans(a):

    return .299*a[:,:,0] + .402*a[:,:,1] + .299*a[:,:,2]

# generates base image for shapes
def give_non_zero(mat):
    co = []
    for i in range(72):
        for j in range(72):
            if mat[i,j] > 0:
                co.append([i,j])

    return co
#checks if list of list is empty or not for triangular case
def isListEmpty(inList):
    ll = np.array(inList)
    if len(ll[0]) ==0:

        return False
    else:

        return True
    
#Function to detect a square's corners    
def detect_sq(image):
    g_kernel = cv2.getGaborKernel((8,8), 4.0, 0, 5, 0, 0)
    g_ = cv2.getGaborKernel((8,8), 4.0,np.pi/2 , 5, 0, 0)
    mj = cv2.filter2D(image,0, g_kernel)  * cv2.filter2D(image,0, g_) #Getting the intersection points between the horizontal and vertical gabor filter results
    corner = give_non_zero(mj)

    return corner

#Function to detect a triangle's corners   
def detect_tri(image):
    corners = []
    #================detecting top corner====================
    h_ = cv2.getGaborKernel((9,9), 6.1,5*np.pi/6 , 8.9, 0, 0)
    g_ = cv2.getGaborKernel((9,9), 6.1,1*np.pi/6 , 8.9, 0, 0)

    mj =  (cv2.bitwise_not(cv2.filter2D(image, 0, h_)) * cv2.bitwise_not(cv2.filter2D(image, 0, g_))) #bitwise multiplication gives corners non-zero values 
    mj = mj.astype('uint8')
    top_corner = give_non_zero(mj)  #getting those non-zero corner points
    
    if len(top_corner) ==2:
        top_corner = top_corner[1]
    if len(top_corner) > 2:
        top_corner = []
    
    #==============detecting side corners1===================
    
    i_ = cv2.getGaborKernel((9,9), 6,1*np.pi/2 , 7.1, 0, 0)
    g_ = cv2.getGaborKernel((9,9), 6.1,1*np.pi/6 , 8.9, 0, 0)

    mj =  (((cv2.filter2D(image, 0, i_)))* cv2.bitwise_not(cv2.filter2D(image, 0, g_))) /2
    mj = mj.astype('uint8')
    side_corner1 = give_non_zero(mj)
    
    if len(side_corner1) == 1:
        side_corner1 = side_corner1[0]
        
    #==============detecting side corner2===================
    
    i_ = cv2.getGaborKernel((9,9), 6,1*np.pi/2 , 7.1, 0, 0)
    g_ = cv2.getGaborKernel((9,9), 6.1,5*np.pi/6 , 8.9, 0, 0)

    mj =  (((cv2.filter2D(image, 0, i_)))* cv2.bitwise_not(cv2.filter2D(image, 0, g_))) /2
    mj = mj.astype('uint8')
    side_corner2 = give_non_zero(mj)
    
    if len(side_corner2) == 1:
        side_corner2 = side_corner2[0]
    
    corner = [top_corner,side_corner1,side_corner2]

    return corner
        
#Function to detect if an image is a square or a triangle or a background
def detect(image):
    im = trans(image)                   #convert img to a single channel
    im = im.astype('uint8')
    img = cv2.resize(im,(72,72))        
    sq_corner = detect_sq(img)          #detecting square corners
    tri_corner = detect_tri(img)        #detecting triangle corners
    flag = 0
    if len(sq_corner)>0:
        flag = 1
        print('its a square')

        return flag,sq_corner
    elif isListEmpty(tri_corner):
        flag = 2
        print('its a triagle')

        return flag,tri_corner
    else:
        print('empty')

        return flag,[]

# background image
back = np.array([[[255]*3]*72]*72)

chec = [blue_sqr,blue_tri,red_sqr,red_tri,back] #back stands for background image


# running for some images which contains square, traingle and  background
random.shuffle(chec)
for i in range(5):

    ml = chec[i]

    plt.imshow(ml)

    flag, corners = detect(ml)

    if flag == 1:
        plt.title("Detected a square using gabor filter")

    if flag == 2:

        plt.title("Detected a triangle using gabor filter")

    if flag == 0:
        plt.title("Nothing is Detected --background ")

    plt.show()


