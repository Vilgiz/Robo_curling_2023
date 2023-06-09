import random
import cv2
import numpy as np
from Camera import Camera
from PyQt6 import QtCore

from Comp_vision import Vision, COLOR_RED, COLOR_TEST, COLOR_YELL
from ImageProcessor import ImageProcessor
from Game_processor import Brain
from Balli import Balli

import settings as glob_const

class GameThread(QtCore.QObject):
    original_image_signal = QtCore.pyqtSignal(np.ndarray)
    processed_image_signal = QtCore.pyqtSignal(np.ndarray)
    score_data = QtCore.pyqtSignal(str)
    #player_score_signal = QtCore.pyqtSignal(int)
    #cid = QtCore.pyqtSignal(np.ndarray) # Corrected image data
    #oid = QtCore.pyqtSignal(np.ndarray) # Original image data
    #hole_data = QtCore.pyqtSignal(str)
    #score_data = QtCore.pyqtSignal(str)

    def get_coordinates(self):
        self.brain.take_data(Human=self.Vis_RED.RED_ROCKS, Robot=self.Vis_RED.YELL_ROCKS)
        result = self.brain.solve()
        self.last_start_coordinates = result[0]
        self.last_stop_coordinates = result[1]
        if (result[2][0] == 0): self.last_color = (0,255,0)
        if (result[2][0] == 1): self.last_color = (0,255,255)
        if (result[2][0] == 1): self.last_color = (0,0,255)
        return result

    def __init_game_parameters(self):
        self.RED_COLOR = COLOR_RED()
        self.Vis_RED = Vision(self.RED_COLOR)
        self.ipi = ImageProcessor()
        self.brain = Brain()
        self.calib_list = []
        self.last_start_coordinates = (0, 0)
        self.last_stop_coordinates = (0, 0)
        self.last_color = (0, 255, 0)
        center = (470, 1250)

        radius_white_Circle = 30
        radius_green_Circle = 150
        radius_blue_Ring = 390
        radius_white_Ring = 270

        self.Red_scope = Balli(center, radius_white_Circle, radius_green_Circle, radius_blue_Ring, radius_white_Ring)
        self.Yellow_scope = Balli(center, radius_white_Circle, radius_green_Circle, radius_blue_Ring, radius_white_Ring)
        self.Red_scope.point = 0
        self.Yellow_scope.point = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_game_parameters()
        self.camera = Camera()        
        self.timer = QtCore.QBasicTimer()
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        self.Red_scope.point = 0
        self.Yellow_scope.point = 0
        # Capture frame
        frame = self.camera.get_image()
        if frame is not None:
            #self.original_image_signal.emit(frame)
            warped_image = self.ipi.perspective_correction(frame)
            self.Vis_RED.Find_contors(warped_image, self.RED_COLOR.lower, self.RED_COLOR.upper)
            self.Vis_RED.Find_Rocks(warped_image)
            #################################################! КРИНЖ !
            data_RED = []
            coef_x = 1 #1.051454
            coef_y = 1 #1.115044
            for point in self.Vis_RED.RED_ROCKS:
                x_p = point[1]
                y_p = point[0]
                x_p = int(x_p * coef_x)
                y_p = int(y_p * coef_y)
                data_RED.append([x_p, y_p])

            data_YELL = []
            for point in self.Vis_RED.YELL_ROCKS:
                x_p = point[1]
                y_p = point[0]
                x_p = int(x_p * coef_x)
                y_p = int(y_p * coef_y)

                data_YELL.append([x_p, y_p])

            self.Vis_RED.RED_ROCKS = data_RED
            self.Vis_RED.YELL_ROCKS = data_YELL

            print("RED") 
            print(self.Vis_RED.RED_ROCKS)  
            print("YELL")  
            print(self.Vis_RED.YELL_ROCKS)

            if type(data_RED) == int:
                    print(self.Red_scope.point)
            else:
                    print(self.Red_scope.point)
                    for quantity in range (len(data_RED)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
                        self.Red_scope.Which_field(self.Red_scope.iteration_of_piptics(data_RED, quantity))
                    #print(Red_scope.point)

            if type(data_YELL) == int:
                    print(self.Yellow_scope.point)
            else:
                    print(self.Yellow_scope.point)
                    for quantity in range (len(data_YELL)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
                        self.Yellow_scope.Which_field(self.Yellow_scope.iteration_of_piptics(data_YELL, quantity))
                    #print(Blue_scope.point)
            start = (self.last_start_coordinates[1], self.last_start_coordinates[0])
            stop = (self.last_stop_coordinates[1], self.last_stop_coordinates[0])
            cv2.line(warped_image, start, stop, self.last_color, 8)
            self.processed_image_signal.emit(warped_image)
            self.score_data.emit(str([self.Yellow_scope.point, self.Red_scope.point]))
    def __del__(self):
        self.timer.stop()


if __name__ == '__main__':
    import sys
    from PyQt6 import QtWidgets, QtGui
    from ImageWidget import ImageWidget

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("КЁРЛИНГ ВЕРСИИ ОДИН ТОЧКА НОЛЬ")
    main_window.showMaximized()
    main_widget = ImageWidget()
    main_window.setCentralWidget(main_widget)
    main_window.showMaximized()
    game = GameThread()
    game.original_image_signal.connect(main_widget.image_data_slot)
    sys.exit(app.exec())

    self.game.oid.connect(self.oiw.image_data_slot)