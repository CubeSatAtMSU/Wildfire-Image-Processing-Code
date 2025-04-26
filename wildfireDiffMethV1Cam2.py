import cv2
import numpy
from picamera2 import Picamera2, Preview
import time
'''
IMPORTANT THOUGHTS
While testing, we may want to impliment some resolution control since we will most likely be testing with
various different USB cameras. This may not be necessary in the final product as we will be using the 
same camera (RPi camera module 3 i think). If you are testing and need to control the resolution of the 
saved images, use the following commands. 
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

You may also notice that instead of using PiCamera2, openCV is used. This is because of our current 
decision to use CSI to USB adapters to plug in multiple RPi camera modules. openCV also already 
includes some basic image processing, so it seems like the better choice. Again, all of this
is subject to change. 
'''


# Establishes different cameras. 
# Check camera device index and change accordingly. 
#cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(0, cv2.CAP_V4L2)
cam1 = Picamera2()
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

# When testing on my computer, just doing test.png did not work in the cv2.imwrite. 
# Image path had to be entire thing. Further testing required. 
image_path = r'C:\Users\Steven\test.png'
#picam2 = Picamera2()
cam1.start_preview(Preview.QTGL)

controls = {"ExposureTime": 500, "AnalogueGain": 1.0, "ColourGains": (0.0,0.0), "Saturation": 0.0, "AeEnable": 0}

preview_config = cam1.create_preview_configuration(controls=controls)
capture_config = cam1.create_still_configuration(raw={}, display=None)
cam1.configure(preview_config)

cam1.start()
time.sleep(1)
#Flush out buffer images. If not done, pictures saved may be old, buffered images. 
for i in range(5):
    #cam1.read()
    cam2.read()

# 90% sure ret is necessary for the .read() function to work. if else statement may not. Further testing required. 
#ret, frame1 = cam1.read()
#if ret:
    # Remove comment if you want image to show 
    #cv2.imshow("Captured Image", frame1)
#    cv2.imwrite("cam1.png", frame1)
#else:
#    print("cam1 failed")

cam1.capture_file("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam1.png")

ret, frame2 = cam2.read()
if ret:
    # Remove comment if you want image to show
    #cv2.imshow("Captured Image", frame2)
    cv2.imwrite("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam2.png", frame2)
else:
    print("cam2 failed")


# Read the saved images in grayscale. Let us say img1 & img 3 are the left and right, and img2 is the peak. 
img1 = cv2.imread("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam1.png",cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam2.png",cv2.IMREAD_GRAYSCALE)

# Establish the images as numpy arrays for easy quick image processing. 
left = img1.astype(numpy.float32)
peak = img2.astype(numpy.float32)

# Subtract the actual value from the "expected" value. 
intensity = peak - left

#Second variable in the threshold is the lower bounds and should be adjust to our needs. Third variable is the upper bounds and should be kept at 255.
ret, finimg = cv2.threshold(intensity, 50, 255, cv2.THRESH_BINARY)
cv2.imwrite("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/finimg.png", finimg)




