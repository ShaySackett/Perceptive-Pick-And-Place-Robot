import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('sample data/smarties.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1 = 50, param2 = 30, minRadius = 0, maxRadius = 100)

circles = np.uint16(np.around(circles))  #change array of float to integer values



for circle in circles[0,:]:
    cv2.circle(img,(circle[0],circle[1]),circle[2],(0,255,0),2)  #put circle around recognized cirlce
    cv2.circle(img, (circle[0], circle[1]), 2, (255, 255, 255), 2)  #draw small circle at center of recognized circle



cv2.imshow('image',img)
k = cv2.waitKey(0)
cv2.destroyAllWindows()

