
from colorsys import hsv_to_rgb
import cv2 as cv
import numpy
from Camera import Camera


Cam = Camera(1)
frame = Cam.get_image()

img = frame
#img = cv.imread("C:\\Users\Vilgi\Desktop\sdsdw.jpg")   # Загружаем изображение


#red_lower = (160, 50, 50)                                                           # Задаем диапазоны цветов для красного и синего цветов
#red_upper = (190, 255, 255) 

 
lower_green = (0, 140, 120)                          # Определение диапазона нужного цвета в HSV
upper_green = (10, 200, 255)  


hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)              # Преобразование изображения в цветовую модель HSV

mask = cv.inRange(hsv, lower_green, upper_green)       # Создание маски для зеленого цвета

contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)    # Нахождение контуров на маске



def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_color = hsv[y, x]
        print(f"Цвет пикселя ({x}, {y}): {pixel_color}")     #  Вывод координат точек в HSV
        return(x,y)


def print_():

    for c in contours:
        area = cv.contourArea(c)
        if area > 200:
            (x, y), radius = cv.minEnclosingCircle(c)
            if radius > 50:
                print("Координаты красной окружности: ({}, {})".format(int(x), int(y)))

            


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
    
    cap = cv.VideoCapture(0)


main()
