"""
Video Manager Module

Handles video capture and frame reading from multiple camera feeds.
"""

import cv2
import logging
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)


class VideoManager:
    """Manages video capture from multiple camera feeds.
    
    Handles opening video files, reading frames, and rewinding when necessary.
    """
    
    def __init__(self, video_paths: Dict[str, str]) -> None:
        """Initialize VideoManager with video file paths.
        
        Args:
            video_paths: Dictionary mapping direction names to video file paths.
                        e.g., {"NORTH": "videos/north.mp4", ...}
        
        Raises:
            FileNotFoundError: If a video file cannot be opened.
            Exception: For unexpected errors during initialization.
        """
        self.video_paths = video_paths
        self.captures: Dict[str, cv2.VideoCapture] = {}
        self._load_videos()
    
    def _load_videos(self) -> None:
        """Load all video files specified in video_paths.
        
        Raises:
            FileNotFoundError: If a video file is not found or cannot be opened.
            Exception: For unexpected errors during video loading.
        """
        for direction, video_path in self.video_paths.items():
            try:
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    logger.error(f"Failed to open video file for {direction}: {video_path}")
                    raise FileNotFoundError(f"Cannot open video file: {video_path}")
                self.captures[direction] = cap
                logger.info(f"Loaded video feed for {direction}: {video_path}")
            except FileNotFoundError as e:
                logger.error(f"Video file not found for {direction}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error loading {direction} video: {e}", exc_info=True)
                raise
    
    def read_frames(self) -> Dict[str, cv2.Mat]:
        """Read frames from all video captures.
        
        Automatically rewinds video if end of file is reached.
        
        Returns:
            Dictionary mapping direction names to frames.
            
        Raises:
            Warning logged if a frame cannot be read from a specific camera.
        """
        frames = {}
        
        for direction, cap in self.captures.items():
            ret, frame = cap.read()
            
            if not ret:
                logger.debug(f"Rewinding video for {direction}")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            
            if not ret:
                logger.warning(f"Failed to read frame from {direction}")
                frames[direction] = None
            else:
                frames[direction] = frame
        
        return frames
    
    def release(self) -> None:
        """Release all video capture resources."""
        for cap in self.captures.values():
            cap.release()
        logger.debug("All video captures released")
