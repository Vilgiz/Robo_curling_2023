
import cv2

class Camera:
    
    def __init__(self, camera_port = 1):                # ����������� ������ camera
        self.camera = self.__camera_init(camera_port)   # ������� ������ ������ ��� ������ ������ "__camera_init"

    def __camera_init(self, path):                      # �����, ������������ ��� �������� ������� ������ (path - ����� ��������� - 0, ��� ������� - 1 ������)

        camera = cv2.VideoCapture(path, cv2.CAP_ANY)    # ������ ����������� � ������ ������ camera   

        camera.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)     # ��������� 
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)     # ����������

        print('Warming up the camera')                  # 
        for i in range(10):                             # ���� ���
            print('/|\\-'[i % 4]+'\r', end='')          # "��������"
            _, frame = camera.read()                    # ������
            cv2.waitKey(100)                            #
        return camera                               


    def get_image(self):                                # ����� ������ ��� ��������� ����� �����������
        ret, frame = self.camera.read()                 # ��������� ����������� � ������ (ret - ������ �� �����������, frame - ������� ����) 

        if ret:                                         # �������� 
            return frame                                # ��������� 
        return None                                     # �����




def main():                                             # ����
    Cap = Camera(1)

    while True:
        Frame = Cap.get_image()
        cv2.imshow('frame', Frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
main()

