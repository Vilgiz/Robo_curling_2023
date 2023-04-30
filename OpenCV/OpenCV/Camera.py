
import cv2

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

        if ret:                                         # Проверки 
            return frame                                # получения 
        return None                                     # кадра




def main():                                             # тест
    Cap = Camera(1)

    while True:
        Frame = Cap.get_image()
        cv2.imshow('frame', Frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
main()

