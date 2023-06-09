from PyQt6 import QtWidgets, QtGui
from cv2 import rotate
from imutils import resize

import numpy as np

class ImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self.rotation_type = None

    def image_data_slot(self, image_data):
        if self.rotation_type:
            image_data = rotate(image_data, self.rotation_type)
        image_data = resize(image_data, width=self.size().width())
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())
        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data, width, height,
                       bytesPerLine, QImage.Format.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def set_rotation_type(self, type):
        self.rotation_type = type

if __name__ == '__main__':
    import cv2
    import sys

    camera = cv2.VideoCapture(0)
    _, frame = camera.read()

    if not _:
        print('Failed to capture frame')
        exit(-1)
    
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("Test window")
    main_widget = ImageWidget()
    main_widget.set_rotation_type(cv2.ROTATE_90_COUNTERCLOCKWISE)
    main_window.setCentralWidget(main_widget)
    main_window.showMaximized()
    main_widget.image_data_slot(frame)

    main_window.show()
    exit(app.exec())