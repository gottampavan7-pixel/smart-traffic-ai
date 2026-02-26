"""
Detection Visualization Module

Handles drawing of detection results on video frames.
"""

import cv2
import logging
from typing import List
from detection.vehicle_detector import Detection

import config

logger = logging.getLogger(__name__)


def draw_detections(frame: cv2.Mat, detections: List[Detection]) -> cv2.Mat:
    """Draw detection bounding boxes and labels on a frame.
    
    Args:
        frame: The frame to draw on.
        detections: List of Detection objects to visualize.
        
    Returns:
        Frame with drawn detections.
    """
    for detection in detections:
        # Draw bounding box
        cv2.rectangle(
            frame,
            (detection.x1, detection.y1),
            (detection.x2, detection.y2),
            config.DETECTOR_BOX_COLOR,
            config.DETECTOR_BOX_THICKNESS
        )
        
        # Draw label with class name and confidence
        label = f"{detection.class_name} {detection.confidence:.2f}"
        cv2.putText(
            frame,
            label,
            (detection.x1, detection.y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            config.DETECTOR_LABEL_FONT_SIZE,
            config.DETECTOR_BOX_COLOR,
            config.DETECTOR_LABEL_THICKNESS
        )
    
    return frame
