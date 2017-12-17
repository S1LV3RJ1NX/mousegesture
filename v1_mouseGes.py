import cv2
import numpy as np
from functions import *
import os

# Defining default ranges for colour values
blue = np.array([[85,69,36],[128,255,255]])#  108,78,20-->105,69,36
yellow = np.array([[11,70,80],[61,255,255]])# 41,70,80--> 31,70,80
red = np.array([[155, 82, 72],[185, 255, 255]])# 174,85,72--> 175,82,58

# Area ranges for contours of different colours to be detected
r_area = [100,1500]
b_area = [100,1500]
y_area = [100,1700]

# Prior initialization of all centers
b_cen, y_pos, r_cen = [240,320],[240,320],[240,320]
cursor = [960,540]

# Status variables
perform = False
showCentroid = False
showContour = False

def changeStatus(key):
		global perform
		global showCentroid
		global showContour
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
				print("              In recalibration mode.")
				print(" Use trackbars to calibrate press space when done")
				print("           Press D for default settings")
				print("=======================================================")

				# Calibration function present in functions.py
				yellow = calibration('Yellow', yellow, cap)
				blue = calibration('Blue', blue, cap)
				red = calibration('Red', red, cap)

		elif key == ord('d'):
				showContour = not showContour
				if showContour:
						print("Showing Contours")
				else:
						print("Not showing Contours")

		else:
			pass

def performAction(yp, rc, bc, action, drag, perform):
	if perform:
		cursor[0] = 4*(yp[0]-110)
		cursor[1] = 4*(yp[1]-110)
		if action == 'move':
			# if within boundary of frame go to respective cursor coordinates
			if yp[0]>110 and yp[0]<560 and yp[1]>110 and yp[1]<420:
				pyautogui.moveTo(cursor[0],cursor[1])

			# if on left edge
			elif yp[0]<110 and yp[1]>110 and yp[1]<420:
				pyautogui.moveTo( 8 , cursor[1])

			# if on right edge
			elif yp[0]>560 and yp[1]>110 and yp[1]<420:
				pyautogui.moveTo(1912, cursor[1])

			# if on top edge
			elif yp[0]>110 and yp[0]<560 and yp[1]<110:
				pyautogui.moveTo(cursor[0] , 8)

			# if on bottom edge
			elif yp[0]>110 and yp[0]<560 and yp[1]>420:
				pyautogui.moveTo(cursor[0] , 1072)

			# top left corner
			elif yp[0]<110 and yp[1]<110:
				pyautogui.moveTo(8, 8)

			# bottom left corner
			elif yp[0]<110 and yp[1]>420:
				pyautogui.moveTo(8, 1072)

			# bottom right corner
			elif yp[0]>560 and yp[1]>420:
				pyautogui.moveTo(1912, 1072)

			# top right corner
			else:
				pyautogui.moveTo(1912, 8)

		elif action == 'left':
			pyautogui.click(button = 'left')
			#time.sleep(0.3)

		elif action == 'right':
			pyautogui.click(button = 'right')
			time.sleep(0.3)

		elif action == 'up':
			pyautogui.scroll(5)

		elif action == 'down':
			pyautogui.scroll(-5)

		elif action == 'SS':
			os.system("gnome-screenshot --file=image.png")
			time.sleep(0.3)


		elif action == 'drag' and drag == 'true':
			global y_pos
			drag = 'false'
			pyautogui.mouseDown()

			while(1):

				k = cv2.waitKey(10) & 0xFF
				changeStatus(k)

				_, frameinv = cap.read()
				# flip horizontaly to get mirror image in camera
				frame = cv2.flip( frameinv, 1)

				hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV)

				b_mask = createMask( hsv, blue)
				r_mask = createMask( hsv, red)
				y_mask = createMask( hsv, yellow)

				Yprev = y_pos

				b_cen = drawCentroid( frame, b_area, b_mask, showCentroid, showContour)
				r_cen = drawCentroid( frame, r_area, r_mask, showCentroid, showContour)
				y_cen = drawCentroid( frame, y_area, y_mask, showCentroid, showContour)

				if 	Yprev[0]!=-1 and y_cen[0]!=-1:
					y_pos = setCursor(y_cen, Yprev)

				performAction(y_pos, r_cen, b_cen, 'move', drag, perform)
				cv2.imshow('Frame', frame)

				# if fingers go far apart i.e, drag action stops then end
				if distance(y_pos,r_cen)>60 or distance(y_pos,b_cen)>60 or distance(r_cen,b_cen)>60:
					break

			pyautogui.mouseUp()

# Begin
cap = cv2.VideoCapture(0)
print("=======================================================")
print("              In calibration mode.")
print(" Use trackbars to calibrate press space when done")
print("           Press D for default settings")
print("=======================================================")

# Calibration ranges so as to detect only 3 colours
# Calibration function present in functions.py
yellow = calibration('Yellow', yellow, cap)
blue = calibration('Blue', blue, cap)
red = calibration('Red', red, cap)
print("Calibration Successfull!!")

cv2.namedWindow('Frame')

print("=========================================================")
print("     press P to turn ON and OFF mouse control")
print("     press C to display centroid of various colours")
print("     press R to recalibrate")
print("     press D to show contours")
print("     Press ESC to exit")
print("=========================================================")

while (1):
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

    b_cen = drawCentroid( frame, b_area, b_mask, showCentroid, showContour)
    r_cen = drawCentroid( frame, r_area, r_mask, showCentroid, showContour)
    y_cen = drawCentroid( frame, y_area, y_mask, showCentroid, showContour)

    '''cv2.drawContours(frame, b_cen, -1, (0,255,0), 5)
    cv2.drawContours(frame, r_cen, -1, (0,255,0), 5)
    cv2.drawContours(frame, y_cen, -1, (0,255,0), 5)'''

    Yprev = y_pos

    if Yprev[0]!=-1 and y_cen[0]!=-1 and y_pos[0]!=-1:
        y_pos = setCursor(y_cen, Yprev)

    output = chooseAction(y_pos, r_cen, b_cen)
    if output[0]!=-1:
        performAction(y_pos, r_cen, b_cen, output[0], output[1], perform)

    cv2.imshow('Frame', frame)

    if key == 27:
        break
cv2.destroyAllWindows()
