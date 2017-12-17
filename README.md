# Mousegesture - Let your hand be mouse
Mouse conrol using OpenCv

Packages required:
  1. Python interpreter
  2. OpenCV
  3. PyAutoGUI
  4. Numpy

For installation of above packages ref google or other online sources. Best way is to use virtual envs(like miniconda)
to avoid any complications.

######################################################################################################

# Technical Details

1. Firstly we capture video in HSV format and calibrate color ranges of three fingers using calibration function, or we can use
   default settings as well.Depending on the calibrations, only the three fingertips are extracted from the video, one
   by one, using the **cv2.inRange()** function. In order to remove noise in the video feed, we apply a two-step morphism i.e. **erosion** and **dilation**. The noise filtered image referred to as
   mask in the program is then sent for locating the centres.
   
2. Location of each of the three centres involves:

      a) Finding contours in the mask relevant to that colour range. This is done by createMask function here instead of 
         using two step morphism we use opening which is same as erosion followed by dilation
         
      b) Discarding contours of irrelevant areas using area filters.
      
      c) Finding the largest contour amongst the remaining ones and applying method of
         moments to find its centre.
         (Both b and c are implemented in **drawCentroid()** function
         
3. Setting cursor position:
    Yellow colour is responsible for setting cursor position. Following method was used to achieve the same.
    
    **) Generally the webcams we use captures video at a resolution of 640x480 pixels. Suppose this frame was linearly mapped 
      to the 1920x1080 pixel display screen. If we have a right-handed user, he would find it uncomfortable to access the left 
      edge of the screen as compared to the right edge. Also accessing the bottom portion of the screen would build stress at 
      the wrist. Hence instead of mapping the whole video frame to the screen, we could rather consider a rectangular sub portion 
      more biased towards right (considering right-handed user) and upper parts of the frame in order to improve comfort. This
      sub portion which measures 480x270 pixels is then linearly mapped to the screen with a scaling factor of 4.
      
    **) Due to noise captured by webcam and vibrations of hand centers keep on vibrating and on scaling we get lot of problems with 
        accuracy. Hence to reduce shakiness we compare the new centre with the previous position of the cursor. If difference is less 
        than 5 pixels, it is usually due to noise. Thus the new cursor position is inclined more towards the previous one. However, 
        a larger difference in previous position and new centre is considered as voluntary movement and the new cursor position is 
        set close to the new centre. This is implemented in **SetCursor()** function
        
    **) Now depending upon locations of three centers what action to be taken is decided by **chooseAction()** function and
        action to be performed is done by **performAction()** function. Actions are carried out with help of **pyAutoGui**
        library.
        Actions performed are:- free movement of cursor, left/right click, drag/select, scroll up/down and screenshot.
        Images to perform those action are given in handmovements.jpg except, **Screenshot** action is performed by connecting
        thumb and middle finger (yellow and blue) and keeping index finger(red) straight/ slighly away from the other two
        like letter 'd' 
