import cv2
import numpy as np
import pyautogui
import time, os


kernel = np.ones((7,7),np.uint8)
cursor = [960,540]

def nothing(x):
	pass

# Distance between two centroids
def distance( c1, c2):
	distance = pow( pow(c1[0]-c2[0],2) + pow(c1[1]-c2[1],2) , 0.5)
	return distance

def calibration(colourName, Range, cap):

	name = 'Calibrate' + colourName
	cv2.namedWindow(name)

	cv2.createTrackbar('Hue',name,Range[0][0]+20,230, nothing)
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
	'''
	Erosion erodes aeay the boundaries of foreground object.A pixel in the original
	image (either 1 or 0) will be considered 1 only if all the pixels under the kernel
	is 1, otherwise it is eroded (made to zero).

	Dilation is opposite of erosion.Here, a pixel element is ‘1’ if atleast one pixel
	under the kernel is ‘1’. So it increases the white region in the image or size of
	foreground object increases.

	Here erosion is followed by dilation since, erosion removes white noises but also shrinks
	our object. So we dilate it. Since noise is gone it won't come back, but our object area
	increases.

	Here we shall use opening which is jst another erosion followed by dialation
	'''

	#erosion = cv2.erode(mask, kernel, iterations=1)
	#dilation = cv2.dilate(erosion, kernel, iterations=1)
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

	#return dilation
	return opening

def swap(array, i):
	array[0],array[i] = array[i],array[0]

def drawCentroid(frame, colorArea, mask, showCentroid, showContour):

	'''The cv2.findContours() method returns three values, as a tuple; in this case,
	we are choosing to ignore the first and third return value. The first parameter is an
	intermediate image that is produced during the contour-finding process. We are
	not interested in that image in this application, so we effectively discard
	that image by placing the underscore (_) in the place of the first return value.
	The second return value is a list of NumPy arrays. Each array holds the points
	for one contour in the image. So, if we have executed our strategy correctly,
	the number of contours – the length of the contours list – will be the number of
	objects in the image. The final return value is a NumPy array that contains
	hierarchy information about the contours. This is also not useful so we shall  discard
	it with _'''

	_, contour, _ = cv2.findContours( mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# gives size of contour
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
		'''Once we have the contours, we can use them to get the moments
		for the corresponding objects in the image. The moments of an object
		are weighted averages of pixel intensities, or functions upon those averages'''

		# Finding centroid using method of moments
		M = cv2.moments(contour[0])

		'''The cv2.moments() method call computes the moments for a contour.
		The return value of the method call is a Python dictionary that contains
		the various moments for the contour. The centroid, or center point, for a
		contour can be found by dividing specific moments, as shown in the code.
		We truncate the results of the divisions to integers, and save the
		coordinates of the center point in the cx and cy variables.'''

		if M['m00'] != 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			center = (cx, cy)

			if showCentroid:
				cv2.circle(frame, center, 5, (0,0,255), -1)

			if showContour:
				cv2.drawContours(frame, contour[0], -1, (0,255,0), 5)

			return center

	else:
		#return error handling values
		return(-1,-1)

'''
This function calculates new cursor pos in such a way that mean deviation
for desired state is reduced. i.e, if difference is less than 5 px then it
is probably due to noise taken by webcam else it is delibrate movement.
'''
def setCursor(yCenter, Yprev):
	yp = np.zeros(2)

	if abs(yCenter[0] - Yprev[0]) < 5 and abs(yCenter[1] - Yprev[1])<5:
		yp[0] = yCenter[0] + 0.9*(Yprev[0]-yCenter[0])
		yp[1] = yCenter[1] + 0.9*(Yprev[1]-yCenter[1])
	else:
		yp[0] = yCenter[0] + 0.1*(Yprev[0]-yCenter[0])
		yp[1] = yCenter[1] + 0.1*(Yprev[1]-yCenter[1])

	return yp

'''
Depending upon the relative pos of 3 centroids this fuction chooses
the desired mouse action. Refer pic of mouse actions for better understanding
'''
def chooseAction(yp, rc, bc):
	out = np.array(['move', 'false'])

	if rc[0]!=-1  and bc[0]!=-1:
		if distance(yp, rc)<50 and distance(yp,bc)<80 and distance(rc,bc)<50:
			# all centroids are close to one another
			#print(distance(yp, rc), distance(yp, bc), distance(rc, bc))
			out[0] = 'drag'
			out[1] = 'true'
			return out
		elif distance(rc,bc)<40:
			out[0] = 'left'
			return out
		elif distance(yp,rc)<40:
			out[0] = 'right'
			return out
		elif distance(yp,rc)>40 and rc[1]-bc[1]>150:
			out[0] = 'down'
			return out
		elif bc[1]-rc[1]>110:
			out[0] = 'up'
			return out
		elif distance(yp,bc)<50 and abs(rc[1]-yp[1]) > 110:
			out[0] = 'SS'
			#print(out[0], distance(yp,bc),abs(rc[1]-yp[1]) )
			return out
		else:
			return out
	else:
		out[0] = -1
		return out
