import cv2
import math
import numpy as np
import sys

from Camera import Camera
from Comp_vision import Vision, COLOR_RED, COLOR_TEST, COLOR_YELL
from ImageProcessor import ImageProcessor

import settings as glob_const

Cap = Camera()

RED_COLOR = COLOR_RED()

Vis_RED = Vision(RED_COLOR)

ipi = ImageProcessor()

calib_list = []

while True:
    frame = Cap.get_image()
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
            ipi.aruco_calibration(frame)
            #frame = ipi.warp(frame)
            ipi.save_settings()
            break
    if key == ord('w'):
            ipi.warp(frame)
    if key == ord('c'):
            calib_list.append(frame.copy())
            print(len(calib_list))
    if key == ord('b'):
            calib_list.clear()
            
print('tsssssssss')
warped_image = ipi.warp(frame)
cv2.imshow('warped_image', warped_image)


