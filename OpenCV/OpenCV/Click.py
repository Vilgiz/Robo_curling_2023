
import cv2
from Camera import Camera

Cam = Camera(1)
frame = Cam.get_image()
pixel_coord = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_coord.append([x,y])
        print(pixel_coord)
        return(pixel_coord)

def main():

    cv2.imshow('Frame', frame)      
    cv2.setMouseCallback("Frame", mouse_callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
