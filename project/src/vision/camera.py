import cv2
import math
import sys
import numpy as np
import logging 

cap = cv2.VideoCapture(-1)
#cap = cv2.VideoCapture('/home/art/out.ogv')

# get red areas
def get_red_mask(hsv_img):
    # note that is in [0-180] and s, v in [0, 255] 
    mask1 = cv2.inRange(hsv_img, (0, 100, 70), (2, 255, 255))
    mask2 = cv2.inRange(hsv_img, (170, 100, 70), (180, 255, 255))
    return mask1 + mask2 # and

def noise_down(mask):
    kernel1 = np.ones((4,4),np.uint8)
    kernel2 = np.ones((6,6),np.uint8)
    # opposite to erode. Fill red space
    res = cv2.dilate(mask, kernel1, iterations=2)
    # if one pix is black center is black
    res = cv2.erode(res, kernel1, iterations=1) 
    return res

def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

# frame may be passed only for painting contours
def find_interesting_bound(mask, frame):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        maxContour = max(contours, key = cv2.contourArea)
        #x, y, w, h = cv2.boundingRect(maxContour)
        return (cv2.boundingRect(maxContour), maxContour, contours)
    else:
        return ((0, 0, 0, 0), None, None)

def crop(img, x, y, w, h):
    if w > 50 and h > 50:
        topx = x+w
        topy = y+h
        cropped = frame[y:topy, x:topx]
        cropped = cv2.resize(cropped, (128, 128))

        return cropped
    else:
        return None

#### main loop
while(True):
    ret, frame = cap.read()
    frame = white_balance(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv = cv2.medianBlur(hsv, 5) # dealing with noise
    hsv = cv2.GaussianBlur(hsv, (1,1), 0)
    
    mask = get_red_mask(hsv)
    mask = noise_down(mask)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    (x, y, w, h), maxContour, contours = find_interesting_bound(mask, frame)
    cropped = crop(frame, x, y, w, h)
    if not cropped is None:
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cv2.imshow('crop', cropped)
        #cv2.imwrite('/home/art/robotVideo1/' + str(i) + '.jpeg', cropped)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 128, 0), 2)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [maxContour], -1,  (255, 0, 0), 2)

    cv2.imshow('res', result)
    
    cv2.imshow('in', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

