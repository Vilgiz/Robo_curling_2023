import cv2
import numpy as np

# Создание объекта VideoCapture для захвата видео с веб-камеры
cap = cv2.VideoCapture(0)

while True:
    # Захват кадра с веб-камеры
    ret, frame = cap.read()

    # Преобразование кадра в цветовое пространство HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Определение диапазона красного цвета в HSV
    lower_red = (0, 160, 160)                                                         # Задаем диапазоны цветов для красного и синего цветов
    upper_red = (20, 255, 255)
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Применение размытия для уменьшения шума
    img_blur = cv2.GaussianBlur(mask, (5, 5), 0)


    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 250, param1=50, param2=30, minRadius=60, maxRadius=300)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        red_circles = []
        for i in circles[0, :]:
            red_circles.append((i[0], i[1], i[2]))
        for circle in red_circles:
            radius = circle[2]
            x = circle[0]
            y = circle[1]
            center = (x,y)
            cv2.circle(frame, center, radius, (0, 255, 0), 3)
            cv2.circle(frame, center, 3, (0, 0, 255), 3)



    # Отображение кадра с найденными кругами
    cv2.imshow('frame', frame)

    # Если нажата клавиша 'q', выход из цикла
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()