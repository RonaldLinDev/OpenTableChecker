from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np 
from BoundBox import BoundBox

# load model
model = YOLO('yolov8x.pt')

# person, backpack, suitcase, handbag, dinner table laptop

results = model(r'imgs/image.webp', imgsz = 3200, agnostic_nms = True, classes = [0,24, 26, 27, 60,63,16])

boxes = results[0].boxes.xyxy.cpu().numpy()
classes = results[0].boxes.cls.cpu().numpy()
names = results[0].names

setOfTables = []
setOfNonTables = []
tableCount = 0
filledTableCount = 0

for ele in zip(boxes, classes):
    box = ele[0]
    label = names[ele[1]]
    print(box, label)
    if label == 'dining table':
        setOfTables.append(box)
    else:
        setOfNonTables.append(box) # dont care

for table in setOfTables:
    ele = BoundBox(table)
    tableCount += 1
    for object in setOfNonTables:
        if ele.overlaps(BoundBox(object)):
            # setOfTables.remove(table)
            # setOfNonTables.remove(object)
            filledTableCount += 1

print(f'filled {filledTableCount} out of {tableCount} tables')

# img = Image.fromarray(results[0].plot())
# img.show()
