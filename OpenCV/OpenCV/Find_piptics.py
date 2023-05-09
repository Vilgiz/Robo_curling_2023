import cv2
import math
from Camera import Camera

Cap = Camera(1)

red_lower = (170, 50, 50)                                                           # Задаем диапазоны цветов для красного и синего цветов
red_upper = (180, 255, 255) 
blue_lower = (100, 160, 50)  
blue_upper = (140, 250, 160)

min_radius = 50                                                                     # Задаем минимальный и максимальный радиусы
max_radius = 100

track_red_pipticks = {}                                                             # МАССИВ С КРАСНЫМИ КАМНЯМИ
track_id = 0

red_pipticks_prev_frame = []                            
blue_pipticks_prev_frame = []

count = 0                                                                           # переменная-счетчик - количество кадров

while True:

    count += 1
    red_pipticks_current_frame = []
    blue_pipticks_current_frame = []


    frame = Cap.get_image()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                                     # Преобразуем изображение в цветовое пространство HSV

    red_mask = cv2.inRange(hsv, red_lower, red_upper)                               # Находим красные камни
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)                            # Находим синие камни
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in red_contours:                                                    # Отображаем контуры красных кругов на изображении
        (x_red, y_red), radius = cv2.minEnclosingCircle(contour)
        center = (int(x_red), int(y_red))
        radius = int(radius)
        if radius > min_radius and radius < max_radius:
            cv2.circle(frame, center, radius, (0, 0, 255), 2)
            red_pipticks_current_frame.append((int(x_red),int(y_red)))              # запись центра координат во фрейм

    for contour in blue_contours:                                                   # Отображаем контуры синих кругов на изображении
        (x_blue, y_blue), radius = cv2.minEnclosingCircle(contour)
        center = (int(x_blue), int(y_blue))
        radius = int(radius)
        if radius > min_radius and radius < max_radius:
            cv2.circle(frame, center, radius, (255, 0, 0), 2)                       
            blue_pipticks_current_frame.append((int(x_red),int(y_red)))             # запись центра координат во фрейм


    if count <= 2:
        for pt in red_pipticks_current_frame:
            for pt2 in red_pipticks_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                
                if distance < 20:                                                   # размер погрешности движения одного и того же объекта
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
                if distance < 20:                                                   # размер погрешности движения одного и того же объекта
                    track_red_pipticks[obj_id] = pt
                    obj_exists = True
                    red_pipticks_current_frame.remove(pt)
                    continue
                # Удаление id
            if not obj_exists:
                track_red_pipticks.pop(obj_id) # add list
                    
    for obj_id, pt in track_red_pipticks.items():
        cv2.circle(frame, center, 1, (0, 255, 0), -1)
        cv2.putText(frame, str(obj_id), (pt[0], pt[1] - 7), 0, 1, (0,0,255), 2)

    print("#################")
    print(track_red_pipticks)


    print("curr frame")
    print(red_pipticks_current_frame)

    cv2.imshow('frame', frame)                                                   
    
    red_pipticks_prev_frame = red_pipticks_current_frame.copy()
    blue_pipticks_prev_frame = blue_pipticks_current_frame.copy()
    
    cv2.waitKey(1)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()