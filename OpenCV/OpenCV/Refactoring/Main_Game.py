import cv2
import math
import numpy as np

from Camera import Camera
from Comp_vision import Vision, COLOR_RED, COLOR_TEST, COLOR_YELL

import settings as glob_const

Cap = Camera()

RED_COLOR = COLOR_RED()
YELL_COLOR = COLOR_YELL()

Vis_RED = Vision(RED_COLOR)
Vis_YELL = Vision(YELL_COLOR)

while True:
    frame = Cap.get_image()

    Vis_RED.Find_contors(frame, RED_COLOR.lower, RED_COLOR.upper)
    Vis_RED.Find_Rocks(frame)
    print("RED")
    print(Vis_RED.track_rocks)

    Vis_YELL.Find_contors(frame, YELL_COLOR.lower, YELL_COLOR.upper)
    Vis_YELL.Find_Rocks(frame)
    print('YELL')
    print(Vis_YELL.track_rocks)

    cv2.waitKey(1)
       