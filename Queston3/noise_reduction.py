import cv2

img=cv2.imread("Blury.png")
h,w,c=img.shape
print(f"Total Resolution/Pixels of the image :{h}*{w}")

blurred_img=cv2.GaussianBlur(img,(5,5),0)
median_blurred_img=cv2.medianBlur(blurred_img,5)

cv2.imshow("original",img)
cv2.imshow("blurred",blurred_img)
cv2.imshow("median",median_blurred_img)
cv2.imwrite("Denoised image.png", median_blurred_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
