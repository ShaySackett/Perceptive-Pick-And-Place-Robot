import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,400,param1 = 50, param2 = 30, minRadius = 40, maxRadius = 100)

        if circles is not None:
            circles = np.uint16(np.around(circles))  #change array of float to integer values



            for circle in circles[0,:]:
                cv2.circle(frame,(circle[0],circle[1]),circle[2],(0,255,0),2)  #put circle around recognized cirlce
                cv2.circle(frame, (circle[0], circle[1]), 2, (255, 255, 255), 2)  #draw small circle at center of recognized circle

        cv2.imshow('image', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break




cap.release()
cv2.destroyAllWindows()

