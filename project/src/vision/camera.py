import cv2
import math
import sys
import numpy as np
import logging 

def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()

def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)

    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix

def simplest_cb(img, percent):
    assert img.shape[2] == 3
    assert percent > 0 and percent < 100

    half_percent = percent / 200.0

    channels = cv2.split(img)

    out_channels = []
    for channel in channels:
        assert len(channel.shape) == 2
        # find the low and high precentile values (based on the input percentile)
        height, width = channel.shape
        vec_size = width * height
        flat = channel.reshape(vec_size)

        assert len(flat.shape) == 1

        flat = np.sort(flat)

        n_cols = flat.shape[0]

        low_val  = flat[int(math.floor(n_cols * half_percent))]
        high_val = flat[int(math.ceil( n_cols * (1.0 - half_percent)))]


        # saturate below the low percentile and above the high percentile
        thresholded = apply_threshold(channel, low_val, high_val)
        # scale the channel
        normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        out_channels.append(normalized)

    return cv2.merge(out_channels)

logging.basicConfig(level=logging.DEBUG)
cap = cv2.VideoCapture(-1)

def get_red_mask(hsv_img):
    # note that is in [0-180] and s, v in [0, 255] 
    mask1 = cv2.inRange(hsv_img, (0, 80, 40), (2, 255, 255))
    mask2 = cv2.inRange(hsv_img, (170, 80, 40), (180, 255, 255))
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

while(True):
    ret, frame = cap.read()
    frame = white_balance(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv = cv2.medianBlur(hsv, 5) # dealing with noise
    hsv = cv2.GaussianBlur(hsv, (1,1), 0)
    
    mask = get_red_mask(hsv)
    mask = noise_down(mask)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        maxContour = max(contours, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(maxContour)
        if w > 50 and h > 50:
            topx = x+w
            topy = y+h
            cropped = frame[y:topy, x:topx]
            cv2.imshow('crop', cropped)        
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [maxContour], -1,  (255, 0, 0), 2)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 128, 0), 2)
    cv2.imshow('in',frame)
    cv2.imshow('res', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

