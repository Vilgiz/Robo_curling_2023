
import cv2
""" 
class Camera:
    
    def __init__(self, camera_port = 1):                # Конструктор класса camera
        self.camera = self.__camera_init(camera_port)   # Создаем объект класса при помощи метода "__camera_init"

    def __camera_init(self, path):                      # Метод, используемый для создания объекта класса (path - выбор встроеной - 0, или внешней - 1 камеры)

        camera = cv2.VideoCapture(path, cv2.CAP_ANY)    # Захват видеопотока в объект класса camera   

        camera.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)     # Установка 
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)     # разрешения

        print('Warming up the camera')                  # 
        for i in range(10):                             # Цикл для
            print('/|\\-'[i % 4]+'\r', end='')          # "прогрева"
            _, frame = camera.read()                    # камеры
            cv2.waitKey(100)                            #
        return camera                               


    def get_image(self):                                # Метод класса для получения кадра изображения
        ret, frame = self.camera.read()                 # Получение изображения с камеры (ret - пришло ли изображение, frame - текущий кадр) 
        frame = cv2.flip(frame, 0)
        #frame = cv2.flip(frame, 1)
        if ret:                                         # Проверки 
            return frame                                # получения 
        return None                                     # кадра """
    



""" 
def main():                                             # тест
    Cap = Camera(1)

    while True:
        Frame = Cap.get_image()
        cv2.imshow('frame', Frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    Cap.release()
    cv2.destroyAllWindows()
    
main() """

""" import cv2
import json
import os.path

class Camera:
    
    def __init__(self):
        self.__load_defaults()
        self.__camera = self.__camera_init()

    def __load_defaults(self):
        self.id = 1
        self.resolution = [1920, 1080]
        self.save_settings()

    def __camera_init(self):
        camera = cv2.VideoCapture(self.id, cv2.CAP_ANY)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH,  self.resolution[1])
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[0])
        print('Warming up the camera')
        for i in range(10):
            print('/|\\-'[i % 4]+'\r', end='')
            _, frame = camera.read()
            cv2.waitKey(10)
        return camera

    def save_settings(self):
        config = {}
        config['id'] = self.id
        config['resolution'] = self.resolution

        with open('camera.json', 'w') as f:
            json.dump(config, f)

    def get_image(self):
        ret, frame = self.__camera.read()
        frame = cv2.flip(frame, 0)
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
 """


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
        #camera.set(cv2.CAP_PROP_FOCUS, 170)  # устанавливаем фокус на 50 см
        print('Warming up the camera')
        for i in range(10):
            print('/|\\-'[i % 4]+'\r', end='')
            _, frame = camera.read()
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
