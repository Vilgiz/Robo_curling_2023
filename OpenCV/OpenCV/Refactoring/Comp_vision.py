import cv2
import math
import numpy as np
from Camera import Camera
from Game_processor import Brain
import settings as config
#from machine_learning.machine_learning import Detecter

# !!!  Класс Vision представляет собой блядский швейцарский нож, который храт в себе туеву хучу всего
# !!!  и было бы мега классно в нем не так часто писать слово self. ---- хз, как это сделать

class COLOR_TEST():
    def __init__(self) -> None:
        self.lower = config.test_lower
        self.upper = config.test_upper


class COLOR_RED():
    def __init__(self) -> None:
        self.lower = config.red_lower
        self.upper = config.red_upper


class COLOR_YELL():
    def __init__(self) -> None:
        self.lower = config.yell_lower
        self.upper = config.yell_upper


class Vision():

    def __init__(self, COLOR) -> None:
        self.track_rocks = {}
        self.track_id = 0
        self.rocks_prev_frame = []
        self.rocks_curr_frame = []
        self.lower = COLOR.lower
        self.upper = COLOR.upper
        self.count = 0
        self.param1 = 1
        self.param2 = 0.29  # 0.43
        self.RED_ROCKS = []
        self.YELL_ROCKS = []
        #self.LR = Detecter()
        self.CV_color = True

    def Find_contors(self, frame, lower, upper):
        self.count += 1
        self.rocks_curr_frame = []
        self.rocks_curr_frame = []
        self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(self.gray, cv2.HOUGH_GRADIENT_ALT, 1, 75, param1=self.param1, param2=self.param2,
                                   minRadius=50, maxRadius=60)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            red_circles = []
            for i in circles[0, :]:
                red_circles.append((i[0], i[1], i[2]))
            for circle in red_circles:
                self.radius_cv = int(circle[2])
                x_cv = circle[0]
                y_cv = circle[1]
                self.center_cv = (x_cv, y_cv)
                self.rocks_curr_frame.append((int(x_cv), int(y_cv)))

    def Find_Rocks(self, frame):
        if self.count <= 2:
            for pt in self.rocks_curr_frame:
                for pt2 in self.rocks_prev_frame:
                    self.distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    if self.distance < 50:
                        self.track_rocks[self.track_id] = pt
                        self.track_id += 1
        else:
            self.track_rocks_copy = self.track_rocks.copy()
            self.rocks_curr_frame_copy = self.rocks_curr_frame.copy()

            for self.obj_id, pt2 in self.track_rocks_copy.items():
                self.obj_exists = False
                for pt in self.rocks_curr_frame_copy:
                    self.distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    if self.distance < 50:
                        self.track_rocks[self.obj_id] = pt
                        self.obj_exists = True
                        if pt in self.rocks_curr_frame:
                            self.rocks_curr_frame.remove(pt)
                            continue
                if not self.obj_exists:
                    self.track_rocks.pop(self.obj_id)
            for pt in self.rocks_curr_frame:
                self.track_rocks[self.track_id] = pt
                self.track_id += 1
        self.rocks_prev_frame = self.rocks_curr_frame.copy()
        self.__check()
        #self.__show_circle(frame)
        self.__Red_Yell_array(frame)
        #self.__show_circle(frame)
        cv2.imshow('frame', frame)
        #if self.count == 1:
            #cv2.createTrackbar('param1', 'frame', 1, 1000, self.__onChange1)   
            #cv2.createTrackbar('param2', 'frame', 1, 1000, self.__onChange2) 

    def __show_circle(self, frame):
        for self.obj_id, pt in self.track_rocks.items():
            self.center_cv = pt
            #res = self.LR.designate(self.hsv[pt[1],pt[0]].reshape(1, -1))
            #if res != -1:
            cv2.circle(frame, self.center_cv, self.radius_cv, (0, 255, 0), 3)
            cv2.circle(frame, self.center_cv, 3, (0, 0, 255), 3)
            cv2.putText(frame, str(self.obj_id),
                        (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
        cv2.imshow('Video', frame)

    def __trans_coord(self):
        self.track_rocks_temp = tuple(self.track_rocks.items())
        self.track_only_coord = []
        for i in self.track_rocks_temp:
            self.track_only_coord.append(i[1])

    def __check(self):
        self.__trans_coord()
        self.track_ROCKS = []
        for pip in range(len(self.track_only_coord)):
            if pip == len(self.track_only_coord) - 1:
                self.track_ROCKS.append(
                    [self.track_only_coord[pip][0], self.track_only_coord[pip][1]])
                break
            distance = math.sqrt((self.track_only_coord[pip][0] - self.track_only_coord[pip+1][1])**2 +
                                 (self.track_only_coord[pip][1] - self.track_only_coord[pip+1][1])**2)
            if distance > 5:
                self.track_ROCKS.append(
                    [self.track_only_coord[pip][0], self.track_only_coord[pip][1]])

    def __onChange1(self, value1):
        self.param1 = value1

    def __onChange2(self, value2):
        value2 = (value2 / 1000) - 0.001
        self.param2 = value2

    def __Red_Yell_array(self, frame):
        self.RED_ROCKS = []
        self.YELL_ROCKS = []
        for j in self.track_ROCKS:
            x, y = j
            pixel_color_HSV = self.hsv[y, x]
            pixel_color_RGB = self.RGB[y, x]

            if self.CV_color:
                tmp_array_HSV = pixel_color_HSV.astype(np.int64)
                tmp_array_RGB = pixel_color_RGB.astype(np.int64)
                if np.all(tmp_array_RGB > config.red_lower_RGB) and np.all(tmp_array_RGB < config.red_upper_RGB):
                    self.RED_ROCKS.append(j)
                    cv2.circle(frame, j, 55, (0, 255, 0), 3)
                elif np.all(tmp_array_HSV > config.yell_lower) and np.all(tmp_array_HSV < config.yell_upper):
                    self.YELL_ROCKS.append(j)
                    cv2.circle(frame, j, 55, (0, 255, 0), 3)
                    
            '''
            else:
                res = self.LR.designate(pixel_color.reshape(1, -1))
                if res == 1:
                    self.RED_ROCKS.append(j)
                elif res == 0:
                    self.YELL_ROCKS.append(j)
        '''
                


if __name__ == '__main__':
    
    import os
    #path = os.path.join(os.path.dirname(__file__),'machine_learning','datasets','1_Pro.mp4')
    #Cap = cv2.VideoCapture(path)

    camera = Camera()
    RED_COLOR = COLOR_RED()
    Vis_RED = Vision(RED_COLOR)
    #cap = cv2.VideoCapture(1)

    while True:
        #warped_image = camera.get_image()
        warped_image = camera.get_image()
        #cv2.imshow('Video', warped_image)
        cv2.waitKey(1)

        Vis_RED.Find_contors(warped_image, RED_COLOR.lower, RED_COLOR.upper)
        Vis_RED.Find_Rocks(warped_image)

        #brain = Brain()
        #temp1 = Vis_RED.RED_ROCKS
        #temp2 = Vis_RED.YELL_ROCKS
        print("RED")
        print(Vis_RED.RED_ROCKS)
        print("YELL")
        print(Vis_RED.YELL_ROCKS)

        """ brain.take_data(Robot=Vis_RED.YELL_ROCKS, Human=Vis_RED.RED_ROCKS)
        res = brain.solve()
        print(res)
        brain.draw_plt() """

    '''

    RED_COLOR = COLOR_RED()
    Vis_RED = Vision(RED_COLOR)
    import os
    path = os.path.join(os.path.dirname(__file__),'machine_learning','datasets','1_Pro.mp4')
    Cap = cv2.VideoCapture(path)
    _, frame = Cap.read()
    while _:
        _, frame = Cap.read()
        cv2.imshow('Video', frame)
        Vis_RED.Find_contors(frame, RED_COLOR.lower, RED_COLOR.upper)
        Vis_RED.Find_Rocks(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    '''