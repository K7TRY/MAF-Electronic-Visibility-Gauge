# This program calculates the percent increase/decrease in the apparent size of an LED by counting
# the number of pixels withing a predetermined range considered the light of the LED. This can be used to 
# detect fog under the assumption that fog will cause dispersion of the light, making it appear larger. The
# thresholds for clear vs a little foggy vs foggy vs too foggy, etc. still need to be determined.
# getClearData returns a list of light-size values from a clear day, for comparison
# getTestVal runs the camera on the RPi to determine the light's size at that moment.

import cv2
import os
import time
import numpy as np
import RPi.GPIO as GPIO
import imutils
import errno
import getpass
import datetime
import math

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18,GPIO.OUT) #LED

def getClearData():
    #Actually read file eventually
    return [11896,11405,11306,11454,11650,11256,11795,12078,12160,12265]

def getTestVal():
    #os.popen('raspistill -o /home/PeregrinTook/testForVis.png') #Take photo (preview off)

    videoTitle = '/home/PeregrinTook/visibilityTest/testLight.h264'
        
    GPIO.output(18,GPIO.HIGH)    
    os.popen('raspivid -w 640 -h 480 -fps 25 -o '+ videoTitle +' -t 10000') #Take video to observe the light
    time.sleep(10)
    GPIO.output(18,GPIO.LOW)
    
    cap = cv2.VideoCapture(videoTitle) 
    
    lower = np.array([80,70,120])
    upper = np.array([220,230,255])
    frameCount = 0
    nonZero = []

    while(True):
        ret,frame = cap.read() #Capture frame by frame
        
        if(ret):
            frameCount = frameCount + 1
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convert BGR to HSV (Hue saturated value)

            mask = cv2.inRange(hsv, lower, upper) #Look for light's color
            res = cv2.bitwise_and(frame,frame,mask= mask) #Bitwise_AND mask and frame
            grayS = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY) #Convert frame to grayscale
            brightThresh = cv2.threshold(grayS, 100, 255, cv2.THRESH_BINARY)[1] #Look for light's brightness
            
            #Count how many "qualified" pixels (right color and bright) exist in frame
            nonZero.append(cv2.countNonZero(brightThresh))
        else:
            break #Break if video ends or cannot read frame
    
    avg = math.floor(sum(nonZero) / frameCount) #Average number of qualified pixels cast as an int
    
    cap.release() 
    cv2.destroyAllWindows()
    
    return avg

#Begin Main
    
clearData = getClearData()
clearDataAvg = sum(clearData)/len(clearData)

print("Processing...\n")
testVal = getTestVal()
if (testVal < clearDataAvg):
    fogPercent = ((1 - (testVal/clearDataAvg))*100)
    print("The light is " +str(round(fogPercent,2)) +"% smaller than usual")
else:
    fogPercent = (((testVal/clearDataAvg) - 1)*100)
    print("The light is " + str(round(fogPercent, 2)) +"% larger than usual")
    


    
    