import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mping

def threshold(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)[1]

def detect_col(image):
    image = image.astype('uint8')
    imm = cv2.bitwise_not(cv2.resize(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY),(72,72)))
    imm = cv2.threshold(imm,180,255,cv2.THRESH_BINARY)[1]
    k = np.sum(imm)
    if k > 10: #flag 1  for blue
        return 1
    else:
        return 0
