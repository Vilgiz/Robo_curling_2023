from Click import MouseCallback
from Camera import Camera
import cv2
import numpy as np


camera = Camera(0)
frame = camera.get_image()

call = MouseCallback("Frame Calibration")
call.get_points(frame)
print(call.points)

