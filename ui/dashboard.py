"""
Dashboard Rendering Module

Handles all visual elements for the traffic command center dashboard.
"""

import cv2
import logging
import time
from typing import Dict, Tuple

import config
import numpy as np

logger = logging.getLogger(__name__)

def get_congestion_level(value: float) -> str:
    """Return text level for congestion based on thresholds."""
    if value < config.CONGESTION_LOW:
        return "LOW"
    if value < config.CONGESTION_MEDIUM:
        return "MEDIUM"
    if value < config.CONGESTION_HIGH:
        return "HIGH"
    return "CRITICAL"


def draw_congestion_badge(frame: cv2.Mat, level: str, position: Tuple[int, int]) -> None:
    """Draw a small rectangular badge indicating congestion level.

    Critical level flashes red to draw attention.
    """
    x, y = position
    text = level
    if level == "LOW":
        color = config.BADGE_COLOR_LOW
    elif level == "MEDIUM":
        color = config.BADGE_COLOR_MEDIUM
    elif level == "HIGH":
        color = config.BADGE_COLOR_HIGH
    else:
        # flashing effect for CRITICAL
        t = time.time()
        blink = int(t * 2) % 2  # toggle every 0.5s
        color = config.BADGE_COLOR_CRITICAL if blink else (100, 0, 0)

    cv2.rectangle(frame, (x, y - 15), (x + 80, y + 5), color, -1)
    cv2.putText(frame, text, (x + 3, y - 2), cv2.FONT_HERSHEY_SIMPLEX,
                0.4, (255, 255, 255), 1)


def draw_traffic_light(frame: cv2.Mat, top_left: Tuple[int, int], is_active: bool) -> None:
    """Draw a vertical traffic light icon.

    Args:
        frame: Destination image.
        top_left: (x, y) of the top-left corner of the light.
        is_active: Whether the green light is currently active (the only lit one).
    """
    x, y = top_left
    radius = config.SIGNAL_LIGHT_RADIUS
    spacing = radius * 2 + 4

    # colors for inactive lights (dark gray)
    off_color = (50, 50, 50)

    # draw red light
    color_red = (0, 0, 255) if not is_active else off_color
    cv2.circle(frame, (x + radius, y + radius), radius, color_red, -1)

    # draw yellow light below
    color_yellow = (0, 255, 255) if not is_active else off_color
    cv2.circle(frame, (x + radius, y + radius + spacing), radius, color_yellow, -1)

    # draw green light at bottom
    color_green = (0, 255, 0) if is_active else off_color
    cv2.circle(frame, (x + radius, y + radius + spacing * 2), radius, color_green, -1)



def draw_density_bar(frame: cv2.Mat, value: float, max_value: float, 
                     start_x: int, start_y: int) -> None:
    """Draw a vehicle density bar on the frame.
    
    The bar color changes based on density: green < 10, orange 10-19, red >= 20.
    
    Args:
        frame: The frame to draw on.
        value: Current vehicle count.
        max_value: Maximum value for scaling the bar.
        start_x: X coordinate of the bar's top-left corner.
        start_y: Y coordinate of the bar's top-left corner.
    """
    filled = int((value / max_value) * config.BAR_WIDTH) if max_value > 0 else 0

    if value < config.BAR_DENSITY_THRESHOLD_1:
        bar_color = config.BAR_COLOR_GREEN
    elif value < config.BAR_DENSITY_THRESHOLD_2:
        bar_color = config.BAR_COLOR_ORANGE
    else:
        bar_color = config.BAR_COLOR_RED

    # Draw outline
    cv2.rectangle(
        frame,
        (start_x, start_y),
        (start_x + config.BAR_WIDTH, start_y + config.BAR_HEIGHT),
        config.BAR_OUTLINE_COLOR,
        config.BAR_OUTLINE_THICKNESS
    )

    # Draw filled portion
    cv2.rectangle(
        frame,
        (start_x, start_y),
        (start_x + filled, start_y + config.BAR_HEIGHT),
        bar_color,
        -1
    )


def create_video_grid(frames: Dict[str, cv2.Mat]) -> cv2.Mat:
    """Create a 2x2 grid of video frames.
    
    Arranges video frames in the order: NORTH-EAST (top), WEST-SOUTH (bottom).
    
    Args:
        frames: Dictionary mapping direction names to frames.
        
    Returns:
        Combined 2x2 grid frame.
    """
    top = cv2.hconcat([frames["NORTH"], frames["EAST"]])
    bottom = cv2.hconcat([frames["WEST"], frames["SOUTH"]])
    video_grid = cv2.vconcat([top, bottom])
    return video_grid


