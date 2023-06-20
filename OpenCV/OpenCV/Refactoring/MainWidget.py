import ast
from PyQt6 import QtWidgets, QtGui
from ImageWidget import ImageWidget
from Robot import Robot
from GameThread import GameThread

class MainWidget(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        super().__init__()

        self.__init_logic()
        self.__init_manual_count()
        self.__init_window_parameters()
        self.__init_image_widget()
        self.__init_score()
        self.__init_controls()
        self.__init_difficulty()
                #self.robot_wins = 0
        #self.player_wins = 0
        try:
            with open("saved.txt", "r") as input:
                line = input.readline().replace("[", "").replace("]", "").split(',')#.write(str([self.rw_count, self.pw_count]))
                self.robot_wins = int(line[0])
                self.player_wins = int(line[1])
                self.lcd_rw.display(self.robot_wins)
                self.lcd_pw.display(self.player_wins)
        except : pass
        self.__init_layout()
        self.setLayout(self.main_layout)
        self.game.score_data.connect(self.__update_score)
        
    def __add_robot_win(self):
        self.robot_wins = self.robot_wins + 1
        self.lcd_rw.display(self.robot_wins)
        with open("saved.txt", "w") as output:
            output.write(str([self.robot_wins, self.player_wins]))
        pass

    def __add_player_win(self):
        self.player_wins = self.player_wins + 1
        self.lcd_pw.display(self.player_wins)
        with open("saved.txt", "w") as output:
            output.write(str([self.robot_wins, self.player_wins]))
        pass

    def __init_manual_count(self):
        self.mcg =   QtWidgets.QGroupBox("Ручной счётчик побед")
        self.mcgl = QtWidgets.QGridLayout()
        self.btn_rw = QtWidgets.QPushButton("Победа робота")
        #self.btn_rw.setFont(QtGui.QFont(self.fonts, 16))
        self.btn_rw.setMinimumHeight(200)
        #self.btn_rw.setFixedSize(100, 80)
        self.btn_rw.clicked.connect(self.__add_robot_win)
        self.lcd_rw = QtWidgets.QLCDNumber()
        self.lcd_rw.setDigitCount(3)
        self.btn_pw = QtWidgets.QPushButton("Победа человека")
        #self.btn_pw.setFont(QtGui.QFont(self.fonts, 16))
        self.btn_pw.setMinimumHeight(200)
        # self.btn_pw.setFixedSize(100, 80)
        self.btn_pw.clicked.connect(self.__add_player_win)
        self.lcd_pw = QtWidgets.QLCDNumber()
        self.lcd_pw.setDigitCount(3)
        self.mcgl.addWidget(self.btn_rw, 0,0)
        self.mcgl.addWidget(self.btn_pw, 0,1)
        self.mcgl.addWidget(self.lcd_rw, 1,0)
        self.mcgl.addWidget(self.lcd_pw, 1,1)
        #lay.addWidget(btn_pw)
        #self.mcg.setFont(QtGui.QFont(self.fonts, 16))
        self.mcg.setLayout(self.mcgl)

    def __init_difficulty(self):
        self.difficulty_group = QtWidgets.QGroupBox("Сложность")
        self.difficulty_group_layout = QtWidgets.QHBoxLayout()
        self.difficulty_box = QtWidgets.QComboBox()
        self.difficulty_box.addItems(['Легко', 'Средне', 'Сложно']) 
        self.difficulty_group.setFont = QtGui.QFont('Comic Sans MS', 25)
        self.difficulty_group_layout.addWidget(self.difficulty_box)
        self.difficulty_group.setLayout(self.difficulty_group_layout)
        self.difficulty_group.setMaximumHeight(80)
        self.difficulty_box.setCurrentIndex(2)


    def __init_logic(self):
        self.robot = Robot(print_debug = True)
        self.robot.start()
        self.game = GameThread()

    def send_step_to_robot(self):      
        try:
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
        except Exception as e:
            pass
            # cv2.line(warped_image, (100, 230), (2000, 230), (255, 255, 0), 1)
            # cv2.line(warped_image, (100, 350), (2000, 350), (255, 255, 0), 1)
            # cv2.line(warped_image, (100, 470), (2000, 470), (255, 255, 0), 1)
            # cv2.line(warped_image, (100, 590), (2000, 590), (255, 255, 0), 1)
            # cv2.line(warped_image, (100, 720), (2000, 720), (255, 255, 0), 1)
    def send_throw1_to_robot(self):
        step_data = ((250, 100), (249, 1250), [2])
        self.robot.send_step(step_data)
        self.game.last_start_coordinates = (250, 100)
        self.game.last_stop_coordinates = (249, 2000)
        self.game.last_color = (255, 255, 0)
        print('Master: ', step_data)

    def send_throw2_to_robot(self):
        step_data = ((350, 100), (349, 1250), [2])
        self.robot.send_step(step_data)
        self.game.last_start_coordinates = (350, 100)
        self.game.last_stop_coordinates = (349, 2000)
        self.game.last_color = (255, 255, 0)
        print('Master: ', step_data)

    def send_throw3_to_robot(self):
        step_data = ((470, 100), (469, 1250), [2])
        self.robot.send_step(step_data)
        self.game.last_start_coordinates = (470, 100)
        self.game.last_stop_coordinates = (469, 2000)
        self.game.last_color = (255, 255, 0)
        print('Master: ', step_data)

    def send_throw4_to_robot(self):
        step_data = ((590, 100), (589, 1250), [2])
        self.robot.send_step(step_data)
        self.game.last_start_coordinates = (590, 100)
        self.game.last_stop_coordinates = (589, 2000)
        self.game.last_color = (255, 255, 0)
        print('Master: ', step_data)

    def send_throw5_to_robot(self):
        step_data = ((720, 100), (719, 1250), [2])
        self.robot.send_step(step_data)
        self.game.last_start_coordinates = (720, 100)
        self.game.last_stop_coordinates = (719, 2000)
        self.game.last_color = (255, 255, 0)
        print('Master: ', step_data)

    def __init_controls(self):
        self.make_step_button = QtWidgets.QPushButton("АВТОХОД")
        self.make_step_button.setFixedSize(700, 300)
        self.make_step_button.setFont(QtGui.QFont(self.fonts, 16))
        self.make_step_button.clicked.connect(self.send_step_to_robot)
        pass
        self.throw1_button = QtWidgets.QPushButton("ЧИСТКА1")
        self.throw1_button.setFixedSize(120, 200)
        self.throw1_button.setFont(QtGui.QFont(self.fonts, 16))
        self.throw1_button.clicked.connect(self.send_throw1_to_robot)
        pass
        self.throw2_button = QtWidgets.QPushButton("ЧИСТКА2")
        self.throw2_button.setFixedSize(120, 200)
        self.throw2_button.setFont(QtGui.QFont(self.fonts, 16))
        self.throw2_button.clicked.connect(self.send_throw2_to_robot)
        pass
        self.throw3_button = QtWidgets.QPushButton("ЧИСТКА3")
        self.throw3_button.setFixedSize(120, 200)
        self.throw3_button.setFont(QtGui.QFont(self.fonts, 16))
        self.throw3_button.clicked.connect(self.send_throw3_to_robot)
        pass
        self.throw4_button = QtWidgets.QPushButton("ЧИСТКА4")
        self.throw4_button.setFixedSize(120, 200)
        self.throw4_button.setFont(QtGui.QFont(self.fonts, 16))
        self.throw4_button.clicked.connect(self.send_throw4_to_robot)
        pass
        self.throw5_button = QtWidgets.QPushButton("ЧИСТКА5")
        self.throw5_button.setFixedSize(120, 200)
        self.throw5_button.setFont(QtGui.QFont(self.fonts, 16))
        self.throw5_button.clicked.connect(self.send_throw5_to_robot)
        self.throw_group = QtWidgets.QGroupBox("ЧИСТКА")
        self.throw_group_layout = QtWidgets.QHBoxLayout()
        self.throw_group_layout.addWidget(self.throw1_button)
        self.throw_group_layout.addWidget(self.throw2_button)
        self.throw_group_layout.addWidget(self.throw3_button)
        self.throw_group_layout.addWidget(self.throw4_button)
        self.throw_group_layout.addWidget(self.throw5_button)
        self.throw_group.setLayout(self.throw_group_layout)


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
        self.left_widget.addWidget(self.mcg)
        self.right_widget = QtWidgets.QVBoxLayout()
        
        self.right_widget.addWidget(self.score_group)
        self.right_widget.addWidget(self.make_step_button)
        self.right_widget.addWidget(self.throw_group)
        self.right_widget.addWidget(self.difficulty_group)

        self.right_widget.setSpacing (0)
        self.right_widget.setContentsMargins (0, 0, 0, 0)

        self.main_layout.addLayout(self.left_widget)
        self.main_layout.addLayout(self.right_widget)

    def __init_image_widget(self):
        self.original_image_widget = ImageWidget()
        self.original_image_widget.setStyleSheet('background-color: #262626;')
        self.original_image_widget.setMinimumSize(800, 0)
        self.original_image_widget.setMaximumSize(800, 600)
        self.game.original_image_signal.connect(self.original_image_widget.image_data_slot)
        self.processed_image_widget = ImageWidget()
        self.processed_image_widget.setStyleSheet('background-color: #262626;')
        self.processed_image_widget.setMinimumSize(800, 0)
        self.processed_image_widget.setMaximumSize(800, 600)
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
