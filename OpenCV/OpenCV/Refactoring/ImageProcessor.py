import math
import cv2
import numpy as np
import os
import json
from Camera import Camera
import settings as config


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
        self.M = None
        self.save_settings()

    def __load_settings(self):
        with open('processor.json', 'r') as file:
            config = json.load(file)
        #self.rotation_angle = config['rotation_angle']
        #self.XOY = config['aruco_XOY']
        #self.scale = config['scale']
        try:
            self.M = np.array(config['rotation_matrix'])
        except Exception:
            self.M = None

    def save_settings(self):
        config = {}
        #config['rotation_angle'] = self.rotation_angle
        config['rotation_matrix'] = self.M.tolist()
        #config['aruco_XOY'] = self.XOY
        #config['scale'] = self.scale

        with open('processor.json', 'w') as f:
            json.dump(config, f)

    def __detectArucoMarkers(self, image):
        value = 0
        count = 0
        while value < 3:
            count +=1
            markers = {}
            arucoDictionary = cv2.aruco.getPredefinedDictionary(
                cv2.aruco.DICT_4X4_50)
            arucoParameters = cv2.aruco.DetectorParameters()
            (corners, ids, rejected) = cv2.aruco.detectMarkers(
                image, arucoDictionary, parameters=arucoParameters)
            value = len(corners) 

            if count > 10:
                print('[ERROR] Could not find all markers')
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
            markers[markerID] = Marker(
                markerID, [cX, cY], [topLeft, topRight, bottomRight, bottomLeft])
            
            self.markers_copy = markers.copy()
        return markers

    def __get_rotaion_matrix(self, markers):
        marker1 = markers[1]
        marker2 = markers[2]
        marker3 = markers[3]
        self.rotation_angle = -math.atan((marker2.topRight[0] - marker1.topRight[0])/(
            marker2.topRight[1] - marker1.topRight[1]))
        self.rotation_matrix = cv2.getRotationMatrix2D(
            self.image_center, self.rotation_angle*180/math.pi, 1.0)

    def chessboard_calibration(self, image_list):
        ch_x = 7
        ch_y = 7

        image, grayColor, threedpoints, twodpoints = self.__chess_processor(image_list, ch_x, ch_y)


        # cv2.destroyAllWindows()

        h, w = image.shape[:2]
        
        # Perform camera calibration by
        # passing the value of above found out 3D points (threedpoints)
        # and its corresponding pixel coordinates of the
        # detected corners (twodpoints)
        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            threedpoints, twodpoints, grayColor.shape[::-1], None, None)

        # Displaying required output
        print(" Camera matrix:")
        print(matrix)

        print("\n Distortion coefficient:")
        print(distortion)

        h,  w = image.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
            matrix, distortion, (w, h), 1, (w, h))

        # # undistort
        # dst = cv2.undistort(image, matrix, distortion, None, newcameramtx)
        # # crop the image
        # x, y, w, h = roi
        # dst = dst[y:y+h, x:x+w]

        # undistort
        
        mapx, mapy = cv2.initUndistortRectifyMap(
            matrix, distortion, None, newcameramtx, (w, h), 5)
        dst = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        
        cv2.imshow('calibresult',dst)
        cv2.waitKey(0)
        

    def __chess_processor(self, image_list, ch_x, ch_y):
         # image = image.copy()
        CHECKERBOARD = (ch_x, ch_y)
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 80, 0.0001)
        # Vector for 3D points
        threedpoints = []

        # Vector for 2D points
        twodpoints = []

        #  3D points real world coordinates
        objectp3d = np.zeros((1, CHECKERBOARD[0]
                              * CHECKERBOARD[1],
                              3), np.float32)
        objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
                                       0:CHECKERBOARD[1]].T.reshape(-1, 2)
        prev_img_shape = None

        for image in image_list:
            grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                grayColor, CHECKERBOARD,
                cv2.CALIB_CB_ADAPTIVE_THRESH
                + cv2.CALIB_CB_FAST_CHECK +
                cv2.CALIB_CB_NORMALIZE_IMAGE)

            if ret == True:
                threedpoints.append(objectp3d)
                corners2 = cv2.cornerSubPix(
                    grayColor, corners, (11, 11), (-1, -1), criteria)
                twodpoints.append(corners2)
                image = cv2.drawChessboardCorners(image,
                                                  CHECKERBOARD,
                                                  corners2, ret)
            

            #cv2.imshow('img', image)
            #cv2.waitKey(0)
        return(image, grayColor, threedpoints, twodpoints)

    def perspective_correction(self, image, calibration = False):
        h,  w = image.shape[:2]
        if calibration:
            markers = self.__detectArucoMarkers(image)
            cv2.circle(image, markers[1].bottomLeft, 3, (0, 0, 255), 3)
            cv2.circle(image, markers[2].bottomLeft, 3, (0, 255, 0), 3)
            cv2.circle(image, markers[3].bottomLeft, 3, (255, 0, 0), 3)
            cv2.circle(image, markers[0].bottomLeft, 3, (255, 0, 255), 3)
            cv2.imshow('detectresult',image)
            start_p = np.float32([markers[1].bottomLeft,markers[2].bottomLeft,
                                  markers[3].bottomLeft,markers[0].bottomLeft])
            dest_p = np.float32([[0,0],[1000,0],
                                 [1000,700],[0,700]])
            self.M = cv2.getPerspectiveTransform(start_p,dest_p)
            # Сохраняем М
            self.save_settings()
            result = cv2.warpPerspective(image, self.M,(w,h))
            cv2.imwrite('rez.png',result)
            cv2.imshow('calibresult',result)
        else:
            result = cv2.warpPerspective(image, self.M,(w,h))
            return(result)
        


    def aruco_calibration(self, image):
        # image = image.copy()
        self.image_center = [(image.shape[1]-1)/2.0, (image.shape[0]-1)/2.0]

        markers = self.__detectArucoMarkers(image)
        if type(markers) is not type(None):
            self.__get_rotaion_matrix(markers)
            for marker in markers:
                marker = markers[marker]
                cv2.circle(image, marker.topRight, 4, (0, 0, 255), -1)


            distance = math.sqrt((markers[1].center[0] - markers[3].center[0])**2 +
                                 (markers[1].center[1] - markers[3].center[1])**2)
        self.scale = config.millimetrs/distance
        self.warp(image, calibration = True)


    def warp(self, image, calibration = False):
        image = image.copy()
        rotation_matrix = self.rotation_matrix.copy()
        self.image_center = [(image.shape[1]-1)/2.0, (image.shape[0]-1)/2.0]
        if type(self.rotation_matrix) is type(None):
            cv2.namedWindow('h', flags=cv2.WINDOW_AUTOSIZE)
            cv2.imshow('h', image)
            print('Empty rotmat')
            return
        cos_rm = np.abs(rotation_matrix[0][0])
        sin_rm = np.abs(rotation_matrix[0][1])
        new_height = int((image.shape[1] * sin_rm) + (image.shape[0] * cos_rm))
        new_width = int((image.shape[1] * cos_rm) + (image.shape[0] * sin_rm))
        rotation_matrix[0][2] += (new_width/2) - self.image_center[0]
        rotation_matrix[1][2] += (new_height/2) - self.image_center[1]
        warped_image = cv2.warpAffine(
            image, rotation_matrix, (new_width, new_height))

        cv2.namedWindow('h', flags=cv2.WINDOW_AUTOSIZE)
        cv2.imshow('h', warped_image)

        if calibration:
            markers = self.__detectArucoMarkers(warped_image)
            while markers == None:
                markers = self.__detectArucoMarkers(warped_image)
            self.XOY =[markers[1].topRight[1], markers[1].topRight[0]]           
            markers[1].topRight[1] = self.XOY[0]
            markers[1].topRight[0] = self.XOY[1]
            warped_image = warped_image[markers[1].topRight[1]:-1, markers[1].topRight[0]:-1]
        else:
            self.markers_copy[1].topRight[1] = self.XOY[0]
            self.markers_copy[1].topRight[0] = self.XOY[1]
            warped_image = warped_image[self.markers_copy[1].topRight[1]:-1, self.markers_copy[1].topRight[0]:-1]

        cv2.namedWindow('g', flags=cv2.WINDOW_AUTOSIZE)
        cv2.imshow('g', warped_image)
        return warped_image

    
##########################
calib_list = []
#########################

if __name__ == '__main__':
    ip = ImageProcessor()
    import cv2
    import sys
    Cap = Camera()
    #Cap = cv2.VideoCapture("win.mp4")
    #take_frame = cv2.imread('WIN.png')
    while True:
        take_frame = Cap.get_image()
        #_,take_frame = Cap.read()
        frame = cv2.flip(cv2.flip(take_frame,0),1)
        #cv2.imshow('frame', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            ip.aruco_calibration(frame)
            ip.warp(frame)
            ip.save_settings()
        if key == ord('w'):
            ip.warp(frame)
        if key == ord('c'):
            calib_list.append(frame.copy())
            print(len(calib_list))
            # ip.chessboard_calibration(frame)
        if key == ord('b'):
            calib_list.clear()
        if key == ord('v'):
            ip.chessboard_calibration(calib_list)
        if key == ord('p'):
            ip.perspective_correction(frame, calibration = True)
        if key == ord('l'):
            cv2.imshow('result',ip.perspective_correction(frame))
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     ip.aruco_calibration(frame)
        #     ip.warp(frame)
        #     ip.save_settings()
        #     #break
