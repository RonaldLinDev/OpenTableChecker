import socket
import pymssql
import predict

HOST = 1
PORT = 1
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                image_arr = conn.recv(BUFFER_SIZE).decode('utf-8')  
                boxes, classes, names  = predict.get_bounding_boxes(image_arr)
                filled_tables, num_tables = predict.count_tables(boxes, classes, names)
                filled_chairs, num_chairs, num_people = predict.count_chairs(boxes, classes, names)
                print(f"Received data: {image_arr}") 
