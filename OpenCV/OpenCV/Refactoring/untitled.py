

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel
import cv2
from Camera import Camera


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        self.Cap = Camera()
        self.capture = cv2.VideoCapture(0)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1304, 722)
        MainWindow.setStyleSheet("background-color: rgb(231, 222, 255);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        #self.label.setGeometry(QtCore.QRect(20, 10, 321, 251))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 280, 321, 241))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(360, 10, 291, 101))
        self.label_3.setObjectName("label_3")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(670, 10, 231, 101))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.pushButton_3.setStyleSheet("background-color: rgb(0, 255, 255);\n"
            "font-size: 16pt \"Bahnschrift Condensed\";\n"
            "\n"
            "")
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(910, 10, 381, 101))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 0, 0);\n"
            "font-size: 16pt \"Bahnschrift Condensed\";\n"
            "\n"
            "")
        self.pushButton_2.setObjectName("pushButton_2")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1304, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "Auto move"))
        self.label.setText(_translate("MainWindow", "Video"))
        self.label_2.setText(_translate("MainWindow", "Frame"))
        self.label_3.setText(_translate("MainWindow", "Score"))
        self.pushButton_3.setText(_translate("MainWindow", "Hand move"))

    def update_frame(self):
        frame = self.Cap.get_image()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
