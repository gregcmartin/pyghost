"""
PyGhost - Python API client for the Ghost Security Platform
"""

from .client import GhostClient, GhostAPIError
from .config import GhostConfig

__version__ = "0.1.0"
__all__ = ["GhostClient", "GhostConfig", "GhostAPIError"]
