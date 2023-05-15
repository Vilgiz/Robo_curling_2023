
import cv2
from Camera import Camera
import numpy as np

class MouseCallback:
    
    def __init__(self, winname):
        self.winname = winname
        self.points = []
        cv2.namedWindow(self.winname)
        cv2.setMouseCallback(self.winname, self.on_mouse)

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))

    def get_points(self, image):
        self.points = []
        cv2.imshow(self.winname, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return np.array(self.points)
    

