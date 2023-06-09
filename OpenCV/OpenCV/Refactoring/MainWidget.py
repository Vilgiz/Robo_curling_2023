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
