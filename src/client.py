import cv2
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 1
PORT = 1
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(HOST, PORT)
        try:
            with cv2.VideoCapture(0) as cam:
                while(True):
                    ret, frame = cam.read()
                    s.sendall(frame)
        except:
            print("camera connect failed")
            s.sendall("camera connect failed".encode('utf-8')) 
except:
    print("socket connect failed")



