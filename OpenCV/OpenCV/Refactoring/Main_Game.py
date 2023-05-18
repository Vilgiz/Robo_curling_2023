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

    Vis_YELL.Find_contors(frame, YELL_COLOR.lower, YELL_COLOR.upper)
    Vis_YELL.Find_Rocks(frame)

    cv2.waitKey(1)

    if Vis_RED.count % 20 == 0:
        while True:  
            print("RED")
            print(Vis_RED.track_ROCKS)        

            print("YELL")
            print(Vis_RED.track_ROCKS)        
            """ Red_scope.point = 0
            Blue_scope.point = 0 """

            """ data = pos_transformation(x_table, y_table, pixel_coord[0], 
                                          pixel_coord[1], pixel_coord[2], ln, BLUE_COORD_2, RED_COORD_2) """

            """ target = brain (data) 
            robot.send_step(target)
        
            
            RED_COORD = []

            for color_piptic in data:
                VR_BLUE_COORD = []
                VR_RED_COORD = []
                if color_piptic[0] == 2:
                    VR_RED_COORD.append(color_piptic[1])
                    VR_RED_COORD.append(color_piptic[2])
                    RED_COORD.append(VR_RED_COORD)
                else:
                    VR_BLUE_COORD.append(color_piptic[1])
                    VR_BLUE_COORD.append(color_piptic[2])
                    BLUE_COORD.append(VR_BLUE_COORD)
            

            if type(RED_COORD) == int:
                print(Red_scope.point)
            else:
                print(Red_scope.point)
                for quantity in range (len(RED_COORD)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
                    Red_scope.Which_field(Red_scope.iteration_of_piptics(RED_COORD, quantity))
            #print(Red_scope.point)

            if type(BLUE_COORD) == int:
                print(Blue_scope.point)
            else:
                print(Blue_scope.point)
                for quantity in range (len(BLUE_COORD)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
                    Blue_scope.Which_field(Blue_scope.iteration_of_piptics(BLUE_COORD, quantity))

            draw_plt(data, target)  """
            cv2.waitKey(0) 

            break 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

       