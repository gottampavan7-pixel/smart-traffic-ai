"""
Smart Traffic AI System - Main Entry Point

A real-time traffic signal optimization system that uses YOLO for vehicle detection
and dynamically adjusts traffic light timing based on vehicle density.
"""

import cv2
import logging
import time
from typing import Dict, Tuple

import config
from detection.vehicle_detector import VehicleDetector
from detection.visualization import draw_detections
from junction.junction_controller import JunctionController
from video.video_manager import VideoManager
from ui import dashboard

# ============================================================================
# LOGGING SETUP
# ============================================================================
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    handlers=[
        logging.StreamHandler() if config.LOG_TO_CONSOLE else logging.NullHandler(),
        logging.FileHandler(config.LOG_FILE) if config.LOG_TO_FILE else logging.NullHandler(),
    ]
)
logger.info("Smart Traffic AI System Starting")


def initialize_components() -> Tuple[VideoManager, VehicleDetector, JunctionController]:
    """Initialize all system components.
    
    Returns:
        Tuple of (VideoManager, VehicleDetector, JunctionController)
        
    Raises:
        Exception: If any component fails to initialize.
    """
    # Initialize video manager
    try:
        video_manager = VideoManager(config.VIDEO_PATHS)
        logger.info("Video manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize video manager: {e}", exc_info=True)
        raise

    # Initialize detector
    try:
        detector = VehicleDetector()
        logger.info("Vehicle detector initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vehicle detector: {e}", exc_info=True)
        raise

    # Initialize controller
    try:
        controller = JunctionController(
            min_green=config.MIN_GREEN_TIME,
            max_green=config.MAX_GREEN_TIME,
            smoothing_alpha=config.SMOOTHING_ALPHA,
            max_consecutive=config.MAX_CONSECUTIVE_SAME_DIRECTION
        )
        logger.info("Junction controller initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize junction controller: {e}", exc_info=True)
        raise

    return video_manager, detector, controller


def process_frames(video_manager: VideoManager, detector: VehicleDetector) -> Tuple[Dict[str, cv2.Mat], Dict[str, int], float]:
    """Process video frames and detect vehicles.
    
    Args:
        video_manager: Manages video input.
        detector: Detects vehicles in frames.
        
    Returns:
        Tuple containing (frames_dict, raw_counts_dict, detect_time_ms).
    """
    raw_counts: Dict[str, int] = {}
    frames: Dict[str, cv2.Mat] = {}

    # Read frames from all video sources
    all_frames = video_manager.read_frames()

    # Detect vehicles in each frame and measure time
    start = time.time()
    valid = 0

    for direction, frame in all_frames.items():
        if frame is None:
            raw_counts[direction] = 0
            frames[direction] = None
            continue

        valid += 1
        vehicle_count, detections = detector.detect(frame)
        raw_counts[direction] = vehicle_count

        # Draw detections on frame
        annotated_frame = draw_detections(frame.copy(), detections)
        frames[direction] = annotated_frame

    elapsed = (time.time() - start) * 1000.0
    detect_time_ms = elapsed / valid if valid > 0 else 0.0

    return frames, raw_counts, detect_time_ms


def main() -> None:
    """Main entry point for the Smart Traffic AI system.
    
    Orchestrates video input, vehicle detection, signal control, and dashboard display.
    """
    video_manager = None
    
    try:
        # Initialize components
        video_manager, detector, controller = initialize_components()

        logger.info("Starting main processing loop")

        prev_time = time.time()
        while True:
            # Process video frames and time detection
            frames, raw_counts, detect_time = process_frames(video_manager, detector)

            # Compute FPS
            now = time.time()
            fps = 1.0 / (now - prev_time) if now > prev_time else 0.0
            prev_time = now

            # Update controller with vehicle counts
            controller.update_counts(raw_counts)
            current_green, remaining_time = controller.decide_signal()

            # Get smoothed counts from controller
            vehicle_counts = controller.smooth_counts

            # Create video grid
            video_grid = dashboard.create_video_grid(frames)

            # Create complete dashboard (include total_duration for progress)
            display_frame = dashboard.create_dashboard(
                video_grid,
                current_green,
                remaining_time,
                controller.current_duration,
                vehicle_counts,
                fps,
                detect_time
            )

            # Display dashboard
            cv2.imshow(config.WINDOW_NAME, display_frame)

            # Check for quit signal
            if cv2.waitKey(config.FRAME_DELAY_MS) & 0xFF == config.QUIT_KEY:
                logger.info("Quitting application (user pressed 'q')")
                break

    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
        raise
    finally:
        logger.info("Cleaning up resources")
        if video_manager:
            video_manager.release()
        cv2.destroyAllWindows()
        logger.info("Smart Traffic AI System stopped")


if __name__ == "__main__":
    main()