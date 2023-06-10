import ast
from PyQt6 import QtWidgets, QtGui
from ImageWidget import ImageWidget
from Robot import Robot
from GameThread import GameThread

class MainWidget(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        super().__init__()
        self.__init_logic()
        self.__init_window_parameters()
        self.__init_image_widget()
        self.__init_score()
        self.__init_controls()
        self.__init_difficulty()
        self.__init_layout()
        self.setLayout(self.main_layout)
        self.game.score_data.connect(self.__update_score)
        
    def __init_difficulty(self):
        self.difficulty_group = QtWidgets.QGroupBox("Сложность")
        self.difficulty_group_layout = QtWidgets.QHBoxLayout()
        self.difficulty_box = QtWidgets.QComboBox()
        self.difficulty_box.addItems(['Легко', 'Средне', 'Сложно']) 
        self.difficulty_group.setFont = QtGui.QFont('Comic Sans MS', 25)
        self.difficulty_group_layout.addWidget(self.difficulty_box)
        self.difficulty_group.setLayout(self.difficulty_group_layout)
        self.difficulty_group.setMaximumHeight(80)


    def __init_logic(self):
        self.robot = Robot(print_debug = True)
        self.robot.start()
        self.game = GameThread()

    def send_step_to_robot(self):      
        if self.difficulty_box.currentIndex() == 0:
            easy_mode = True
            hard_mode = False
        if self.difficulty_box.currentIndex() == 1:
            easy_mode = False
            hard_mode = False
        if self.difficulty_box.currentIndex() == 2:
            easy_mode = False
            hard_mode = True
        step_data = self.game.get_coordinates(easy_mode, hard_mode)
        if step_data != None:
            self.robot.send_step(step_data)
            print('Master: ', step_data)
            #self.brain.draw_plt()
        pass

    def __init_controls(self):
        self.make_step_button = QtWidgets.QPushButton("АВТОХОД")
        self.make_step_button.setFixedSize(500, 500)
        self.make_step_button.setFont(QtGui.QFont(self.fonts, 16))
        self.make_step_button.clicked.connect(self.send_step_to_robot)
        pass

    def __init_score(self): 
        self.score_group = QtWidgets.QGroupBox("Счёт")
        self.score_group_layout = QtWidgets.QGridLayout()
        player_score_label = QtWidgets.QLabel("Игрок")
        player_score_label.setMaximumHeight(20)
        self.lcd_number_player = QtWidgets.QLCDNumber()
        self.lcd_number_player.digitCount = 3
        robot_score_label = QtWidgets.QLabel("Робот")
        robot_score_label.setMaximumHeight(20)
        self.lcd_number_robot = QtWidgets.QLCDNumber()
        self.lcd_number_robot.digitCount = 3
        self.score_group_layout.addWidget(player_score_label, 0, 0)
        self.score_group_layout.addWidget(robot_score_label, 0, 1)
        self.score_group_layout.addWidget(self.lcd_number_player, 1, 0)
        self.score_group_layout.addWidget(self.lcd_number_robot, 1, 1)
        self.score_group.setLayout(self.score_group_layout)
        self.score_group.setMaximumHeight(200)

    def __update_score(self, score):
        score = ast.literal_eval(score)
        self.lcd_number_robot.display(score[0])
        self.lcd_number_player.display(score[1])
       

    def __init_window_parameters(self):
        self.fonts = 'Comic Sans MS'
        self.windowTitle = 'НЕПРЕВЗОЙДЁННЫЙ РОБО-КЁРЛИНГ ВЕРСИИ 2.5.9.9'

    def __init_layout(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.left_widget = QtWidgets.QVBoxLayout()
        #self.left_widget.addWidget(self.original_image_widget)
        self.left_widget.addWidget(self.processed_image_widget)
        self.right_widget = QtWidgets.QVBoxLayout()
        
        self.right_widget.addWidget(self.score_group)
        self.right_widget.addWidget(self.make_step_button)
        self.right_widget.addWidget(self.difficulty_group)

        self.right_widget.setSpacing (0)
        self.right_widget.setContentsMargins (0, 0, 0, 0)

        self.main_layout.addLayout(self.left_widget)
        self.main_layout.addLayout(self.right_widget)

    def __init_image_widget(self):
        self.original_image_widget = ImageWidget()
        self.original_image_widget.setStyleSheet('background-color: #262626;')
        self.original_image_widget.setMinimumSize(1000, 0)
        self.original_image_widget.setMaximumSize(1000, 600)
        self.game.original_image_signal.connect(self.original_image_widget.image_data_slot)
        self.processed_image_widget = ImageWidget()
        self.processed_image_widget.setStyleSheet('background-color: #262626;')
        self.processed_image_widget.setMinimumSize(1000, 0)
        self.processed_image_widget.setMaximumSize(1000, 600)
        self.game.processed_image_signal.connect(self.processed_image_widget.image_data_slot)
        #self.game.cid.connect(self.ciw.image_data_slot)


if __name__ == '__main__':
    import sys
    import cv2
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("КЁРЛИНГ ВЕРСИИ ОДИН ТОЧКА НОЛЬ")
    main_widget = MainWidget()

    camera = cv2.VideoCapture(1)
    _, frame = camera.read()

    main_widget.original_image_widget.image_data_slot(frame)

    main_window.setCentralWidget(main_widget)
    main_window.showMaximized()

    sys.exit(app.exec())
