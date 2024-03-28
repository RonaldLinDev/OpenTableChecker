import socket
import pymssql 
import predict
import struct
import numpy as np
import datetime
import json

HOST = socket.gethostname()
print(HOST)
PORT = 49152

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', PORT))
        print('waiting for client')
        s.listen()
        conn, addr = s.accept()
        print('accepted')
        with conn:
            print('Connected by', addr)
            try:
                with open('db_config.json') as f:
                    db_config = json.load(f)
                conn = pymssql.connect(
                    server=db_config['server'],
                    user=db_config['user'],
                    password=db_config['password'],
                    database=db_config['database']
                )               
                cursor = conn.cursor(as_dict = True)
                while True:
                    size = struct.unpack('!i', conn.recv(4))[0]
                    height = struct.unpack('!i', conn.recv(4))[0]
                    width = struct.unpack('!i', conn.recv(4))[0]
                    image_arr = b''
                    while (len(image_arr) < size):
                        image_arr += conn.recv(size - len(image_arr))
                    image_arr = np.frombuffer(image_arr, dtype = np.uint8).reshape((height, width, 3))
                    print(f'image array {image_arr}')  
                    boxes, classes, names  = predict.get_bounding_boxes(image_arr)
                    filled_tables, num_tables = predict.count_tables(boxes, classes, names)
                    filled_chairs, num_chairs, num_people = predict.count_chairs(boxes, classes, names)
                    print(f"Received data: {image_arr}")
                    cursor.execute('INSERT INTO occupancy VALUES(0, %s, %s, %s, %s, %s)' % (datetime.datetime.now().strftime, num_chairs, filled_chairs, num_tables, filled_tables, num_people) )               
            except Exception as e:
                print(e)
                 
