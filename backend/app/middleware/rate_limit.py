"""Simple in-process rate limiting for authentication endpoints."""
import time
from collections import defaultdict
from threading import Lock
from typing import Dict

from app.config import settings


class SimpleRateLimiter:
    """
    Simple in-process fixed-window rate limiter.

    NOTE: This is suitable for single-instance MVP only.
    For horizontal scaling, move to shared store (Redis).
    """

    def __init__(self, max_attempts: int = 5, window_seconds: int = 300):
        """
        Initialize rate limiter.

        Args:
            max_attempts: Maximum attempts allowed per window
            window_seconds: Time window in seconds
        """
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: Dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def is_rate_limited(self, key: str) -> bool:
        """
        Check if key is rate limited.

        Args:
            key: Identifier to rate limit (e.g., IP address or email)

        Returns:
            True if rate limited, False otherwise
        """
        if not settings.rate_limit_enabled:
            return False

        with self._lock:
            now = time.time()
            window_start = now - self.window_seconds

            # Remove expired attempts
            self._attempts[key] = [
                timestamp for timestamp in self._attempts[key] if timestamp > window_start
            ]

            # Check if limit exceeded
            if len(self._attempts[key]) >= self.max_attempts:
                return True

            # Record new attempt
            self._attempts[key].append(now)
            return False

    def reset(self, key: str | None = None) -> None:
        """
        Reset rate limit counters.

        Args:
            key: Specific key to reset, or None to reset all
        """
        with self._lock:
            if key is None:
                self._attempts.clear()
            elif key in self._attempts:
                del self._attempts[key]


# Global rate limiter instance
login_rate_limiter = SimpleRateLimiter(max_attempts=5, window_seconds=300)
