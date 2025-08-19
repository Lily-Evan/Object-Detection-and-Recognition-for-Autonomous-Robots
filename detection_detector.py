import cv2
import numpy as np
import torch

class YOLODetector:
    def __init__(self, model_path='models/yolov5s.pt', device='cpu'):
        self.device = device
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True).to(self.device)
        self.model.eval()
        self.names = self.model.names

    def detect(self, frame):
        # Accepts BGR images (OpenCV)
        results = self.model(frame)
        detections = []
        for *xyxy, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = [int(v.item()) for v in xyxy]
            conf = conf.item()
            cls = int(cls.item())
            label = self.names[cls]
            detections.append({'bbox': (x1, y1, x2, y2), 'conf': conf, 'label': label})
        return detections

    def draw_detections(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            label = det['label']
            conf = det['conf']
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            text = f"{label} {conf:.2f}"
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        return frame