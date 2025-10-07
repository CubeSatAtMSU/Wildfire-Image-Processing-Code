import cv2
import numpy
from picamera2 import Picamera2, Preview
import time
'''
IMPORTANT THOUGHTS
As of writing this the current plan is to get a Raspberry Pi 5, which includes 2 CSI ports. This allows us to mount 
two of the cameras direclty to the RPi, but one of the cameras will have to be connected via a USB to CSI 
connector. All of the code to take pictures via CSI use the Picamera2 library, while the USB camera uses the 
OpenCV library. When we actually acquire the RPi 5, testing should be done on image similarity between the 
cameras directly connected through the CSI ports and the single USB camera.

To control resolution for the OpenCV camera, 
<CAMERAVARIABLE>.set(cv2.CAP_PROP_FRAME_WIDTH, <WIDTH>)
<CAMERAVARIABLE>.set(cv2.CAP_PROP_FRAME_HEIGHT, <HEIGHT>)
'''


# Establishes different cameras. 
# Cameras 1 & 2 will be connected through the CSI ports and will be established using PiCamera. 
# --- Important note --- Testing needs to be done on the indexes when using multiple CSI cameras. 
cam1 = Picamera2(0)
cam2 = Picamera2(1)

# Since camera 3 will be used through a CSI to USB connector, it will be setup through USB.
# cv2.V4L2 MUST BE HERE!!!
# --- Important note --- Look into config files to make all cameras look the same.  
cam3 = cv2.VideoCapture(2, cv2.CAP_V4L2)

# Configurations for the Picamera2 cameras. Look into how to do this with the OpenCV cameras. 
# --- Important note --- the commands all saying preview may all be unecessary if we just want to take images. Testing required.
controls = {"ExposureTime": 500, "AnalogueGain": 1.0, "ColourGains": (0.0,0.0), "Saturation": 0.0, "AeEnable": 0}

preview_config = cam1.create_preview_configuration(controls=controls)
capture_config = cam1.create_still_configuration(raw={}, display=None)
cam1.configure(preview_config)

preview_config = cam2.create_preview_configuration(controls=controls)
capture_config = cam2.create_still_configuration(raw={}, display=None)
cam2.configure(preview_config)

cam1.start()
cam2.start()

time.sleep(1)


# Save Picamera2 images. 
cam1.capture_file("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam1.png")
cam2.capture_file("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam2.png")

#Flush out buffer images. If not done, pictures saved may be not be current. (Happened with crappy USB camera at least, testing required.)
for i in range(5):
    cam3.read()

ret, frame3 = cam3.read()
if ret:
    cv2.imwrite("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam3.png", frame3)
else:
    print("cam3 failed")


# Read the saved images in grayscale. Let us say img1 & img 3 are the left and right, and img2 is the peak. 
# Note - May want to make the camera connected through USB the peak reading so everything stays consistent. 
img1 = cv2.imread("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam1.png",cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam2.png",cv2.IMREAD_GRAYSCALE)
img3 = cv2.imread("/home/cubesat/Desktop/Wildfire-Image-Processing-Code/cam3.png",cv2.IMREAD_GRAYSCALE)

'''
NumPy is a library that converts the images into arrays. This allows for much quicker data processing. As you will
see from the following lines of code, you can just do simple arithmetic to add and subtract the pixel data. 
'''
left = img1.astype(numpy.float32)
peak = img2.astype(numpy.float32)
right = img3.astype(numpy.float32)

# Average the left and right images. 
mid = (left + right) / 2.0

# Subtract the actual value from the "expected" value. 
intensity = peak - mid

'''
cv2.THRESH_BINARY lets us set a lower threshold for the pixel values after we finish the image processing. 
This will leave us with an image where the purely white spots are areas where potassium is being detected, 
indicating a fire. The number after intensity is the lower threshold, and should be tuned through manual testing. 
'''

ret, finimg = cv2.threshold(intensity, 50, 255, cv2.THRESH_BINARY)
cv2.imwrite("finalimage.png", finimg)