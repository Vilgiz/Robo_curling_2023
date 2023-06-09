import cv2
import math
import numpy as np
import sys

from Robot import Robot
from Camera import Camera
from Comp_vision import Vision, COLOR_RED, COLOR_TEST, COLOR_YELL
from ImageProcessor import ImageProcessor
from Game_processor import Brain

import settings as glob_const

Cap = Camera()

robot = Robot(timeout=10, print_debug=True)
robot.start()

RED_COLOR = COLOR_RED()

Vis_RED = Vision(RED_COLOR)

ipi = ImageProcessor()

brain = Brain()

calib_list = []

while True:
    frame = Cap.get_image()
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        ipi.aruco_calibration(frame)
        #frame = ipi.warp(frame, calibration = True)
        #ipi.save_settings()
        frame = ipi.perspective_correction(frame, calibration = True)
    if key == ord('c'):
        calib_list.append(frame.copy())
        print(len(calib_list))
    if key == ord('b'):
        calib_list.clear()
    if key == ord('u'):
        #warped_image = ipi.warp(frame)
        warped_image = ipi.perspective_correction(frame)
        Vis_RED.Find_contors(warped_image, RED_COLOR.lower, RED_COLOR.upper)
        Vis_RED.Find_Rocks(warped_image)
        #################################################! КРИНЖ !
        data_RED = []
        coef_x = 1 #1.051454
        coef_y = 1 #1.115044
        for point in Vis_RED.RED_ROCKS:
            x_p = point[1]
            y_p = point[0]
            #x_p *= ipi.scale
            #y_p *= ipi.scale
            #x_p = x_p + 20
            #y_p = y_p + 70
            x_p = int(x_p * coef_x)
            y_p = int(y_p * coef_y)
            data_RED.append([x_p, y_p]) #+15

        data_YELL = []
        for point in Vis_RED.YELL_ROCKS:
            x_p = point[1]
            y_p = point[0]
            #x_p *= ipi.scale
            #y_p *= ipi.scale
            #x_p = x_p + 20
            #7y_p = y_p + 70
            x_p = int(x_p * coef_x)
            y_p = int(y_p * coef_y)

            data_YELL.append([x_p, y_p]) #+15

        Vis_RED.RED_ROCKS = data_RED
        Vis_RED.YELL_ROCKS = data_YELL
        #################################################! КРИНЖ !
        brain = Brain() 
        print("RED") 
        print(Vis_RED.RED_ROCKS)  
        print("YELL")  
        print(Vis_RED.YELL_ROCKS)
    if key == ord('i'):
        brain.take_data(Robot=Vis_RED.RED_ROCKS, Human=Vis_RED.YELL_ROCKS)
        res = brain.solve()
        if res != None:
            robot.send_step(res)
            print('Master: ', res)
            brain.draw_plt()
