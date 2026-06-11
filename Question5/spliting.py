import cv2
import numpy as np

img=cv2.imread("Himalaya.png")

blue_channel = img[ :, :, 0]
green_channel = img[ :, :, 1]
red_channel = img[ :, :, 2]

blank=np.zeros_like(green_channel)
combining=cv2.merge([blue_channel,blank, red_channel])

cv2.imshow("blue", blue_channel)
cv2.imshow("green", green_channel)
cv2.imshow("red", red_channel)
cv2.imshow("combining", combining)
cv2.imwrite("combining.png", combining)
cv2.waitKey(0)
cv2.destroyAllWindows()