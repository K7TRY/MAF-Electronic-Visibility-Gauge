# Adapated from VisionTest by Amanda Joy Panell 22AUG17, and there is still extra code from that
# creates file of sample values of a light size, to use in the program "testytesty" to calculate
# change in light size

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

#Collects sample data for each light every minute and stores it in a file
def recordLightData():
    startMin = datetime.datetime.now().strftime("%M")
    
    fileName = '/home/PeregrinTook/visibilityTest/lightInfo.txt'
    
    print("\nBegining data collection now.")
    count = 0
    
    while True:
        fileName = '/home/PeregrinTook/visibilityTest/InfoBag.txt'
        lightInfo = open(fileName, 'a')
        lightInfo.write(str(checkLight(True,888,datetime.datetime.now().strftime("%M"), False)) + "\n") #Collect data
        lightInfo.close()
        count = count + 1
        time.sleep(2) #Wait for a minute
        
        if(count >= 10): #Exit after 10 tests
            print("Finished setup!")
            break  
    
#Set a lights expected visibility settings
def checkLight(onOff, avgOff, min, testYN):
    
    if(onOff == False):
        videoTitle = '/home/PeregrinTook/visibilityTest/lightOFF' + min + '.h264'
    else:
        GPIO.output(18,GPIO.HIGH)
        if(testYN):
            videoTitle = '/home/PeregrinTook/visibilityText/lightTest' + min + '.h264'
        else:
            videoTitle = '/home/PeregrinTook/visibilityTest/lightON' + min + '.h264'
        
    os.popen('raspivid -w 640 -h 480 -fps 25 -o '+ videoTitle +' -t 10000') #Take video to observe the light
    time.sleep(10)
    
    if(onOff == True):
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
            if(onOff == False):
                nonZero.append(cv2.countNonZero(brightThresh)) #When light is off
            else:
                if(testYN):
                    nonZero.append(cv2.countNonZero(brightThresh))
                else:
                    nonZero.append(cv2.countNonZero(brightThresh) - avgOff) #When light is on
    
        else:
            break #Break if video ends or cannot read frame
    
    avg = math.floor(sum(nonZero) / frameCount) #Average number of qualified pixels cast as an int
    
    cap.release() 
    cv2.destroyAllWindows()
    
    if(onOff == False):
        return(datetime.datetime.now().strftime("%H\t") + str(avg) + '\t' + str(checkLight(True, avg, False)))
    else:
        return avg

#Checks if a number is within a certian percentage of another number
def inRange(num,targetNum,percentage):
    somePercent = targetNum * (percentage / 100)
    if(num >= (targetNum - somePercent) and num <= (targetNum + somePercent)):
        return True

#Tests visibility of one light
def testSpecificLight():
    currentMin = datetime.datetime.now().strftime("%M")
    timeStamp = datetime.datetime.now().strftime("%d%m%y%H%M%S")
    
    size = checkLight(True,888, currentMin, True) #Take video, record sample, get size
    
    #Get expected size
    getSize = open('/home/PeregrinTook/visibilityTest/Info.txt')
    lineByLine = getSize.read().split("\n")
    for line in lineByLine:
        if (line[:2] == currentHr):
            lineSplit = line.split("\t")
            expectedSize = lineSplit[2]
    
    #Return verdict
    if(inRange(math.floor(size),int(expectedSize),10)):
        print("Light was within expected range: " + math.floor(size))
        print("Expected size of " + expectedSize)
        return True
    else:
        print("light was NOT within expected range: " + math.floor(size))
        print("Expected size of " + expectedSize)
        return False
        
recordLightData() #Initiates 24 hour data collection (Needs to be done at least once on a day with good visibility)
#testSpecificLight()
#getVisibility()
        