"""
Configuration file for Smart Traffic AI System
Contains all magic numbers, paths, and parameters
"""

# ============================================================================
# VIDEO INPUT CONFIGURATION
# ============================================================================
VIDEO_PATHS = {
    "NORTH": "videos/north.mp4",
    "EAST": "videos/east.mp4",
    "SOUTH": "videos/south.mp4",
    "WEST": "videos/west.mp4",
}

# ============================================================================
# DETECTION CONFIGURATION
# ============================================================================
YOLO_MODEL_PATH = "yolov8n.pt"
YOLO_IMAGE_SIZE = 640
VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck

# ============================================================================
# JUNCTION CONTROLLER CONFIGURATION
# ============================================================================
MIN_GREEN_TIME = 15  # seconds
MAX_GREEN_TIME = 90  # seconds
SMOOTHING_ALPHA = 0.7  # Exponential moving average factor (0-1)
MAX_CONSECUTIVE_SAME_DIRECTION = 2  # Fairness limit

# ============================================================================
# UI/VISUALIZATION CONFIGURATION
# ============================================================================
# Dashboard panel
PANEL_HEIGHT = 250
PANEL_BACKGROUND_COLOR = (30, 30, 30)  # deep gray background
PANEL_TEXT_COLOR = (220, 220, 220)
HEADER_HEIGHT = 40
HEADER_BACKGROUND = (15, 15, 15)
HEADER_TEXT_COLOR = (240, 240, 240)

# Signal light (unused now but kept for compatibility)
SIGNAL_LIGHT_RADIUS = 12
SIGNAL_LIGHT_THICKNESS = -1  # -1 = filled circle
SIGNAL_LIGHT_GREEN = (0, 255, 0)
SIGNAL_LIGHT_RED = (0, 0, 255)

# Density bar
BAR_WIDTH = 200
BAR_HEIGHT = 20
BAR_OUTLINE_COLOR = (80, 80, 80)
BAR_OUTLINE_THICKNESS = 2
BAR_COLOR_GREEN = (0, 200, 0)  # < low threshold
BAR_COLOR_ORANGE = (0, 140, 255)  # medium
BAR_COLOR_RED = (0, 0, 200)  # high
BAR_DENSITY_THRESHOLD_1 = 10
BAR_DENSITY_THRESHOLD_2 = 20
BAR_DENSITY_THRESHOLD_3 = 30

# Layout offsets
DASHBOARD_START_X = 30
DASHBOARD_OFFSET_PER_DIRECTION = 300
DASHBOARD_TITLE_Y_OFFSET = 20
DASHBOARD_CONTENT_Y_OFFSET = 40
DASHBOARD_METRICS_Y_OFFSET = 35
DASHBOARD_BAR_Y_OFFSET = 50
TIMER_TEXT_X_OFFSET = 300

# Text formatting
TITLE_FONT_SIZE = 0.8
TITLE_THICKNESS = 2
DIRECTION_FONT_SIZE = 0.6
DIRECTION_THICKNESS = 2
METRICS_FONT_SIZE = 0.6
METRICS_THICKNESS = 2
TIMER_FONT_SIZE = 0.8
TIMER_THICKNESS = 2
DETECTOR_LABEL_FONT_SIZE = 0.5
DETECTOR_LABEL_THICKNESS = 2
DETECTOR_BOX_THICKNESS = 2
DETECTOR_BOX_COLOR = (0, 255, 0)

# Congestion badge
CONGESTION_LOW = 10
CONGESTION_MEDIUM = 20
CONGESTION_HIGH = 30

BADGE_COLOR_LOW = (0, 200, 0)
BADGE_COLOR_MEDIUM = (0, 140, 255)
BADGE_COLOR_HIGH = (0, 0, 200)
BADGE_COLOR_CRITICAL = (0, 0, 255)

# Progress bar
PROGRESS_BAR_HEIGHT = 10
PROGRESS_BAR_COLOR = (0, 255, 0)
PROGRESS_BAR_BG = (80, 80, 80)

# Status panel
STATUS_PANEL_HEIGHT = 120
STATUS_BG = (25, 25, 25)
STATUS_TEXT_COLOR = (230, 230, 230)
STATUS_LIGHT_Y_OFFSET = 60
STATUS_LIGHT_BADGE_X_OFFSET = 90

# Performance metrics
FPS_FONT_SIZE = 0.5
FPS_FONT_COLOR = (200, 200, 200)

# Window
WINDOW_NAME = "4-Road Smart Junction AI - Command Center"
QUIT_KEY = ord("q")
FRAME_DELAY_MS = 1  # milliseconds for cv2.waitKey()

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "smart_traffic.log"
LOG_TO_CONSOLE = True
LOG_TO_FILE = True
