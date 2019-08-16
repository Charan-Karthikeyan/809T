import numpy as np


import cv2


import imutils 


import collections

import math

image =cv2.imread("temp.jpg")
#image =cv2.imread("arrow.jpeg")
image = cv2.flip(image,1)



image = imutils.resize(image, width=900)



num_arr=[]
	
	
lower_green= np.array ([40,90,100])


upper_green = np.array([90,255,190])


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

mask= cv2.inRange(hsv,lower_green,upper_green)


blur = cv2.GaussianBlur(mask,(9,9),0)
result=cv2.bitwise_and(hsv, hsv, mask=mask)

corners = cv2.goodFeaturesToTrack(blur,5,0.03,20)
print(corners)

corners = np.int32(corners)


for i in corners:
    x,y = i.ravel()
    cv2.circle(image,(x,y),4,(255,0,0),-1)

points=np.array(corners).reshape(5,2)
num_arr=(0,1,2,3,4)
rest=[]

for b in num_arr:
	for c in range(b+1,len(num_arr)):
	 dist = np.linalg.norm(points[b]-points[c])
	 rest.append([dist,b,c])


rest.sort()
rest.reverse()
temp = []
temp.append(rest[0][1])
temp.append(rest[0][2])
temp.append(rest[1][1])
temp.append(rest[1][2])

head=-1
for i in temp:
	if temp.count(i)>1:
	 head=i
	 break
temp.remove(head)
temp.remove(head)


midpoint = (points[temp[0]] + points[temp[1]])/2

dir = points[head] - midpoint

myradians = math.atan2(dir[1], dir[0])
mydegrees = math.degrees(myradians)
print(mydegrees)

cv2.circle(image,(int(midpoint[0]),int(midpoint[1])),4,(255,0,0),-1)
cv2.line(image,(int(midpoint[0]),int(midpoint[1])),(int(points[head][0]),int(points[head][1])),(255,30,200),3)

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
red = (0, 0, 255)
if  -135< mydegrees < -45:
 cv2.putText(image, " UP degrees= %f"%(mydegrees), (100, 200), font, 2, red, 2)

elif -180< mydegrees< -135:
 cv2.putText(image, "LEFT degrees= %f"%(mydegrees), (100, 200), font, 1, red, 1)

elif 135< mydegrees< 180:
 cv2.putText(image, " LEFT degrees= %f" % (mydegrees), (100, 200), font, 1, red, 1)

elif 45 <mydegrees< 135:
 cv2.putText(image, " DOWN degrees= %f" % (mydegrees), (100, 200), font, 1, red, 1)

elif 0< mydegrees < 45:
 cv2.putText(image, " RIGHT degrees= %f"% (mydegrees), (100, 200), font, 1, red, 1)

else:
 cv2.putText(image, " RIGHT degrees= %f"% (mydegrees), (100, 200), font, 1, red, 1)

cv2.imshow("hw4",image)

cv2.waitKey(0)
		