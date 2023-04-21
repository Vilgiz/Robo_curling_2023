
import cv2

# Загружаем изображение

img = cv2.imread("C:\\Users\Vilgi\Desktop\sdsdw.jpg")
#img = cv2.imread("E:\\Robo_curling_2023\test_photo\sdsdw.jpg")

# Определение диапазона зеленого цвета
lower_green = (29, 86, 6)
upper_green = (64, 255, 255)

# Преобразование изображения в цветовую модель HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Создание маски для зеленого цвета
mask = cv2.inRange(hsv, lower_green, upper_green)

# Нахождение контуров на маске
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Вывод координат точек с зеленым цветом
for cnt in contours:
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        print("Координаты точки с зеленым цветом: ({}, {})".format(x, y))

# Отображение изображения с маской
cv2.imshow("Image", img)
cv2.imshow("Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
