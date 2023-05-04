import cv2
import numpy as np
from Camera import Camera

Cam = Camera(1)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        X = x
        Y = y
        print(f"Координата пикселя: ({x}, {y})")  
        return X,Y


while True:
    
    img = Cam.get_image()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)                  # Преобразование в HSV-пространство

    lower_red = np.array([0, 50, 50])                           # Определение диапазона красного цвета
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2        # Объединение двух масок

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)         # Нахождение контуров

    largest_contour = None                      # Нахождение наибольшего контура окружности
    largest_radius = 0
    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > largest_radius:
            largest_radius = radius
            largest_contour = contour

    if largest_contour is not None:                                         # Запись координат контура окружности
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        largest_contour_coords = (int(x), int(y))
        print(f"Центр красного круга ({x}, {y})")
        print(f"Радиус красного круга ({radius})")

    else:
        largest_contour_coords = None

    if largest_contour_coords is not None:
        user_coords = (100, 100)  # Replace with user-entered coordinates
        distance = cv2.pointPolygonTest(largest_contour, user_coords, True)
        if distance >= 0:
            print("User-entered coordinates are within the range of the largest circle contour")
        else:
            print("User-entered coordinates are not within the range of the largest circle contour")

    if largest_contour is not None:
        cv2.drawContours(img, [largest_contour], 0, (0, 255, 0), 2)
    cv2.imshow('image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cv2.destroyAllWindows()