﻿
import cv2
import math
from Camera import Camera
import numpy as np

Cap = Camera(0)
count = 0     


red_lower = (0, 140, 120)                                                            # Задаем диапазоны цветов для красного и синего цветов
red_upper = (10, 200, 255)  
blue_lower = (90, 70, 20)   
blue_upper = (120, 220, 100)

min_radius = 30                                                                 # Задаем минимальный и максимальный радиусы
max_radius = 1000

track_red_pipticks = {}                                                             # МАССИВ С КРАСНЫМИ КАМНЯМИ
track_id = 0

track_blue_pipticks = {}                                                            # МАССИВ С КРАСНЫМИ КАМНЯМИ
track_id_blue = 0

red_pipticks_prev_frame = []                            
blue_pipticks_prev_frame = []

count = 0                                                                           # переменная-счетчик - количество кадров
arg1 = 1
arg2 = 2

x_table = 400
y_table = 1300
ln = 310


class Find:
    def __init__(self):

        return 0
    
    def find_counters(self, red_lower, red_upper, blue_lower ,blue_upper):
        count += 1
        
        #red_lower = (0, 150, 150)                               # Задаем  
        #red_upper = (10, 200, 255)                              # диапазоны
        #blue_lower = (90, 70, 50)                               # цветов для
        #blue_upper = (115, 220, 100)                            # красного и синего 

        frame = Cap.get_image()                                  
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                                   
        red_mask = cv2.inRange(hsv, red_lower, red_upper)                              
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)                        
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return (red_contours, blue_contours)

    def find_piptics(self, min_radius, max_radius):

        track_red_pipticks = {}                                 # СЛОВАРЬ С КРАСНЫМИ КАМНЯМИ
        track_id = 0

        track_blue_pipticks = {}                                # СЛОВАРЬ С СИНИМИ КАМНЯМИ
        track_id_blue = 0

        red_pipticks_prev_frame = []                            
        blue_pipticks_prev_frame = []

        return 0 

    def reset_the_frame(self):
        red_pipticks_current_frame = []
        blue_pipticks_current_frame = []

        return 0
    
Find = Find()

Find.reset_the_frame()
Find.find_counters((0, 150, 150), (10, 200, 255), (90, 70, 50), (115, 220, 100))
Find.find_piptics(30, 1000)
    
while True:

    for contour in red_contours:                                                    # Отображаем контуры красных кругов на изображении
        (x_red, y_red), radius = cv2.minEnclosingCircle(contour)
        center_red = (int(x_red), int(y_red))
        radius = int(radius)
        if radius > min_radius and radius < max_radius:
            cv2.circle(frame, center_red, radius, (0, 0, 255), 2)
            red_pipticks_current_frame.append((int(x_red),int(y_red)))              # запись центра координат во фрейм



    for contour in blue_contours:                                                   # Отображаем контуры синих кругов на изображении
        (x_blue, y_blue), radius = cv2.minEnclosingCircle(contour)
        center_blue = (int(x_blue), int(y_blue))
        radius = int(radius)
        if radius > min_radius and radius < max_radius:
            cv2.circle(frame, center_blue, radius, (255, 0, 0), 2)                       
            blue_pipticks_current_frame.append((int(x_blue),int(y_blue)))           # запись центра координат во фрейм



    if count <= 2:
        for pt in red_pipticks_current_frame:
            for pt2 in red_pipticks_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                
                if distance < 70:                                                   # размер погрешности движения одного и того же объекта
                    track_red_pipticks[track_id] = pt
                    track_id += 1

    else: 
        track_red_pipticks_copy = track_red_pipticks.copy()
        red_pipticks_current_frame_copy = red_pipticks_current_frame.copy()

        for obj_id, pt2 in track_red_pipticks_copy.items():
            obj_exists = False
            for pt in red_pipticks_current_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                # Обновлениие позиции камня
                if distance < 30:                                                   # размер погрешности движения одного и того же объекта
                    track_red_pipticks[obj_id] = pt
                    obj_exists = True
                    if pt in red_pipticks_current_frame:
                        red_pipticks_current_frame.remove(pt)
                        continue
                # Удаление id
            if not obj_exists:
                track_red_pipticks.pop(obj_id) # add list
   
        for pt in red_pipticks_current_frame:
            track_red_pipticks[track_id] = pt
            track_id += 1

                
    for obj_id, pt in track_red_pipticks.items():
        cv2.circle(frame, center_red, 3, (0, 255, 0), -1)
        cv2.putText(frame, str(obj_id), (pt[0], pt[1] - 7), 0, 1, (0,0,255), 2)


########################################################################################### 


    if count <= 2:
        for pt_blue in blue_pipticks_current_frame:
            for pt2_blue in blue_pipticks_prev_frame:
                distance_blue = math.hypot(pt2_blue[0] - pt_blue[0], pt2_blue[1] - pt_blue[1])
                
                if distance_blue < 70:                                              # размер погрешности движения одного и того же объекта
                    track_blue_pipticks[track_id_blue] = pt_blue
                    track_id_blue += 1

    else: 
        track_blue_pipticks_copy = track_blue_pipticks.copy()
        blue_pipticks_current_frame_copy = blue_pipticks_current_frame.copy()

        for obj_id_blue, pt2_blue in track_blue_pipticks_copy.items():
            obj_exists_blue = False
            for pt_blue in blue_pipticks_current_frame_copy:
                distance_blue = math.hypot(pt2_blue[0] - pt_blue[0], pt2_blue[1] - pt_blue[1])
                # Обновлениие позиции камня
                if distance_blue < 30:                                              # размер погрешности движения одного и того же объекта
                    track_blue_pipticks[obj_id_blue] = pt_blue
                    obj_exists_blue = True
                    if pt_blue in blue_pipticks_current_frame:
                        blue_pipticks_current_frame.remove(pt_blue)
                        continue
                # Удаление id
            if not obj_exists_blue:
                track_blue_pipticks.pop(obj_id_blue) # add list
   
        for pt_blue in blue_pipticks_current_frame:
            track_blue_pipticks[track_id_blue] = pt_blue
            track_id_blue += 1

                
    for obj_id_blue, pt_blue in track_blue_pipticks.items():
        cv2.circle(frame, center_blue, 3, (0, 255, 255), -1)
        cv2.putText(frame, str(obj_id_blue), (pt_blue[0], pt_blue[1] - 7), 0, 1, (0,0,255), 2)





   
#######################################################################################

    #print("###########################")

    #print("RED PiPticks:")
    #print(track_red_pipticks)
    #print("BLUE PiPticks:")
    #print(track_blue_pipticks)

    #print("###########################")

    cv2.imshow('frame', frame)                                                   
    
    red_pipticks_prev_frame = red_pipticks_current_frame.copy()
    blue_pipticks_prev_frame = blue_pipticks_current_frame.copy()
   

    BLUE = tuple(track_blue_pipticks.items())
    RED = tuple(track_red_pipticks.items())
    print("Watch on your piptic 0_0")

    print("RED")
    print(RED)
    print("BLUE")
    print(BLUE)

    cv2.waitKey(1) 



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()