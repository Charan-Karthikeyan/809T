import numpy as np 

import cv2 

import imutils 


image =cv2.imread("light.png")

image = imutils.resize(image, width=400)

#cv2.imshow("canvas", image)
lower_green= np.array ([70,200,100])

upper_green = np.array([90,255,190])

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow("hsv",hsv)
mask= cv2.inRange(hsv,lower_green,upper_green)

result=cv2.bitwise_and(hsv, hsv, mask=mask)

#cv2.imshow("filtered",result)


#cv2.imshow("mask", hsv)
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
center = None

if len(cnts) >0:
	c = max(cnts,key = cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

	if radius > 10:
		cv2.circle(image, (int(x), int(y)), int(radius),(0, 125, 255), 2)
		cv2.circle(image,center,5,(0,0,255),-1)
cv2.imshow("circle_with",image)


cv2.waitKey(0)
		













