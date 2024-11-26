"""
PyGhost - Python client for the Ghost Security Platform API
"""

from .client import GhostClient, AsyncGhostClient
from .resources.endpoints import EndpointFilters
from .exceptions import (
    GhostAPIError,
    ClientNotInitializedError,
    ValidationError,
    AuthenticationError,
    ResourceNotFoundError,
    ConnectionError,
    RetryError,
    TimeoutError
)
from .types import (
    EndpointKind,
    LastSeenPeriod,
    DEFAULT_BIN_DURATION
)

__version__ = "0.1.0"

__all__ = [
    # Main clients
    "GhostClient",
    "AsyncGhostClient",
    
    # Filters
    "EndpointFilters",
    
    # Exceptions
    "GhostAPIError",
    "ClientNotInitializedError",
    "ValidationError",
    "AuthenticationError",
    "ResourceNotFoundError",
    "ConnectionError",
    "RetryError",
    "TimeoutError",
    
    # Types and constants
    "EndpointKind",
    "LastSeenPeriod",
    "DEFAULT_BIN_DURATION"
]
