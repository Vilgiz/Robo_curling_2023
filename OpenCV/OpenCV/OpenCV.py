import cv2

image = cv2.imread("C:\\Users\Vilgi\Desktop\IMG_20230409_110532.jpg")

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()