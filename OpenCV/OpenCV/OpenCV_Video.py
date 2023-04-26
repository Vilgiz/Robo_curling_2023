
import cv2 as cv

# Определение диапазона красного цвета в HSV
lower_red = (0, 50, 50)
upper_red = (10, 255, 255)
lower_red2 = (170, 50, 50)
upper_red2 = (180, 255, 255)

# Настройка веб-камеры
cap = cv.VideoCapture(1)

while True:
    # Получение кадра с веб-камеры
    ret, frame = cap.read()

    # Преобразование цветового пространства из BGR в HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Создание маски для красного цвета
    mask1 = cv.inRange(hsv, lower_red, upper_red)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Поиск контуров на маске
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Отображение кадра с контурами 
    cv.drawContours(frame, contours, -1, (0, 0, 255), 2)
    cv.imshow('frame', frame)

    # Вывод координат в консоль
    for c in contours:
        area = cv.contourArea(c)
        if area > 200:
            (x, y), radius = cv.minEnclosingCircle(c)
            if radius > 10:
                print("Координаты красной окружности: ({}, {})".format(int(x), int(y)))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()