def create_dashboard(video_grid: cv2.Mat,
                    current_green: str,
                    remaining_time: int,
                    total_duration: int,
                    vehicle_counts: Dict[str, float],
                    fps: float,
                    detect_time: float) -> cv2.Mat:
    """Compose the complete Smart City command center dashboard.

    Args:
        video_grid: 2x2 concatenated video frames.
        current_green: Direction currently green.
        remaining_time: Seconds left for green light.
        vehicle_counts: Smoothed vehicle counts per direction.
        fps: Frames per second being rendered.
        detect_time: Average detection time per frame (ms).
    """
    # compute mode based on congestion
    max_count = max(vehicle_counts.values()) if vehicle_counts else 0
    if max_count >= config.CONGESTION_HIGH:
        system_mode = "EMERGENCY"
    elif max_count >= config.CONGESTION_MEDIUM:
        system_mode = "HEAVY TRAFFIC"
    else:
        system_mode = "NORMAL"

    height_v, width_v, _ = video_grid.shape
    total_height = config.HEADER_HEIGHT + height_v + config.STATUS_PANEL_HEIGHT

    # create base canvas
    dashboard = np.zeros((total_height, width_v, 3), dtype="uint8")
    dashboard[:] = config.PANEL_BACKGROUND_COLOR

    # header bar
    dashboard[0:config.HEADER_HEIGHT] = config.HEADER_BACKGROUND
    # draw title centered
    title = "SMART TRAFFIC COMMAND CENTER"
    (tw, th), _ = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX,
                                 config.TITLE_FONT_SIZE, config.TITLE_THICKNESS)
    tx = (width_v - tw) // 2
    ty = (config.HEADER_HEIGHT + th) // 2
    cv2.putText(dashboard, title, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX,
                config.TITLE_FONT_SIZE, config.HEADER_TEXT_COLOR,
                config.TITLE_THICKNESS)

    # place video grid
    dashboard[config.HEADER_HEIGHT:config.HEADER_HEIGHT + height_v, 0:width_v] = video_grid
    # draw border around grid
    cv2.rectangle(dashboard,
                  (0, config.HEADER_HEIGHT),
                  (width_v-1, config.HEADER_HEIGHT + height_v-1),
                  (100, 100, 100), 2)

    # status panel
    status_y = config.HEADER_HEIGHT + height_v
    dashboard[status_y:status_y + config.STATUS_PANEL_HEIGHT] = config.STATUS_BG

    # draw system status texts
    cv2.putText(dashboard, f"Mode: {system_mode}",
                (config.DASHBOARD_START_X, status_y + 25),
                cv2.FONT_HERSHEY_SIMPLEX, config.METRICS_FONT_SIZE,
                config.STATUS_TEXT_COLOR, config.METRICS_THICKNESS)
    cv2.putText(dashboard, f"Active: {current_green}",
                (config.DASHBOARD_START_X, status_y + 50),
                cv2.FONT_HERSHEY_SIMPLEX, config.METRICS_FONT_SIZE,
                config.STATUS_TEXT_COLOR, config.METRICS_THICKNESS)
    cv2.putText(dashboard, f"Phase: {current_green}",
                (config.DASHBOARD_START_X, status_y + 75),
                cv2.FONT_HERSHEY_SIMPLEX, config.METRICS_FONT_SIZE,
                config.STATUS_TEXT_COLOR, config.METRICS_THICKNESS)

    # draw performance metrics
    cv2.putText(dashboard, f"FPS: {fps:.1f}",
                (width_v - 150, status_y + 25),
                cv2.FONT_HERSHEY_SIMPLEX, config.FPS_FONT_SIZE,
                config.FPS_FONT_COLOR, 1)
    cv2.putText(dashboard, f"Detect: {detect_time:.1f}ms",
                (width_v - 150, status_y + 50),
                cv2.FONT_HERSHEY_SIMPLEX, config.FPS_FONT_SIZE,
                config.FPS_FONT_COLOR, 1)

    # draw traffic lights and congestion for each direction
    directions = list(config.VIDEO_PATHS.keys())
    for i, direction in enumerate(directions):
        x_offset = config.DASHBOARD_START_X + i * config.DASHBOARD_OFFSET_PER_DIRECTION
        light_top = status_y + config.STATUS_LIGHT_Y_OFFSET
        is_active = (direction == current_green)
        draw_traffic_light(dashboard, (x_offset, light_top), is_active)

        # congestion badge
        level = get_congestion_level(vehicle_counts.get(direction, 0))
        draw_congestion_badge(
            dashboard,
            level,
            (x_offset + config.STATUS_LIGHT_BADGE_X_OFFSET, light_top + 40)
        )

    # draw progress bar for green timer
    bar_y = status_y + config.STATUS_PANEL_HEIGHT - 20
    ratio = remaining_time / total_duration if total_duration > 0 else 0
    bar_width = int(ratio * width_v)
    cv2.rectangle(dashboard, (0, bar_y), (width_v, bar_y + config.PROGRESS_BAR_HEIGHT),
                  config.PROGRESS_BAR_BG, -1)
    cv2.rectangle(dashboard, (0, bar_y), (bar_width, bar_y + config.PROGRESS_BAR_HEIGHT),
                  config.PROGRESS_BAR_COLOR, -1)

    return dashboard
