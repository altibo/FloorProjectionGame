import cv2
import numpy as np

class Tracker:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        self.bg_sub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)
        self.min_area = 500  # adjust for distance
        
    def get_frame_and_positions(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, []
        
        # Simple person/blob detection via background subtraction
        fg_mask = self.bg_sub.apply(frame)
        fg_mask = cv2.medianBlur(fg_mask, 5)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        positions = []
        for cnt in contours:
            if cv2.contourArea(cnt) > self.min_area:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    positions.append((cx, cy))
        
        return frame, positions
    
    def release(self):
        self.cap.release()
