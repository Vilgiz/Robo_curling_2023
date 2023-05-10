from Game_logic import brain, draw_points_and_circles
import Find_piptics 
import cv2
import math
from Camera import Camera
from Transform_2 import pos_transformation

#from OpenCV_Photo_test import mouse_callback

Cap = Camera(1)

red_lower = (0, 160, 170)                                                           # Задаем диапазоны цветов для красного и синего цветов
red_upper = (10, 220, 210) 
blue_lower = (100, 150, 120)  
blue_upper = (120, 250, 180)

min_radius = 55                                                                     # Задаем минимальный и максимальный радиусы
max_radius = 100

track_red_pipticks = {}                                                             # МАССИВ С КРАСНЫМИ КАМНЯМИ
track_id = 0

track_blue_pipticks = {}                                                            # МАССИВ С КРАСНЫМИ КАМНЯМИ
track_id_blue = 0

red_pipticks_prev_frame = []                            
blue_pipticks_prev_frame = []

count = 0 

while (True):
    Red, Blue = Find_piptics.Find(Cap, red_lower, red_upper, blue_lower, blue_upper, min_radius, max_radius, count, 
             track_red_pipticks, track_id, track_blue_pipticks, track_id_blue, red_pipticks_prev_frame, 
             blue_pipticks_prev_frame)

    if cv2.waitKey(1) & 0xFF == ord('w'):
        data = pos_transformation (Red, Blue,[0,0])
        result = brain(data)
        print(Red, Blue)
        print (result)
        draw_points_and_circles(data, brain(data))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()