import cv2
import numpy as np
from functions import *


# Defining default ranges for colour values
blue = np.array([[88,78,20],[128,255,255]])
yellow = np.array([[21,70,80],[61,255,255]])
red = np.array([[154, 85, 72],[185, 255, 255]])


# Begin
cap = cv2.VideoCapture(0)
print("=======================================================")
print("              In calibration mode.")
print(" Use trackbars to calibrate press space when done")
print("           Press D for default settings")
print("=======================================================")

yellow = calibration('Yellow', yellow, cap)
blue = calibration('Blue', blue, cap)
red = calibration('Red', red, cap)

print("Calibration Successfull!!")
cv2.namedWindow('Frame')
