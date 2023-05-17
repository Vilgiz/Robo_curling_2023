import cv2
import math
import numpy as np

from Camera import Camera
from Comp_vision import Vision, COLOR_RED, COLOR_TEST, COLOR_YELL

import settings as glob_const

Cap = Camera()
COLOR = COLOR_TEST()
Vis = Vision(COLOR)

print(Vis.rocks_curr_frame)
print("22")

while True:
    frame = Cap.get_image()
    Vis.Find_contors(frame, COLOR.lower, COLOR.upper)
    Vis.Find_Rocks()
    print(Vis.track_rocks)
    cv2.waitKey(1)
       