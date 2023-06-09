from PyQt6 import QtWidgets, QtGui
from ImageWidget import ImageWidget

class MainWidget(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        super().__init__()
        self.__init_window_parameters()
        self.__init_image_widget()
        self.__init_layout()
        self.setLayout(self.main_layout)
        
    def __init_window_parameters(self):
        self.fonts = 'Comic Sans MS'
        self.windowTitle = 'НЕПРЕВЗОЙДЁННЫЙ РОБО-КЁРЛИНГ ВЕРСИИ 2.5.9.9'

    def __init_layout(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.left_widget = QtWidgets.QVBoxLayout()
        self.left_widget.addWidget(self.image_widget)

        self.right_widget = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("asdasdas")
        self.right_widget.addWidget(self.label)

        self.main_layout.addLayout(self.left_widget)
        self.main_layout.addLayout(self.right_widget)

    def __init_image_widget(self):
        self.image_widget = ImageWidget()
        self.image_widget.setStyleSheet('background-color: #262626;')


if __name__ == '__main__':
    import sys
    import cv2
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("КУЛЬБУТТО ВЕРСИИ ОДИН ТОЧКА НОЛЬ")
    main_widget = MainWidget()

    camera = cv2.VideoCapture(0)
    _, frame = camera.read()

    main_widget.image_widget.image_data_slot(frame)

    main_window.setCentralWidget(main_widget)
    main_window.showMaximized()

    sys.exit(app.exec())

# import ast
# from distutils.log import debug
# from functools import partial
# import sys
# import time
# from PyQt5 import QtCore
# from PyQt5 import QtWidgets, uic
# from PyQt5 import QtGui
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# from PyQt5.QtWidgets import (QWidget, QLCDNumber, QHBoxLayout,
#                              QLabel, QApplication, QGridLayout, QPushButton, QGroupBox)
# from PyQt5.QtCore import Qt
# from cv2 import COLOR_BGR2GRAY, cvtColor, equalizeHist, imshow, putText, waitKey,\
#     destroyAllWindows, destroyWindow,\
#     erode, dilate,\
#     WINDOW_GUI_EXPANDED, FONT_HERSHEY_PLAIN,\
#     VideoCapture, CAP_ANY, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
# import cv2
# import numpy as np

# from ImageWidget import ImageWidget
# #from Game import Game
# #from Robot import Robot


# class MainWidget(QtWidgets.QWidget):
#     def __init__(self,  parent=None):
#         # super().__init__(parent)
#         super().__init__()  # Call the inherited classes __init__ method
#         #self.robot = Robot(print_debug = True)
#         #self.robot.start()
#         self.fonts = "Comic Sans MS"
#         #self.game = Game(1)
#         #self.rw_count = 0
#         #Qself.pw_count = 0
        
#             #line
#         #uic.loadUi('basic.ui', self)  # Load the .ui file
        
#         self.__init_control_buttons()
#         self.__init_imshow()
#         self.__init_score()
#         self.__init_std_group()
#         self.__init_kick_group()
#         self.__init_manual_count()
#         # self.btn_start = QPushButton("START")
#         # self.btn_start.clicked.connect(partial(self.__send_command, None, None))
        
#         self.label = QLabel()
#         self.game.score_data.connect(self.__update_score)
#         main_layout = QtWidgets.QVBoxLayout()
#         qb = QtWidgets.QWidget()
#         qb_layout = QtWidgets.QHBoxLayout()
#         qb_layout.addWidget(self.std_group)
#         qb_layout.addWidget(self.kick_group)
#         qb_layout.addWidget(self.cgroup)
#         #qb_layout.addWidget(self.btn_random)
#         qb_layout.addWidget(self.psgroup)
#         qb_layout.addWidget(self.rsgroup)
#         qb.setLayout(qb_layout)
#         vid = QtWidgets.QWidget()
#         vid_layout = QtWidgets.QHBoxLayout()
#         vid_layout.addWidget(self.oiw)
#         vid_layout.addWidget(self.ciw)
#         vid_layout.addWidget(self.mcg)
#         vid.setLayout(vid_layout)


#         main_layout.addWidget(qb)
#         main_layout.addWidget(vid)
#         self.setLayout(main_layout)

#         try:
#             with open("saved.txt", "r") as input:
#                 line = input.readline().replace("[", "").replace("]", "").split(',')#.write(str([self.rw_count, self.pw_count]))
#                 self.rw_count = int(line[0])
#                 self.pw_count = int(line[1])
#                 self.lcd_rw.display(self.rw_count)
#                 self.lcd_pw.display(self.pw_count)
#         except : pass

#     def __rwadd(self):
#         self.rw_count = self.rw_count + 1
#         self.lcd_rw.display(self.rw_count)
#         with open("saved.txt", "w") as output:
#             output.write(str([self.rw_count, self.pw_count]))

#     def __pwadd(self):
#         self.pw_count = self.pw_count + 1
#         self.lcd_pw.display(self.pw_count)
#         with open("saved.txt", "w") as output:
#             output.write(str([self.rw_count, self.pw_count]))


#     def brightness_slider_changed(self):
#         self.game.set_correction_parameters(
#             self.brightness_trackbar.value(), self.contrast_trackbar.value())

#     def contrast_slider_changed(self):
#         self.game.set_correction_parameters(
#             self.brightness_trackbar.value(), self.contrast_trackbar.value())


#     def __init_manual_count(self):
#         self.mcg = QGroupBox("Ручной счётчик побед")
#         self.mcgl = QGridLayout()
#         self.btn_rw = QPushButton("Победа робота")
#         self.btn_rw.setMinimumHeight(200)
#         #self.btn_rw.setFixedSize(100, 80)
#         self.btn_rw.clicked.connect(self.__rwadd)
#         self.lcd_rw = QLCDNumber()
#         self.lcd_rw.setDigitCount(3)
#         self.btn_pw = QPushButton("Победа человека")
#         self.btn_pw.setMinimumHeight(200)
#         # self.btn_pw.setFixedSize(100, 80)
#         self.btn_pw.clicked.connect(self.__pwadd)
#         self.lcd_pw = QLCDNumber()
#         self.lcd_pw.setDigitCount(3)
#         self.mcgl.addWidget(self.btn_rw, 0,0)
#         self.mcgl.addWidget(self.btn_pw, 0,1)
#         self.mcgl.addWidget(self.lcd_rw, 1,0)
#         self.mcgl.addWidget(self.lcd_pw, 1,1)
#         #lay.addWidget(btn_pw)
#         self.mcg.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))
#         self.mcg.setLayout(self.mcgl)

#     def __init_std_group(self):
#         all_index = ([(0, -2)], [(1, -1), (0, -1), (-1, -1)], [(2, 0), (1, 0),
#                      (0, 0), (-1, 0), (-2, 0)], [(1, 1), (0, 1), (-1, 1)], [(0, 2)])
#         def __robot_index(point): return (-point[0]+3, -point[1]+3)
#         self.std_group = QGroupBox("Просто кидаем шар")
#         self.std_grid = QGridLayout()
#         for line in all_index:
#             for index in line:
#                 index = __robot_index(index)
#                 button = QPushButton(f'{index[0]} {index[1]}')
#                 button.setFixedSize(100, 80)
#                 button.clicked.connect(partial(self.__send_command, index, 0))
#                 button.clicked.connect(self.btn_auto.setFocus)
#                 self.std_grid.addWidget(button, 6-index[0], index[1])
#         self.std_group.setLayout(self.std_grid)
#         self.std_group.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))

#     def __init_kick_group(self):
#         all_index = ([(0, -2)], [(1, -1), (0, -1), (-1, -1)], [(2, 0), (1, 0),
#                      (0, 0), (-1, 0), (-2, 0)], [(1, 1), (0, 1), (-1, 1)], [(0, 2)])
#         def __robot_index(point): return (-point[0]+3, -point[1]+3)
#         self.kick_group = QGroupBox("Выбиваем шар")
#         self.kick_grid = QGridLayout()
#         for line in all_index:
#             for index in line:
#                 index = __robot_index(index)
#                 button = QPushButton(f'{index[0]} {index[1]}')
#                 button.setFixedSize(100, 80)
#                 button.clicked.connect(partial(self.__send_command, index, 1))
#                 self.kick_grid.addWidget(button, 6-index[0], index[1])
#         self.kick_group.setLayout(self.kick_grid)
#         self.kick_group.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))

#     def __init_control_buttons(self):
#         self.cgrid = QGridLayout()
#         #
#         self.btn_auto = QPushButton("АВТОХОД")
#         self.btn_auto.setFixedSize(200, 200)
#         self.btn_auto.clicked.connect(self.__send_auto_command)
#         self.btn_auto.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))
#         self.cgrid.addWidget(self.btn_auto, 0, 0)
#         #
#         self.btn_random = QPushButton("РАНДОМ")
#         self.btn_random.setFixedSize(200, 200)
#         self.btn_random.clicked.connect(self.__send_random_command)
#         self.btn_random.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))
#         self.cgrid.addWidget(self.btn_random, 0, 1)
#         self.cgroup = QGroupBox("Автоигра")
#         self.cgroup.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))
#         self.cgroup.setLayout(self.cgrid)
#         #
#         self.cgrid2 = QGroupBox("Куда бьём и как")
#         self.d1 = QLCDNumber()
#         self.d1.setDigitCount(1)
#         self.d2 = QLCDNumber()
#         self.d2.setDigitCount(1)
#         self.d3 = QLCDNumber()
#         self.d3.setDigitCount(1)
#         self.cgrid2l = QHBoxLayout()
#         self.cgrid2l.addWidget(self.d1)
#         self.cgrid2l.addWidget(self.d2)
#         self.l = QLabel()
#         self.cgrid2l.addWidget(self.l)
#         self.cgrid2l.addWidget(self.d3)
#         self.cgrid2.setLayout(self.cgrid2l)
#         self.cgrid2.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))
#         #
#         self.cgrid.addWidget(self.cgrid2, 1, 0, 1, 2)


#     def __update_score(self, score):
#         score = ast.literal_eval(score)
#         self.ps.display(score[0])
#         self.rs.display(score[1])
#         pass

#     def __init_score(self):
#         self.psgroup = QGroupBox("Очки игрока:")
#         self.ps = QLCDNumber()
#         self.ps.setDigitCount(3)
#         self.psgl = QHBoxLayout()
#         self.psgl.addWidget(self.ps)
#         self.psgroup.setLayout(self.psgl)
#         self.psgroup.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))
#         pass
#         self.rsgroup = QGroupBox("Очки робота:")
#         self.rs = QLCDNumber()
#         self.rs.setDigitCount(3)
#         self.rsgl = QHBoxLayout()
#         self.rsgl.addWidget(self.rs)
#         self.rsgroup.setLayout(self.rsgl)
#         self.rsgroup.setFont(QtGui.QFont(self.fonts, 16, QtGui.QFont.Bold))

#     def __init_imshow(self):
#         self.oiw = ImShowWidget()
#         self.ciw = ImShowWidget()
#         self.game.oid.connect(self.oiw.image_data_slot)
#         self.game.cid.connect(self.ciw.image_data_slot)

#     def __send_command(self, id, speed):
#         if id is None and speed is None: 
#             self.robot.send_start()
#         self.d1.display(id[0])
#         self.d2.display(id[1])
#         self.d3.display(speed)
#         self.robot.send_step(id, speed)

#     def __send_auto_command(self):
#         hole = self.game.get_hole()
#         self.d1.display(hole[0][0])
#         self.d2.display(hole[0][1])
#         self.d3.display(hole[1])
#         self.robot.send_step(hole[0], hole[1])

#     def __send_random_command(self):
#         hole = self.game.get_random_hole()
#         self.d1.display(hole[0][0])
#         self.d2.display(hole[0][1])
#         self.d3.display(hole[1])
#         self.robot.send_step(hole[0], hole[1])

# def closeEvent(event):
#     #main_widget.robot.stop()
#     del main_widget.robot 
#     del main_widget.game

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)

#     main_window = QtWidgets.QMainWindow()
#     main_window.setWindowTitle("КУЛЬБУТТО ВЕРСИИ ОДИН ТОЧКА НОЛЬ")
#     main_widget = MainWidget()
#     main_window.setCentralWidget(main_widget)
#     main_window.showMaximized()
#     main_window.closeEvent = closeEvent

#     sys.exit(app.exec_())