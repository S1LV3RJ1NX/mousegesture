import cv2
import numpy as np
from functions import *


# Defining default ranges for colour values
blue = np.array([[85,69,36],[128,255,255]])#  108,78,20-->105,69,36
yellow = np.array([[11,70,80],[61,255,255]])# 41,70,80--> 31,70,80
red = np.array([[155, 82, 72],[185, 255, 255]])# 174,85,72--> 175,82,58

# Area ranges for contours of different colours to be detected
r_area = [100,1300]
b_area = [100,1300]
y_area = [100,1300]

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

        # Calibration function present in functions.py
        yellow = calibration('Yellow', yellow, cap)
        blue = calibration('Blue', blue, cap)
        red = calibration('Red', red, cap)

    else:
        pass


# Begin
cap = cv2.VideoCapture(0)
'''print("=======================================================")
print("              In calibration mode.")
print(" Use trackbars to calibrate press space when done")
print("           Press D for default settings")
print("=======================================================")

# Calibration ranges so as to detect only 3 colours
# Calibration function present in functions.py
yellow = calibration('Yellow', yellow, cap)
blue = calibration('Blue', blue, cap)
red = calibration('Red', red, cap)'''
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

    '''Now we are going to capture video flip it as what we get
    from input is reversed frame then based on color ranges
    calibrated we are going to prepare mask for respective colors'''

    _, source = cap.read()
    frame = cv2.flip(source, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    b_mask = createMask(hsv, blue)
    r_mask = createMask(hsv, red)
    y_mask = createMask(hsv, yellow)

    b_cen = drawCentroid( frame, b_area, b_mask, showCentroid)
    r_cen = drawCentroid( frame, r_area, r_mask, showCentroid)
    y_cen = drawCentroid( frame, y_area, y_mask, showCentroid)

    '''cv2.drawContours(frame, b_cen, -1, (0,255,0), 5)
    cv2.drawContours(frame, r_cen, -1, (0,255,0), 5)
    cv2.drawContours(frame, y_cen, -1, (0,255,0), 5)'''

    cv2.imshow('Frame', frame)



    if key == 27:
        break
cv2.destroyAllWindows()
