import cv2
import math
import numpy as np

from Camera import Camera
import settings as glob_const

############# !!!  Класс Vision представляет собой блядский швейцарский нож, который храт в себе туеву хучу всего
############# !!!  и было бы мега классно в нем не так часто писать слово self. ---- хз, как это сделать

class COLOR_TEST():
    def __init__(self) -> None:
        self.lower = glob_const.test_lower
        self.upper = glob_const.test_upper

class COLOR_RED():
    def __init__(self) -> None:
        self.lower = glob_const.red_lower
        self.upper = glob_const.red_upper

class COLOR_YELL():
    def __init__(self) -> None:
        self.lower = glob_const.yell_lower
        self.upper = glob_const.yell_upper

class Vision():

    def __init__(self, COLOR) -> None:
        self.track_rocks = {}                                                       
        self.track_id = 0                                                      
        self.rocks_prev_frame = []                          
        self.rocks_curr_frame = []      
        self.lower = COLOR.lower
        self.upper = COLOR.upper
        self.count = 0  

    def Find_contors(self, frame, lower, upper):
        self.count += 1
        self.rocks_curr_frame = []
        self.rocks_curr_frame = []

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                                    
        Mask = cv2.inRange(hsv, lower, upper)                        
        Blur = cv2.GaussianBlur(Mask, (5, 5), 0)
        ## ! ПОМЕНЯТЬ, СУКА, НЕ ОТЛАЖЕНО !!!!!!!
        ## ! ПОМЕНЯТЬ, СУКА, НЕ ОТЛАЖЕНО !!!!!!!                                             
        """ circles = cv2.HoughCircles(Blur, cv2.HOUGH_GRADIENT, 1, glob_const.min_dist, 
                                    glob_const.accuracy, glob_const.sensitivity, 
                                    glob_const.min_radius, glob_const.max_radius) """
        ## ! ПОМЕНЯТЬ, СУКА, НЕ ОТЛАЖЕНО !!!!!!!
        ## ! ПОМЕНЯТЬ, СУКА, НЕ ОТЛАЖЕНО !!!!!!!
        circles = cv2.HoughCircles(Blur, cv2.HOUGH_GRADIENT, 1, 250, param1=50, param2=30, 
                                   minRadius=60, maxRadius=300)            
        ## ! ПОМЕНЯТЬ, СУКА, НЕ ОТЛАЖЕНО !!!!!!!
        ## ! ПОМЕНЯТЬ, СУКА, НЕ ОТЛАЖЕНО !!!!!!!
        if circles is not None:
            circles = np.uint16(np.around(circles))
            red_circles = []
            for i in circles[0, :]:
                red_circles.append((i[0], i[1], i[2]))
            for circle in red_circles:
                self.radius_cv = int(circle[2])
                x_cv = circle[0]
                y_cv = circle[1]
                self.center_cv = (x_cv,y_cv)
                self.rocks_curr_frame.append((int(x_cv),int(y_cv))) 

    def Find_Rocks(self, frame): 
        if self.count <= 2:
            for pt in self.rocks_curr_frame:
                for pt2 in self.rocks_prev_frame :
                    self.distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    
                    if self.distance < 50:                                              # размер погрешности движения одного и того же объекта
                        self.track_rocks[self.track_id] = pt
                        self.track_id += 1

        else: 
            self.track_rocks_copy = self.track_rocks.copy()
            self.rocks_curr_frame_copy = self.rocks_curr_frame.copy()

            for self.obj_id, pt2 in self.track_rocks_copy.items():
                self.obj_exists = False
                for pt in self.rocks_curr_frame_copy:
                    self.distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    # Обновлениие позиции камня
                    if self.distance < 50:                                              # размер погрешности движения одного и того же объекта
                        self.track_rocks[self.obj_id] = pt
                        self.obj_exists = True
                        if pt in self.rocks_curr_frame:
                            self.rocks_curr_frame.remove(pt)
                            continue
                    # Удаление id
                if not self.obj_exists:
                    self.track_rocks.pop(self.obj_id) # add list
    
            for pt in self.rocks_curr_frame:
                self.track_rocks[self.track_id] = pt
                self.track_id += 1

        for self.obj_id, pt in self.track_rocks.items():
            cv2.circle(frame, self.center_cv, self.radius_cv, (0, 255, 0), 3)
            cv2.circle(frame, self.center_cv, 3, (0, 0, 255), 3)
            cv2.putText(frame, str(self.obj_id), (pt[0], pt[1] - 7), 0, 1, (0,0,255), 2)

        cv2.imshow('frame',frame)                                                   
    
        self.rocks_prev_frame  = self.rocks_curr_frame.copy()
        pass