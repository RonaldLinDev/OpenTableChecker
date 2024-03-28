import cv2
import socket
import struct
import time

HOST = '192.168.1.88'
PORT = 49152
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        try:
            cam = cv2.VideoCapture(0)
            time.sleep(5)
            while(True): 
                ret, frame = cam.read()
                print(frame.dtype)
                frame_bytes = frame.tobytes()
                s.sendall(struct.pack('!i', len(frame_bytes))) # size
                s.sendall(struct.pack('!i', frame.shape[0])) # height
                s.sendall(struct.pack('!i', frame.shape[1])) # width
                s.sendall(frame_bytes)
                time.sleep(60)
        except Exception as e:
            print(e)
except Exception as e:
    print(e)



