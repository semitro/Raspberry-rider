import cv2
import numpy as np
import logging 

logging.basicConfig(level=logging.DEBUG)
cap = cv2.VideoCapture(2)
for i in range(50000):
    print(i*13. - i + i -i - i*12.)
    pass

def get_red_mask(hsv_img):
    # note that is in [0-180] and s, v in [0, 255] 
    mask1 = cv2.inRange(hsv_img, (0,   130, 90), (10, 255, 255))
    mask2 = cv2.inRange(hsv_img, (170, 130, 90), (180, 255, 255))
    return mask1 + mask2 # and

def noise_down(mask):
    # if one pix is black center is black
    res = cv2.erode(mask, None, iterations=2) 
    # opposite to erode. Fill red space
    res = cv2.dilate(res, None, iterations=3)
    return res

while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv = cv2.medianBlur(hsv, 5) # dealing with noise
    hsv = cv2.GaussianBlur(hsv, (1,1), 0)
    
    mask = get_red_mask(hsv)
    mask = noise_down(mask)
    cv2.imshow('mask', mask) 
    result = cv2.bitwise_and(frame, frame, mask=mask)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    cv2.imshow('in',frame)
    cv2.imshow('res', result)
#crop
    #(x, y) = np.where(mask == 255)
    if len(contours) > 1:
        x, y, w, h = cv2.boundingRect(contours[0])
        topx = x+w
        topy = y+h
        cropped = frame[x:topx+1, y:topy+1]# cv2.rect (0, 255, 0, -1))
        cv2.imshow('crop', cropped)        
   # if len(x) != 0 and len(y) !=0 :
   #    (topx, topy) = (np.min(x), np.min(y))
   #     (botx, boty) = (np.max(x), np.max(y))
   #     cropped = frame[topx:botx+1, topy:boty+1]
   #     cv2.imshow('crop', cropped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

