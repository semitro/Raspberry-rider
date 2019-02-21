import cv2

cap = cv2.VideoCapture(0)

def get_red_mask(hsv_img):
    # note that is in [0-180] and s, v in [0, 255] 
    mask1 = cv2.inRange(hsv_img, (0,   120, 120), (10, 255, 255))
    mask2 = cv2.inRange(hsv_img, (170, 120, 120), (180, 255, 255))
    return mask1 + mask2 # and

while(True):
    ret, frame = cap.read()
    cv2.imshow('original', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = get_red_mask(hsv)

    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

