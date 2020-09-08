#!/usr/bin/env python

import sys
import numpy as np
import cv2
import time
import serial
import ctypes

from pylepton import Lepton
from PIL import Image
from smbus2 import SMBus
 

# Function returns one picture frame with normalized value
def capture(flip_v = False, device = "/dev/spidev0.0"):
    with Lepton(device) as l:
        a,_ = l.capture()
    if flip_v:
        cv2.flip(a,0,a)
    cv2.normalize(a, a, 0, 255, cv2.NORM_MINMAX) #Normalization of data
    print(a)
    return np.uint8(a)


while True:
    image = capture()
    w, h = 80, 60
    data = np.zeros((h, w, 3), dtype=np.uint8)

    #Tresholding image data
    thre_val = 130
    max_val = 255
    ret,thresh1 = cv2.threshold(image,thre_val,max_val,cv2.THRESH_TOZERO)
    #Creation of binary mask
    for hei in range(0,60):
        for wid in range(0,80):
            if thresh1[hei][wid] > 130 :
                thresh1[hei][wid] = 255
                data[hei,wid]=[0,255,0]
            else:
                thresh1[hei][wid] = 0
                data[hei,wid]=[0,0,0]

    # Find contours
    countours = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    # If at least one contour was found
    if len(countours) > 0:
        # Find the largest contour
        c = max(countours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        #If radius is bigger then treshold
        if radius > 3:
            cv2.circle(data, center, 2, (0, 0, 255), -1) #Show center of object

            
    dim = (640, 480)
    resized = cv2.resize(data, dim)
    #Resized picture for better view
    cv2.imshow("Termokamera",resized)
    cv2.waitKey(100)
