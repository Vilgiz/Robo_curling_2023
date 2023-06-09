from PyQt6 import QtWidgets, QtGui
from MainWidget import MainWidget

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.font = 'Comic Sans MS'
    main_window.setWindowTitle('НЕПРЕВЗОЙДЁННЫЙ РОБО-КЁРЛИНГ ВЕРСИИ 2.5.9.9')
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.showMaximized()

    sys.exit(app.exec())
