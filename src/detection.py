import time
import json
from pathlib import Path
from typing import Dict, List
import onnxruntime as rt
import numpy as np
import cv2

from config import (
    models_path, outputs_path, get_logger,model_name,conf_thresh,iou_thresh,input_size
)
from frame_loader import multicamloader
from utils import perfmetrics, timer

logger=get_logger(__name__)

class yolov8detector:
    def __init__(self,model_path):
        self.session=rt.InferenceSession(str(model_path), providers=['CPUExecutionProvider'])
        self.input_name=self.session.get_inputs()[0].name
        self.output_names=[o.name for o in self.session.get_outputs()]
        self.input_size=input_size
        self.metrics = perfmetrics('yolov8detector')
        logger.info(f"Loaded ONNX model: {model_path}")

    def preprocess(self,image):
        with timer("preprocess"):
            img_resized=cv2.resize(image,(self.input_size,self.input_size))
            img_rgb=cv2.cvtColor(img_resized,cv2.COLOR_RGB2BGR)
            img_norm=img_rgb.astype(np.float32)/255.0
            img_chw=np.transpose(img_norm,(2,0,1))
            img_batch=np.expand_dims(img_chw,0)
            return img_batch

    def _postprocess(self,output,og_shape):
        detections=[]
        if output.shape[1]=84:
            output=output.transpose(0,2,1)
        output.transpose(0,2,1)

        for det in output[0]:
            x,y,w,h=det[0],det[1],det[2],det[3]
            conf=det[4]
            classes=det[5:]
            class_id=np.argmax(classes)
            class_conf=classes[class_id]
            final_conf=conf*class_conf

            if final_conf>conf_thresh:
                detections.append({
                    'x':float(x),
                    'y':float(y),
                    'w':float(w),
                    'h':float(h),
                    'conf':float(final_conf),
                    'class_id':int(class_id)
                })
        return detections

    def detect(self,image):
        start=time.perf_counter()
        img_batch=self.preprocess(image)
        with timer("inference"):
            outputs=self.session.run(self.output_names,{self.input_name:img_batch})
        detections=self._postprocess(outputs[0],image.shape)
        elapsed=(time.perf_counter()-start)*1000
        self.metrics.record_frame(elapsed)
        return detections


class detectionpipe:


