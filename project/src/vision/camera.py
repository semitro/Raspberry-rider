import cv2
import logging 

logging.basicConfig(level=logging.DEBUG)
cap = cv2.VideoCapture(0)

def get_red_mask(hsv_img):
    # note that is in [0-180] and s, v in [0, 255] 
    mask1 = cv2.inRange(hsv_img, (0,   120, 120), (10, 255, 255))
    mask2 = cv2.inRange(hsv_img, (170, 120, 120), (180, 255, 255))
    return mask1 + mask2 # and

while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('1', hsv)

    hsv = cv2.medianBlur(hsv, 5)
    #hsv = cv2.GaussianBlur(hsv, (1,1), 0)

    cv2.imshow('2',hsv)
    mask = get_red_mask(hsv)

    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

