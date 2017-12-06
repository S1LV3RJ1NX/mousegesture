import cv2
import numpy as np
from functions import *


# Defining default ranges for colour values
blue = np.array([[88,78,20],[128,255,255]])
yellow = np.array([[21,70,80],[61,255,255]])
red = np.array([[154, 85, 72],[185, 255, 255]])

# Status variables
perform = False
showCentroid = False

def changeStatus(key):
    global perform
    global showCentroid
    global yellow, red, blue

    if key == ord('p'):
        perform = not perform
        if perform:
            print("Mouse simulation ON..")
        else:
            print("Mouse simulation OFF")

    elif key == ord('c'):
        showCentroid = not showCentroid
        if showCentroid:
            print("Showing Cenroid")
        else:
            print("Not showing Centroid")

    elif key == ord('r'):
        print("=======================================================")
        print("              In recalibration mode.")
        print(" Use trackbars to calibrate press space when done")
        print("           Press D for default settings")
        print("=======================================================")

        yellow = calibration('Yellow', yellow, cap)
        blue = calibration('Blue', blue, cap)
        red = calibration('Red', red, cap)

    else:
        pass


# Begin
cap = cv2.VideoCapture(0)
print("=======================================================")
print("              In calibration mode.")
print(" Use trackbars to calibrate press space when done")
print("           Press D for default settings")
print("=======================================================")

# Calibration ranges so as to detect only 3 colours
yellow = calibration('Yellow', yellow, cap)
blue = calibration('Blue', blue, cap)
red = calibration('Red', red, cap)
print("Calibration Successfull!!")

cv2.namedWindow('Frame')

print("=========================================================")
print("     press P to turn ON and OFF mouse control")
print("     press C to display centroid of various colours")
print("     press R to recalibrate")
print("     Press ESC to exit")
print("=========================================================")

while True:
    key = cv2.waitKey(10) & 0xFF
    # Checking status based on key pressed
    changeStatus(key)

    if key == 27:
        break
cv2.destroyAllWindows()
