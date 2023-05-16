import cv2
import math

from Transform_2 import pos_transformation
from Game_logic import brain, draw_plt

from Robot import Robot
from Balli import Balli
from Camera import Camera
from Click import MouseCallback

robot = Robot(timeout=10, print_debug=True)
robot.start()
Cap = Camera(0)

frame = Cap.get_image()
call = MouseCallback("Frame Calibration")
call.get_points(frame)
pixel_coord = (call.points)

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


center = (400, 1100)

radius_white_Circle = 50
radius_green_Circle = 150
radius_blue_Ring = 260
radius_white_Ring = 370

Red_scope = Balli(center, radius_white_Circle, radius_green_Circle, radius_blue_Ring, radius_white_Ring)
Blue_scope = Balli(center, radius_white_Circle, radius_green_Circle, radius_blue_Ring, radius_white_Ring)

while True:

    count += 1
    red_pipticks_current_frame = []
    blue_pipticks_current_frame = []

    frame = Cap.get_image()                                  

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                                    # Преобразуем изображение в цветовое пространство HSV

    red_mask = cv2.inRange(hsv, red_lower, red_upper)                               # Находим красные камни
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)                            # Находим синие камни
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


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
    #print("Watch on your piptic 0_0")

    #print("RED")
    #print(RED)
    #print("BLUE")
    #print(BLUE)

    cv2.waitKey(1) 



    if count % 20 == 0:
        while True: 
            if (True):

                RED_COORD = []
                for pip in RED:
                    RED_COORD.append(pip[1])

                BLUE_COORD = []
                for pip in BLUE:
                    BLUE_COORD.append(pip[1])


                data = pos_transformation(x_table, y_table, pixel_coord[0], pixel_coord[1], pixel_coord[2], ln, RED_COORD, BLUE_COORD)
                print(data)

                target = brain (data) 
                robot.send_step(target)
                #print(target)
                
                BLUE_COORD = []
                RED_COORD = []



                for color_piptic in data:
                    VR_BLUE_COORD = []
                    VR_RED_COORD = []
                    if color_piptic[0] == 0:
                        VR_RED_COORD.append(color_piptic[1])
                        VR_RED_COORD.append(color_piptic[2])
                        RED_COORD.append(VR_RED_COORD)
                    else:
                        VR_BLUE_COORD.append(color_piptic[1])
                        VR_BLUE_COORD.append(color_piptic[2])
                        BLUE_COORD.append(VR_BLUE_COORD)


                print (RED_COORD)
                print (BLUE_COORD)

                if type(RED_COORD) == int:
                    print(Red_scope.point)
                else:
                    print(Red_scope.point)
                    for quantity in range (len(RED_COORD)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
                        Red_scope.Which_field(Red_scope.iteration_of_piptics(RED_COORD, quantity))
                    print(Red_scope.point)

                if type(BLUE_COORD) == int:
                   print(Blue_scope.point)
                else:
                    for quantity in range (len(BLUE_COORD)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
                        Blue_scope.Which_field(Blue_scope.iteration_of_piptics(BLUE_COORD, quantity))
                    print(Blue_scope.point)

                draw_plt(data, target) 
                cv2.waitKey(0) 

                break



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
