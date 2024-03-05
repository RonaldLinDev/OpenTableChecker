from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np 
from BoundBox import BoundBox

# load model
model = YOLO('models/yolov8x.pt')

# person, backpack, suitcase, handbag, dinner table laptop
IMAGE =  "imgs/"+ "IMG_7695.jpeg"
IMG_SIZE = 3200

results = model(IMAGE,
                 imgsz = IMG_SIZE,
                iou = 0.5, 
                agnostic_nms = True,
                retina_masks = True,
                classes = [0,24, 26, 27, 60,63,16])

boxes = results[0].boxes.xyxy.cpu().numpy()
classes = results[0].boxes.cls.cpu().numpy()
names = results[0].names

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


print(f'filled {sum(filled)} out of {len(filled)} tables')

img = Image.fromarray(results[0].plot())
img.show()
