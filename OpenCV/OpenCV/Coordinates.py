
import cv2
import numpy as np
from Camera import Camera


Cap = Camera(1)

while True:
    Frame = Cap.get_image()

    height, width = Frame.shape[:2]
    center_x, center_y = int(width/2), int(height/2)

    M = np.float32([[1, 0, center_x - width/2], [0, 1, center_y - height/2]])        # Создание матрицы преобразования

    new_frame = np.zeros((height, width, 3), dtype=np.uint8)        # Создание нового изображения

    new_frame = cv2.warpAffine(new_frame, M, (width, height))        # Применение преобразования к новому изображению

    result = cv2.addWeighted(Frame, 1, new_frame, 1, 0)        # Наложение исходного изображения на новое изображение

    cv2.imshow('frame', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()