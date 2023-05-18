import math
import cv2
import numpy as np
import os
import json
from Camera import Camera

class Marker():
    def __init__(self, id, center, corners):
        self.id = id
        self.center = center
        [self.topLeft, self.topRight, self.bottomRight, self.bottomLeft] = corners

class ImageProcessor():
    def __init__(self):
        if os.path.isfile('processor.json'):
            self.__load_settings()
        else:
            self.__load_defaults()

    def __load_defaults(self):
        self.rotation_angle = 0
        self.rotation_matrix = None
        self.save_settings()

    def __load_settings(self):
        with open('processor.json', 'r') as file:
            config = json.load(file)
        self.rotation_angle = config['rotation_angle']

    def save_settings(self):
        config = {}
        config['rotation_angle'] = self.rotation_angle

        with open('processor.json', 'w') as f:
            json.dump(config, f)

    def __detectArucoMarkers(self, image):
        markers = {}
        arucoDictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        arucoParameters = cv2.aruco.DetectorParameters()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDictionary, parameters=arucoParameters)

        if len(corners) != 3:
            print('[ERROR] Could not find all three markers')
            return None
        
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = [int(topRight[0]), int(topRight[1])]
            bottomRight = [int(bottomRight[0]), int(bottomRight[1])]
            bottomLeft = [int(bottomLeft[0]), int(bottomLeft[1])]
            topLeft = [int(topLeft[0]), int(topLeft[1])]
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            print("[INFO] ArUco marker ID: {}".format(markerID))
            markers[markerID] = Marker(markerID, [cX, cY], [topLeft, topRight, bottomRight, bottomLeft])
        return markers

    def __get_rotaion_matrix(self, markers):
        marker1 = markers[1]
        marker2 = markers[2]
        marker3 = markers[3]
        self.rotation_angle = -math.atan((marker2.topRight[0] - marker1.topRight[0])/(marker2.topRight[1] - marker1.topRight[1]))
        self.rotation_matrix = cv2.getRotationMatrix2D(self.image_center, self.rotation_angle*180/math.pi, 1.0)


    def aruco_calibration(self, image):
        #image = image.copy()
        self.image_center =[(image.shape[1]-1)/2.0, (image.shape[0]-1)/2.0] 

        markers = self.__detectArucoMarkers(image)
        if type(markers) is not type(None):
            self.__get_rotaion_matrix(markers)
            for marker in markers:
                marker = markers[marker]
                cv2.circle(image, marker.topRight, 4, (0, 0, 255), -1)

    def warp(self, image):
        image = image.copy()
        cos_rm = np.abs(self.rotation_matrix[0][0])
        sin_rm = np.abs(self.rotation_matrix[0][1])    
        new_height = int((image.shape[1] * sin_rm) + (image.shape[0] * cos_rm))
        new_width = int((image.shape[1] * cos_rm) +  (image.shape[0] * sin_rm))
        self.rotation_matrix[0][2] += (new_width/2) - self.image_center[0]
        self.rotation_matrix[1][2] += (new_height/2) - self.image_center[1]
        warped_image = cv2.warpAffine(
            image, self.rotation_matrix, (new_width, new_height))

        cv2.namedWindow('h', flags=cv2.WINDOW_AUTOSIZE)
        cv2.imshow('h', warped_image)

        
        markers = self.__detectArucoMarkers(warped_image)
        warped_image = warped_image[markers[1].topRight[1]:-1, markers[1].topRight[0]:-1]
        cv2.namedWindow('g', flags=cv2.WINDOW_AUTOSIZE)
        cv2.imshow('g', warped_image)
        cv2.waitKey(100)
        pass

if __name__ == '__main__':
    ip = ImageProcessor()
    import cv2
    import sys
    Cap = Camera()

    while True:
        frame = Cap.get_image()
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  
            ip.aruco_calibration(frame)
            ip.warp(frame)
            #break