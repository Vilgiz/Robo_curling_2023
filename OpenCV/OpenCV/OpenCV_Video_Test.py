
from asyncio.windows_events import NULL
import cv2 as cv
from Camera import Camera

lower_red = (0, 50, 50)                 # Определение диапазона красного цвета в HSV
upper_red = (10, 255, 255)
lower_red2 = (170, 50, 50)
upper_red2 = (180, 255, 255)

cap = cv.VideoCapture(1)                # Настройка веб-камеры
Cam = Camera(1)

while True:

    ret, frame = cap.read()                 # Получение кадра с веб-камеры

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)            # Преобразование цветового пространства из BGR в HSV

    mask1 = cv.inRange(hsv, lower_red, upper_red)                   # Создание маски для красного цвета
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    contours, _ = cv.findContours( mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)     # Поиск контуров на маске
 
    cv.drawContours(frame, contours, -1, (0, 255, 0), 2)    # Отображение кадра с контурами
    cv.imshow('frame', frame)

    for c in contours:                                      # Вывод координат в консоль
        area = cv.contourArea(c)
        if area > 200:
            (x, y), radius = cv.minEnclosingCircle(c)
            if radius < 65:
                print("Координаты красной окружности: ({}, {})".format(int(x), int(y)))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()