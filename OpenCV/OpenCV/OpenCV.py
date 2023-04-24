
import cv2
import numpy

img = cv2.imread("C:\\Users\Vilgi\Desktop\sdsdw.jpg")   # Загружаем изображение

lower_green = (30, 50, 50)                               # Определение диапазона зеленого цвета в HSV
upper_green = (90, 255, 230)


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)              # Преобразование изображения в цветовую модель HSV

mask = cv2.inRange(hsv, lower_green, upper_green)       # Создание маски для зеленого цвета

contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    # Нахождение контуров на маске


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_color = img[y, x][::-1]
        print(f"Цвет пикселя ({x}, {y}): {pixel_color}")


def print_():
    for cnt in contours:                                    # Вывод координат точек с зеленым цветом
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            print("Координаты точки с зеленым цветом: ({}, {})".format(x, y))


def main():
   
    cv2.imshow("Mask", mask)                        # Отображение маски
                
    cv2.namedWindow('image')                        
    cv2.setMouseCallback("image", mouse_callback)
    cv2.imshow('image', img)                        # Отображение окна изображения

    print_()

    cv2.waitKey(0)
    cv2.destroyAllWindows()    

main()