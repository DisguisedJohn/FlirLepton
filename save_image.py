#!/usr/bin/env python
import os
import sys
import numpy as np
import cv2
import time
import serial
import ctypes

from pylepton import Lepton
from PIL import Image
 
# Function returns one picture frame with normalized value
def capture(flip_v = False, device = "/dev/spidev0.0"):
    with Lepton(device) as l:
        a,_ = l.capture()
    if flip_v:
        cv2.flip(a,0,a)
    cv2.normalize(a, a, 0, 255, cv2.NORM_MINMAX) #Normalization of data
   #print(a)
    return np.uint8(a)


image = capture()
            
dim = (640, 480)
resized = cv2.resize(image, dim)
#Resized picture for better view
 
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = timestr + ".jpg"

cv2.imwrite(filename, image)
print('Image saved. Press any key to continue...')
cv2.waitKey(0)
