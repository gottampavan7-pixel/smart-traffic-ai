"""
Vehicle Detection Module

Handles vehicle detection using YOLO model.
"""

import logging
from typing import Tuple, List, Dict, Optional
import cv2
from ultralytics import YOLO

import config

logger = logging.getLogger(__name__)


class Detection:
    """Represents a single vehicle detection."""
    
    def __init__(self, class_id: int, class_name: str, confidence: float,
                 x1: int, y1: int, x2: int, y2: int) -> None:
        """Initialize a Detection object.
        
        Args:
            class_id: YOLO class ID.
            class_name: Human-readable class name (e.g., 'car').
            confidence: Detection confidence score (0-1).
            x1: Left x-coordinate of bounding box.
            y1: Top y-coordinate of bounding box.
            x2: Right x-coordinate of bounding box.
            y2: Bottom y-coordinate of bounding box.
        """
        self.class_id = class_id
        self.class_name = class_name
        self.confidence = confidence
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class VehicleDetector:
    """Detects vehicles in video frames using YOLOv8.
    
    Handles YOLO model loading and vehicle detection, returning detection
    data without performing any visualization.
    """
    
    def __init__(self, model_path: Optional[str] = None) -> None:
        """Initialize VehicleDetector with YOLO model.
        
        Args:
            model_path: Path to YOLO model file. If None, uses config default.
            
        Raises:
            FileNotFoundError: If model file not found.
            Exception: For other initialization errors.
        """
        try:
            if model_path is None:
                model_path = config.YOLO_MODEL_PATH
            logger.info(f"Loading YOLO model from {model_path}")
            self.model = YOLO(model_path)
            self.vehicle_classes = config.VEHICLE_CLASSES
            logger.info(f"YOLO model loaded successfully. Tracking classes: {self.vehicle_classes}")
        except FileNotFoundError as e:
            logger.error(f"YOLO model file not found: {model_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}", exc_info=True)
            raise

    def detect(self, frame: cv2.Mat) -> Tuple[int, List[Detection]]:
        """Detect vehicles in a frame.
        
        Args:
            frame: Input frame from video.
            
        Returns:
            Tuple of (vehicle_count, list of Detection objects).
        """
        results = self.model(frame, verbose=False, imgsz=config.YOLO_IMAGE_SIZE)
        vehicle_count = 0
        detections: List[Detection] = []

        for result in results:
            boxes = result.boxes

            for box in boxes:
                cls = int(box.cls[0])

                if cls in self.vehicle_classes:
                    vehicle_count += 1
                    
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_name = self.model.names[cls]
                    
                    detection = Detection(
                        class_id=cls,
                        class_name=class_name,
                        confidence=confidence,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2
                    )
                    detections.append(detection)

        return vehicle_count, detections