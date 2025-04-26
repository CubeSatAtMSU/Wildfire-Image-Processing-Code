# importing required libraries
import matplotlib.pyplot as plt
import numpy as np
import cv2 as mr_kitty
import glob
from matplotlib.backends.backend_pdf import PdfPages

# Setting parameters for figures: font size, figure size in inches, and layout

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = [9,7]
plt.rcParams['figure.autolayout'] = True


# Changeable file type e.g(.jpg,.png,etc.) must be within **

file_type = "*.jpg*"

# adjustable range of pixel values from 0 to 255

n = 256

# building bin index for histogram

ih = np.zeros(n, np.int32)
for i in range(0, n):
    ih[i] = int(i)
    
# Set path for folder with images needing to be processed

    
path = '/home/cubesat/Desktop/Paper'
path += '/' + file_type


# Setting up image and histogram list to organize and process images efficiently

image_list = []
h760_list = []
h770_list = []
h780_list = []

# reading image/images of choice
# In this case I am using an image of pine needles from Feb 10

for file in sorted(glob.glob(path)):
    # ~ print(file)
    fimages = mr_kitty.imread(file, 0)
    image_list.append(fimages)

image_num = len(image_list)

# Calculating histograms for each set of images/filters
# They are then organized into their respective lists and summed up

for i in range(0, image_num):
    h_img = mr_kitty.calcHist([image_list[i]], [0], None, [256], [0, 256])
    if i < image_num/3:
        h760_list.append(h_img)
    elif i < (2/3)*image_num:
        h770_list.append(h_img)
    else:
        h780_list.append(h_img)
        
# Converting lists into arrays and summing

h760 = sum(np.array(h760_list))
h770 = sum(np.array(h770_list))
h780 = sum(np.array(h780_list))

# Co-plotting for histograms calculated above on linear and logarithmic scales

fig1, (ax1,ax2) = plt.subplots(1,2)
fig1.suptitle('Histograms on linear and log scales')

ax1.plot(h760, color='blue')
ax1.plot(h770, color='red')
ax1.plot(h780, color='green')
ax1.set_xlabel('Pixel Value')
ax1.set_ylabel('Number of Pixels')
ax1.legend(['h760', 'h770', 'h780'])
ax2.plot(h760, color='blue')
ax2.plot(h770, color='red')
ax2.plot(h780, color='green')
ax2.set_yscale('log')
ax2.set_xlabel('Pixel Value')
ax2.set_ylabel('Number of Pixels')
ax2.legend(['h760', 'h770', 'h780'])
plt.close('all')

# Setting up for s arrays

s760_list = []
s770_list = []
s780_list = []

# Flattening histogram arrays to 1D for functionality

h760, h770, h780 = h760.flatten(), h770.flatten(), h780.flatten()

# creating s arrays from 0 - 255

for i in range(0, 256):
    pix_sum1 = int(sum(h760))
    s760_list.append(pix_sum1)
    h760[i] = 0
    pix_sum2 = int(sum(h770))
    s770_list.append(pix_sum2)
    h770[i] = 0
    pix_sum3 = int(sum(h780))
    s780_list.append(pix_sum3)
    h780[i] = 0

# Converting lists into arrays 

s760 = np.array(s760_list)
s770 = np.array(s770_list)
s780 = np.array(s780_list)

# Co-plotting for s arrays wrt pixel value on linear and logarithmic scales

fig2, (ax1,ax2) = plt.subplots(1,2)
fig2.suptitle('S plots where s = sum_(i=j)[h_i] on linear and log scales')

ax1.plot(s760, color='blue')
ax1.plot(s770, color='red')
ax1.plot(s780, color='green')
ax1.set_xlabel('Pixel Value')
ax1.set_ylabel('Number of Pixels')
ax1.legend(['s760', 's770', 's780'])
ax2.plot(s760, color='blue')
ax2.plot(s770, color='red')
ax2.plot(s780, color='green')
ax2.set_yscale('log')
ax2.set_xlabel('Pixel Value')
ax2.set_ylabel('Number of Pixels')
ax2.legend(['s760', 's770', 's780'])
plt.close('all')

# Midpoint and delta 77 calculations 

midpoint = (1/2)*(s760 + s780)
delta77 = s770 - midpoint

# Plotting for delta 77 plot

fig3, ax = plt.subplots()
ax.plot(ih,delta77)
ax.set_title('Delta 77 plot')
ax.set_xlabel('Pixel Values')
ax.set_ylabel('Delta 77')

# Set limit for delta 77 plot
ax.set_ylim([-5000,5000])

plt.close('all')

# Organizing figures into list

fig_list = [fig1, fig2, fig3]

# Choose your file path and ame your report 

report_location = '/home/cubesat/Desktop' 
report_location += '/' + input('Name your file:\n') + '.pdf'

# Small function that creates pdf file

pdfFile = PdfPages(report_location)

for pltItr in range(0,3):
    pdfFile.savefig(fig_list[pltItr])

pdfFile.close()
