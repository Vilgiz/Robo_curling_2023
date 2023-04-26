
import cv2 as cv
import numpy

img = cv.imread("C:\\Users\Vilgi\Desktop\sdsdw.jpg")   # Загружаем изображение

lower_green = (30, 50, 50)                               # Определение диапазона зеленого цвета в HSV
upper_green = (90, 255, 230)


hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)              # Преобразование изображения в цветовую модель HSV

mask = cv.inRange(hsv, lower_green, upper_green)       # Создание маски для зеленого цвета

contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)    # Нахождение контуров на маске


def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_color = img[y, x][::-1]
        print(f"Цвет пикселя ({x}, {y}): {pixel_color}")


def print_():
    for cnt in contours:                                    #  Вывод координат точек с зеленым цветом
        M = cv.moments(cnt)
        if M["m00"] != 0:
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            print("Координаты точки с зеленым цветом: ({}, {})".format(x, y))

            


def draw_circles(image, coordinates_list, radius=40, color=(0, 0, 255), thickness=5):
    for coord in coordinates_list:
        x, y = coord
        cv.circle(image, (x, y), radius, color, thickness)



def main():
   
    cv.imshow("Mask", mask)                        # Отображение маски 
                
    cv.namedWindow('image')                        
    cv.setMouseCallback("image", mouse_callback)

    print_()

    cv.imshow('image', img)                        # Отображение окна изображения

    cv.waitKey(0)
    cv.destroyAllWindows()    

main()