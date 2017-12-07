import cv2
import numpy as np
import pyautogui

kernel = np.ones((7,7),np.uint8)

def nothing(x):
	pass

def calibration(colourName, Range, cap):

	name = 'Calibrate' + colourName
	cv2.namedWindow(name)

	cv2.createTrackbar('Hue',name,Range[0][0]+20,180, nothing)
	cv2.createTrackbar('Sat',name,Range[0][1],255, nothing)
	cv2.createTrackbar('Val',name,Range[0][2],255, nothing)

	while True:
		k = cv2.waitKey(5) & 0xFF
		if k == ord('d'):
			cv2.destroyWindow(name)
			return Range

		_, revframe = cap.read()
		frame = cv2.flip(revframe, 1)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		hue = cv2.getTrackbarPos('Hue',name)
		sat = cv2.getTrackbarPos('Sat',name)
		val = cv2.getTrackbarPos('Val', name)

		lower = np.array([hue-20, sat, val])
		upper = np.array([hue+20, 255, 255])

		'''The cv2.inRange  function expects three arguments: the first is the image
		 were we are going to perform color detection, the second is the lower  limit
		 of the color you want to detect, and the third argument is the upper  limit
		 of the color you want to detect.'''

		mask = cv2.inRange(hsv, lower, upper)
		eroded = cv2.erode(mask, kernel, iterations=1)
		dilated = cv2.dilate(eroded, kernel, iterations=1)

		cv2.imshow(name, dilated)
		if k == ord(' '):
			cv2.destroyWindow(name)
			return np.array([[hue-20, sat, val], [hue+10, 255, 255]])

def createMask(frame, colorRng):
	'''cv2.inrange is used to filter out specific color then it
	undergoes erosion and dilation to generate mask'''

	mask = cv2.inRange(frame, colorRng[0], colorRng[1])
	# Morphosis
	erosion = cv2.erode(mask, kernel, iterations=1)
	dilation = cv2.dilate(erosion, kernel, iterations=1)

	return dilation

def swap(array, i):
	temp = array[i]
	array[i] = array[0]
	array[0] = temp

def drawCentroid(frame, colorArea, mask, showCentroid):
	_, contour, _ = cv2.findContours( mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	l = len(contour)
	area = np.zeros(l)

	#Filtering contours based on Area
	for i in range(l):
		if cv2.contourArea(contour[i])>colorArea[0] and cv2.contourArea(contour[i])<colorArea[1]:
			area[i] = cv2.contourArea(contour[i])
		else:
			area[i] = 0
	# Sorted returns a copy insted of sorting in place
	decend = sorted(area, reverse = True)

	# bringing contours with largest valid area to the top
	# which shall be later used to find centroid
	for i in range(l):
		if area[i] == decend[0]:
			swap( contour, i)

	if l > 0:
		# Finding centroid using method of moments
		M = cv2.moments(contour[0])
		if M['m00'] != 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			center = (cx, cy)

			if showCentroid:
				cv2.circle(frame, center, 5, (0,0,255), -1)

			return center

	else:
		#return error handling values
		return(-1,-1)
