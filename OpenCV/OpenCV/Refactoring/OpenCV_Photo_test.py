
from colorsys import hsv_to_rgb
import cv2 as cv
import cv2
import numpy
from Camera import Camera


Cam = Camera()
frame = Cam.get_image()

img = frame
img = cv.medianBlur(img, 9)
# img = cv.imread("C:\\Users\Vilgi\Desktop\sdsdw.jpg")   # Загружаем изображение


# red_lower = (160, 50, 50)                # Задаем диапазоны цветов для красного и синего цветов
# red_upper = (190, 255, 255)

""" lower_green = (0, 160, 160)                 # Задаем диапазоны цветов для красного и синего цветов
upper_green = (20, 255, 255) """

# Определение диапазона нужного цвета в HSV
lower_green = (140, 100, 0)
upper_green = (255, 255, 160)
# Yelow hsv
lower_green = (15, 60, 100)  # (90, 70, 20)
upper_green = (100, 255, 255)  # (120, 220, 100)

#reg rgb
# lower_green = (100, 0, 0)
# upper_green = (255, 100, 100)
# # Преобразование изображения в цветовую модель HSV

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Создание маски для зеленого цвета
mask = cv.inRange(hsv, lower_green, upper_green)

# Нахождение контуров на маске
contours, hierarchy = cv.findContours(
    mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_color = hsv[y, x]
        # Вывод координат точек в HSV
        print(f"Цвет пикселя ({x}, {y}): {pixel_color}")
        return (x, y)


def print_():

    for c in contours:
        area = cv.contourArea(c)
        if area > 200:
            (x, y), radius = cv.minEnclosingCircle(c)
            if radius > 50:
                print("Координаты красной окружности: ({}, {})".format(
                    int(x), int(y)))


def draw_circles(image, coordinates_list, radius=40, color=(0, 0, 255), thickness=5):
    for coord in coordinates_list:
        x, y = coord
        cv.circle(image, (x, y), radius, color, thickness)


def main():

    # Отображение маски
    cv.imshow("Mask", mask)

    cv.namedWindow('image')
    cv.setMouseCallback("Mask", mouse_callback)

    print_()

    # Отображение окна изображения
    cv.imshow('image', img)

    cv.waitKey(0)
    cv.destroyAllWindows()

    cap = cv.VideoCapture(0)


main()
