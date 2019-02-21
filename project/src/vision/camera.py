import cv2
import logging 

logging.basicConfig(level=logging.DEBUG)
cap = cv2.VideoCapture(0)

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
    cv2.imshow('1',frame)

    hsv = cv2.medianBlur(hsv, 5) # dealing with noise
    hsv = cv2.GaussianBlur(hsv, (1,1), 0)
    
    mask = get_red_mask(hsv)
    mask = noise_down(mask)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('mask', mask)
    cv2.imshow('res', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

