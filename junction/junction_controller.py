"""
Junction Controller Module

Controls traffic signal timing based on vehicle density at each direction.
"""

import time
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class JunctionController:
    """Controls traffic signal timing for a 4-way junction.
    
    Uses exponential moving average to smooth vehicle counts and applies
    fairness logic to prevent one direction from getting too many consecutive
    green lights.
    """

    def __init__(self,
                 min_green: int = 15,
                 max_green: int = 90,
                 smoothing_alpha: float = 0.7,
                 max_consecutive: int = 2) -> None:
        """Initialize JunctionController with timing parameters.
        
        Args:
            min_green: Minimum green light duration in seconds (default: 15).
            max_green: Maximum green light duration in seconds (default: 90).
            smoothing_alpha: Exponential moving average factor 0-1 (default: 0.7).
                           Higher values give more weight to recent counts.
            max_consecutive: Maximum times same direction can get green (default: 2).
        """
        self.MIN_GREEN = min_green
        self.MAX_GREEN = max_green
        self.ALPHA = smoothing_alpha
        self.MAX_CONSECUTIVE = max_consecutive

        self.current_green: str = None
        self.green_end_time: float = 0
        self.last_green: str = None
        self.consecutive_count: int = 0
        # duration of current green phase in seconds (for UI progress bar)
        self.current_duration: int = 0

        self.smooth_counts: Dict[str, float] = {
            "NORTH": 0,
            "EAST": 0,
            "SOUTH": 0,
            "WEST": 0,
        }
        
        logger.debug(f"JunctionController initialized: min_green={min_green}, max_green={max_green}, "
                   f"smoothing_alpha={smoothing_alpha}, max_consecutive={max_consecutive}")

    def update_counts(self, raw_counts: Dict[str, int]) -> None:
        """Update smoothed vehicle counts using exponential moving average.
        
        Args:
            raw_counts: Dictionary mapping directions to current vehicle counts.
        """
        for direction in raw_counts:
            self.smooth_counts[direction] = (
                self.ALPHA * self.smooth_counts[direction]
                + (1 - self.ALPHA) * raw_counts[direction]
            )

    def decide_signal(self) -> Tuple[str, int]:
        """Decide which direction gets green light and for how long.
        
        Selects the direction with the most vehicles, with fairness logic
        to prevent starvation of other directions.
        
        Returns:
            Tuple of (direction_name, remaining_seconds_for_green_light)
        """
        current_time = time.time()

        if self.current_green is None or current_time >= self.green_end_time:

            directions = list(self.smooth_counts.keys())
            values = list(self.smooth_counts.values())

            max_index = values.index(max(values))
            selected = directions[max_index]

            # Fairness logic: prevent same direction getting green too many times
            if selected == self.last_green:
                self.consecutive_count += 1
            else:
                self.consecutive_count = 1

            if self.consecutive_count > self.MAX_CONSECUTIVE:

                sorted_dirs = sorted(
                    self.smooth_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )

                for d, _ in sorted_dirs:
                    if d != self.last_green:
                        selected = d
                        break

                self.consecutive_count = 1

            self.current_green = selected
            self.last_green = selected

            calculated_time = int(self.smooth_counts[selected]) * 2
            calculated_time = max(
                self.MIN_GREEN,
                min(calculated_time, self.MAX_GREEN)
            )

            # Store current duration for UI progress bar
            self.current_duration = calculated_time

        # compute remaining time until green ends
        remaining = int(self.green_end_time - time.time())
        if remaining < 0:
            remaining = 0
        return self.current_green, remaining