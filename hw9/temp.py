import cv2
import numpy 

image = cv2.imread("inv_image.jpg")
print(image.shape)
print(image.shape[0])
c_x = int(image.shape[0]/2)
c_y = int(image.shape[1]/2)

cv2.circle(image,(c_y,c_x),4,(0,0,255),-1)
cv2.imshow('image',image)
cv2.waitKey()
cv2.destroyAllWindows()