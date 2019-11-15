#!/usr/bin/env python
# coding: utf-8

import cv2 as cv
import numpy as np
import time

#TODO: optimize this shit. It calculates about 0.8 s
def clearCircle(img, x, y, radius):
    return
    for i in range(len(img)):
        for j in range(len(img[0])):
            if( (i-y)*(i-y) + (j-x)*(j-x) >= r2 ):
                img[i][j] = 255
                
# TODO: refactor. Improve algo
def findPixelInArrow(img, xStart, yStart, arrowColor=255, jump=2, maxIterations=64):
    sign = 1
    x = xStart
    y = yStart
    for i in range(1, maxIterations):
        if img[y][x] == arrowColor: # TODO: check i and j are correct
            return (x, y)
        x = xStart + i*sign
        y = yStart + i*sign
        sign *= -1
    return None

def convolveStraightLines(img):
    kernel = np.array([[1, -1], [0, 0]])
    img = cv.filter2D(img, -1, kernel)
    kernel = np.array([[1], [-1]])
    return cv.filter2D(img, -1, kernel)

def eraseNegativeLines(img):
    kernel = np.array([[1, 0], [0,-1]])
    t = cv.filter2D(img, -1, kernel)
    kernel = np.array([[1, 0, 0], [0, 0, -1], [0, 0, 0]])
    t = cv.filter2D(t, -1, kernel)
    kernel = np.array([[1, 0, 0], [0, 0, 0], [0, -1, 0]])
    return cv.filter2D(t, -1, kernel)


def erasePositiveLines(img):
    kernel = np.array([[0, 1], [-1,0]])
    t = cv.filter2D(img, -1, kernel)
    kernel = np.array([[0, 0, 0], [0,0,1], [-1,0,0]])
    t = cv.filter2D(t, -1, kernel)
    kernel = np.array([[0, 0, 0], [0,1,0], [-1,0,0]])
    t = cv.filter2D(t, -1, kernel)
    kernel = np.array([[0, -1], [0, 0], [0,0], [0,0], [1, 0]])
    return cv.filter2D(t, -1, kernel)
    
def calcAvgY(img, color=255):
    ySum = 0
    yCount = 1
    for i in range(len(img)):
        for j in range(len(img[0])):
            if(img[i][j] == color):
                ySum += i
                yCount += 1
                
    return ySum/yCount


def processImage(img, title):
    # make it black and white only
    _, img = cv.threshold(img, 160, 255, cv.THRESH_BINARY)
    # get rid of point noise 
    img = cv.medianBlur(img, 3)
    # get rid of whitespaces in the circle contour
    kernel = np.ones((3,3),np.uint8)
    # erode?
    img = cv.erode(img,kernel,iterations = 1)
    # find circles (we give position of the center and radius) 
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,55,
                            param1=1,param2=17,minRadius=40,maxRadius=75)
    if circles is None: return None # it means the image is garbage
    circles = np.uint16(np.around(circles))

    beforeCircle = time.time()
    for i in circles[0,:]: # drawing for visualazing
        clearCircle(img, i[0],i[1], i[2]) # make circle black again

    afterCircle = time.time()
    print("Clearing circle: " + str(afterCircle - beforeCircle))
    # calc point in arrow to pass it to floodfill
    circle  = circles[0,0]
    centerX = circle[0]
    centerY = circle[1]
    xInArrow, yInArrow = findPixelInArrow(img, centerX, centerY, arrowColor=0)
    
    # flood fill the arrow
    mask = np.zeros((len(img) + 2, len(img[0]) + 2), np.uint8)
    cv.floodFill(img, mask, (xInArrow, yInArrow), 0)
    mask = cv.bitwise_not(mask) # what's going on with logic?
    img  = cv.bitwise_or(img, mask[2:len(mask), 2:len(mask[0])])
    
    # let's keep only arrow's oblique lines feature
    img = convolveStraightLines(img)
    
    # clear lines kx + b where k < 0
    imgPositive = eraseNegativeLines(img)
    imgNegative = erasePositiveLines(img)

    yAvgNegative = calcAvgY(imgNegative, 0)
    yAvgPositive = calcAvgY(imgPositive, 0)
    print("negative:"  + str(yAvgNegative))
    print("postitive:" + str(yAvgPositive))
    
    return "left" if yAvgPositive > yAvgNegative else "right"



for i in range(1, 5):
    img = cv.imread("img/" + str(i) + ".png", 1)
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    start = time.time()
    print(processImage(img, str(i)))
    end = time.time()
    print("time elapsed: " + str(end - start)) 

cv.destroyAllWindows()

