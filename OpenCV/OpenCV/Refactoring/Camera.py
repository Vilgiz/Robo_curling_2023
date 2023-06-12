
import cv2
import json
import os.path

class Camera:
    
    def __init__(self):
        if os.path.isfile('camera.json'):
            self.__load_settings()
        else:
            self.__load_defaults()
        self.__camera = self.__camera_init()

    def __load_defaults(self):
        self.id = 0
        self.resolution = [1920, 1080]
        self.save_settings()

    def __load_settings(self):
        with open('camera.json', 'r') as file:
            config = json.load(file)
        self.id = config['id']
        self.resolution = config['resolution']

    def __camera_init(self):
        camera = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # выключаем автофокус
        camera.set(cv2.CAP_PROP_FOCUS, 190)  # устанавливаем фокус на 50 см
        #camera.set(cv2.CAP_PROP_EXPOSURE, -5)
        print('Warming up the camera')
        for i in range(10):
            print('/|\\-'[i % 4]+'\r', end='')
            #_, frame = camera.read()
            cv2.waitKey(5)
        return camera

    def save_settings(self):
        config = {}
        config['id'] = self.id
        config['resolution'] = self.resolution

        with open('camera.json', 'w') as f:
            json.dump(config, f)

    def get_image(self):
        ret, frame = self.__camera.read()
        if ret:
            return frame
        return None
    
if __name__ == '__main__':
    camera = Camera()
    cv2.namedWindow('Test image', cv2.WINDOW_GUI_EXPANDED)
    while True:
        frame = camera.get_image()
        if type(frame) != None:
            cv2.imshow('Test image', frame)    
        cv2.waitKey(100)
