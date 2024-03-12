from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np 
from BoundBox import BoundBox
import sys

# load model
model = YOLO('models/yolov8x.pt')

# person, backpack, suitcase, handbag, dinner table laptop
image_file =  "imgs/"+ "odeimg.jpg"




def get_bounding_boxes(model, image_file):
    width, height = Image.open(image_file).size
    results = model(image_file,
                    imgsz = (width, height),
                    iou = 0.5,
                    classes = [0,24, 26, 27, 56, 60, 63, 16])

    boxes = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()
    names = results[0].names
    img = Image.fromarray(results[0].plot())
    img.show()
    return boxes, classes, names 

def count_tables(boxes, classes, names):
    listOfTables = []
    listOfNonTables = []
    tableCount = 0
    for ele in zip(boxes, classes):
        box = ele[0]
        label = names[ele[1]]
        print(box, label)
        if label == 'dining table':
            listOfTables.append(box)
        else:
            listOfNonTables.append(box) # dont care

    filled = [0 for table in listOfTables]

    for idx, table  in enumerate(listOfTables):
        ele = BoundBox(table)
        for object in listOfNonTables:
            if ele.overlaps(BoundBox(object)):
                filled[idx] = 1
    return sum(filled), len(filled) # filled tables, count tables

def count_chairs(boxes, classes, names):
    listOfTables = []
    listOfPeople = []
    chairCount = 0
    for ele in zip(boxes, classes):
        box = ele[0]
        label = names[ele[1]]
        print(box, label)
        if label == 'chair':
            listOfTables.append(box)
        elif label == 'person':
            listOfPeople.append(box) # dont care

    filled = [0 for table in listOfTables]

    for idx, table  in enumerate(listOfTables):
        ele = BoundBox(table)
        for object in listOfPeople:
            if ele.overlaps(BoundBox(object)):
                filled[idx] = 1
    return sum(filled), len(filled), len(listOfPeople)


    

if __name__ == '__main__':
    boxes, classes, names  = get_bounding_boxes(model, image_file)
    filled_tables, num_tables = count_tables(boxes, classes, names)
    filled_chairs, num_chairs, num_people = count_chairs(boxes, classes, names)
    print(f'filled {filled_tables} out of {num_tables} tables')
    print(f'filled {filled_chairs} out of {num_chairs} chairs')
    print(f'population: {num_people} ')
