import BoundBox
import Image
import predict
import cv2

try:
    cam = cv2.VideoCapture(0)
    while(True):
        
        ret, frame = cam.read()
        cv2.imshow('frame', frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
except:
    print("no cam found")