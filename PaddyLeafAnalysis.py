import numpy as np
import sys
import time
import os
from collections import OrderedDict
from glob import glob
from datetime import datetime
import cv2

# OpenCV max values: H-max = 179, S-max and V-max = 255
# paint.net uses H = 0 to 360, S = 0 to 100, V = 0 to 100
# need to convert the value to openCV values before use.


# FUNCTION : FIND BLAST ===============================================
def convert(img_path, out_path):
    img = cv2.imread(img_path)
    output = img
    # Set minimum and max HSV values to display
    lower = np.array([0, 30, 0])    # Minimum range here [ H, S, V ]
    upper = np.array([22, 255, 255])# Maximum range here [ H, S, V ]
    # lower = np.array([0, 40, 0])    # Minimum range here [ H, S, V ]
    # upper = np.array([20, 155, 255])# Maximum range here [ H, S, V ]
    # Masking here
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)


    output = cv2.bitwise_and(img,img, mask= mask)

    output = ~output
    lower = np.array([0, 20, 0])    # Minimum range here [ H, S, V ]
    upper = np.array([179, 255, 255])# Maximum range here [ H, S, V ]
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(output,output, mask= mask)
    cv2.imwrite(out_path, output)


# START HERE ==========================================================
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0
chart1 = chart2 = chart3 = chart4 = chart5 = chart6 = 0
statusChart =""
status = ""
data_dir = './NewImage/'
old_dir = './Converted/'
print('!!! Paddy Leaf Checker (PROTOTYPE) !!!')
print('')
input("Put your Paddy Leaf images (.JPG FILES ONLY) into the < NewImage > folder, and press ENTER to continue...")
while(True):
    time.sleep(1)
    images = glob(os.path.join(data_dir, '*.jpg'))
    total_images = len(images)

    if total_images > 0:
        print('Number of images:', total_images)
        time.sleep(2)
        for f in glob(os.path.join(data_dir, '*.jpg')):
            o = old_dir + os.path.basename(f)
            convert(f,o)
            time.sleep(2);
            total_images = total_images - 1

            # THIS PART TO DETECT BLAST?
            img = cv2.imread(o)
            BLUE_MIN = np.array([130, 50, 50], np.uint8)  # IT IS BGR NOT RGB
            BLUE_MAX = np.array([255, 200, 200], np.uint8)
            dst = cv2.inRange(img, BLUE_MIN, BLUE_MAX)
            no_blue = cv2.countNonZero(dst)
            WHITE_MIN = np.array([254, 254, 254], np.uint8)  # IT IS BGR NOT RGB
            WHITE_MAX = np.array([255, 255, 255], np.uint8)
            dst2 = cv2.inRange(img, WHITE_MIN, WHITE_MAX)
            no_white = cv2.countNonZero(dst2)
            if(no_white <5):
                no_white = 5
            ratio_white_blue = (no_blue/no_white)*100
            status = "Healthy"  # if blue pixel more than 2900 then consider as unhealthy
            if (ratio_white_blue > 1):
                status = "Need Attention, possible unhealthy plant"

            # PADDY LEAF CHART COMPARISON
            img = cv2.imread(f)
            CHART1_MIN = np.array([64, 0, 0])  # IT IS HSV
            CHART1_MAX = np.array([70, 255, 255])
            hsvChart = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cht1 = cv2.inRange(hsvChart, CHART1_MIN, CHART1_MAX)
            chart1 = cv2.countNonZero(cht1)

            CHART2_MIN = np.array([71, 0, 0])  # IT IS HSV
            CHART2_MAX = np.array([83, 255, 255])
            hsvChart = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cht2 = cv2.inRange(hsvChart, CHART2_MIN, CHART2_MAX)
            chart2 = cv2.countNonZero(cht2)

            CHART3_MIN = np.array([84, 0, 0])  # IT IS HSV
            CHART3_MAX = np.array([92, 255, 255])
            hsvChart = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cht3 = cv2.inRange(hsvChart, CHART3_MIN, CHART3_MAX)
            chart3 = cv2.countNonZero(cht3)

            CHART4_MIN = np.array([93, 0, 0])  # IT IS HSV
            CHART4_MAX = np.array([118, 255, 255])
            hsvChart = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cht4 = cv2.inRange(hsvChart, CHART4_MIN, CHART4_MAX)
            chart4 = cv2.countNonZero(cht4)

            CHART5_MIN = np.array([119, 0, 0])  # IT IS HSV
            CHART5_MAX = np.array([127, 255, 255])
            hsvChart = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cht5 = cv2.inRange(hsvChart, CHART5_MIN, CHART5_MAX)
            chart5 = cv2.countNonZero(cht5)
            
            
            chart6 = 0            #original intended to be 6 chart.
            statusChart = ""  # if blue pixel more than 2900 then consider as unhealthy
            if (max(chart1,chart2,chart3,chart4,chart5,chart6) == chart1):
                statusChart = 'LCC: Critical Condition'
                LCC = 1
                
            if (max(chart1,chart2,chart3,chart4,chart5,chart6) == chart2):
                statusChart = 'LCC: Maximum N is needed'
                LCC = 2
                
            if (max(chart1,chart2,chart3,chart4,chart5,chart6) == chart3):
                statusChart = 'LCC: N supply is needed'
                LCC = 3
                
            if (max(chart1,chart2,chart3,chart4,chart5,chart6) == chart4):
                statusChart = 'LCC: N Supply need to be improved'
                LCC = 4
                
            if (max(chart1,chart2,chart3,chart4,chart5,chart6) == chart5):
                statusChart = 'LCC: Healthy'
                LCC = 5
                
            if (ratio_white_blue > 1):
                status = "Need Attention, possible unhealthy plant"

            ## RESULTS
            print('FILE: ' + o + '   , Status: ' + status + '   , ' + statusChart)
            # print(ratio_white_blue)

    print('')
    print('Analyse completed. Thank you for using.')
    print('Powered by I LIKE RICE')
    print('')
    print('')
    input("Put your Paddy Leaf images (.JPG FILES ONLY) into the < NewImage > folder, and press ENTER to continue...")


