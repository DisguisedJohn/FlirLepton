#!/usr/bin/env python

import sys
import numpy as np
import cv2
import time
import ctypes

from pylepton import Lepton
from PIL import Image
from smbus2 import SMBus

def capture(flip_v = True, device = "/dev/spidev0.1"):
    with Lepton(device) as l:
        a,_ = l.capture()
    if flip_v:
        cv2.flip(a,0,a)

    # When AGC is disable, no need to use normalization and shift because raw data are 8bit
    #cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
    #np.right_shift(a, 8, a)

    return np.uint8(a)

while True:
    image = capture()

    # # Creating RGB picture (ish) >> Not used but can be used for picture saving
    # w, h = 80, 60
    # data = np.zeros((h, w, 3), dtype=np.uint8)
    # for row in range(0,60):
    #     for collumn in range(0,80):
    #         data[row,collumn] = [image[row,collumn], image[row,collumn], image[row,collumn]]

    # # Creating, showing and saving image froma camera
    # img = Image.fromarray(data, 'RGB')
    # img.save('image2.png')
    # img.show()

    # Tresholding values in image and denoising
    thre_val = 130
    max_val = 255

        # Simple threshold
    ret,thresh1 = cv2.threshold(image,thre_val,max_val,cv2.THRESH_TOZERO)

    #     # Adaptive treshold
    # thresh2 = cv2.adaptiveThreshold(resized2, max_val, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 3)

    #     # Denoise
    # denoise = cv2.fastNlMeansDenoising(thresh1,0.1,3,3)

# OBJECT DETECTION #

   # Basically transforming raw 8bit data to HSL 
   # when if raw data value is higher than some value it will be maxed etc.
   # used for object detection cause OD is using HSL masks
   for hei in range(0,60):
       for wid in range(0,80):
           if thresh1[hei][wid] > 130:
               thresh1[hei][wid] = 255
               data[hei,wid]=[0,0,100]
           else:
               thresh1[hei][wid] = 0
               data[hei,wid]=[0,0,0]

    # Mask boundaries setup (should be useless because of manual normalization to [0,0,100])
   lower = np.array([0,0,80])
   upper = np.array([0,0,100])

    # Creating mask
   mask = cv2.inRange(data, lower, upper)
   mask = cv2.erode(mask, None, iterations=2)
   mask = cv2.dilate(mask, None, iterations=2)

    # Contour finding           
   # find contours in the mask and initialize the current
   # (x, y) center of the ball
   cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
   center = None
   
   # only proceed if at least one contour was found
   if len(cnts) > 0:
       # find the largest contour in the mask, then use
       # it to compute the minimum enclosing circle and
       # centroid
       c = max(cnts, key=cv2.contourArea)
       ((x, y), radius) = cv2.minEnclosingCircle(c)
       M = cv2.moments(c)
       center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
       
       # only proceed if the radius meets a minimum size
       if radius > 3:
           # draw the circle and centroid on the frame,
           # then update the list of tracked points
#            cv2.circle(data, (int(x), int(y)), int(radius),
#                (0, 255, 255), 2)
           cv2.circle(data, center, 5, (0, 255, 0), -1)



    # Resizing generated image for better debugging and better picture
   dim = (640, 480)
   resized = cv2.resize(data, dim)

    cv2.imshow("Termokamera s detekci objektu", resized)
    cv2.waitKey(100)
