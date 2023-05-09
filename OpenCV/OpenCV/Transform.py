import cv2 as cv
import numpy as np
from Camera import Camera

Cam = Camera(1)

def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Координата пикселя: ({x}, {y})")  

while True:
    
    img = Cam.get_image()

    # Получение размеров изображения
    m = 1
    height, width = (int(m*600), int(m*900)) 

    # Создание матрицы преобразования
    M = np.float32([[1, 0, width], [0, 1, 0]])

    # Применение преобразования
    img = cv.warpAffine(img, M, (width, height))


    # задаем координаты четырех углов прямоугольника на исходном изображении
    src_pts = np.float32([[0, 0], [img.shape[1], 0], [img.shape[1], img.shape[0]], [0, img.shape[0]]])

    # задаем координаты четырех углов прямоугольника на выходном изображении
    dst_pts = np.float32([[0, 0], [img.shape[1], 0], [img.shape[1]*0.8, img.shape[0]], [img.shape[1]*0.2, img.shape[0]]])

    # получаем матрицу преобразования
    M = cv.getPerspectiveTransform(src_pts, dst_pts)

    # применяем преобразование
    warped_img = cv.warpPerspective(img, M, (img.shape[1], img.shape[0]))

    cv.imshow('Original Image', img)
    cv.setMouseCallback("Original Image", mouse_callback)
    cv.imshow('Warped Image', warped_img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.waitKey(0)
cv.destroyAllWindows()
