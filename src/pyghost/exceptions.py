"""
Exceptions for the Ghost Security API client.
"""
from typing import Optional, Dict


class GhostAPIError(Exception):
    """Base exception for Ghost Security API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        """
        Initialize the error.
        
        Args:
            message (str): Error message
            status_code (int, optional): HTTP status code
            response (dict, optional): Raw API response
        """
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        """Format error message with status code if available."""
        if self.status_code:
            return f"{self.status_code} - {super().__str__()}"
        return super().__str__()


class ClientNotInitializedError(GhostAPIError):
    """Raised when trying to use async client outside context manager."""
    
    def __init__(self):
        super().__init__(
            "Client not initialized. Use 'async with' context manager."
        )


class ValidationError(GhostAPIError):
    """Raised when request parameters fail validation."""
    pass


class AuthenticationError(GhostAPIError):
    """Raised when API authentication fails."""
    pass


class ResourceNotFoundError(GhostAPIError):
    """Raised when requested resource is not found."""
    pass


class ConnectionError(GhostAPIError):
    """Raised when connection to the API fails."""
    
    def __init__(self, message: str):
        super().__init__(
            f"Failed to connect to the Ghost Security API: {message}"
        )


class RetryError(GhostAPIError):
    """Raised when max retries are exceeded."""
    
    def __init__(self, message: str):
        super().__init__(
            f"Connection retry attempts exhausted: {message}"
        )


class TimeoutError(GhostAPIError):
    """Raised when request times out."""
    
    def __init__(self, timeout: int):
        super().__init__(
            f"Request timed out after {timeout} seconds"
        )
