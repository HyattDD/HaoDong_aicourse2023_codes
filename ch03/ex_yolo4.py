# Still testing, not working yet


#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
os.environ['TL_BACKEND'] = 'torch'

import numpy as np
import cv2
from PIL import Image
from common import yolo4_input_processing, yolo4_output_processing, \
    result_to_json, read_class_names, draw_boxes_and_labels_to_image_with_json
from yolo import YOLOv4
import tensorlayerx as tlx

tlx.logging.set_verbosity(tlx.logging.DEBUG)

INPUT_SIZE = 416
image_path = './dog.jpg'

class_names = read_class_names('./model/coco.names')
original_image = cv2.imread(image_path)
image = cv2.cvtColor(np.array(original_image), cv2.COLOR_BGR2RGB)

model = YOLOv4(NUM_CLASS=80, pretrained=True)
model.set_eval()

batch_data = yolo4_input_processing(original_image)
feature_maps = model(batch_data)
pred_bbox = yolo4_output_processing(feature_maps)
json_result = result_to_json(image, pred_bbox)

image = draw_boxes_and_labels_to_image_with_json(image, json_result, class_names)
image = Image.fromarray(image.astype(np.uint8))
image.show()
