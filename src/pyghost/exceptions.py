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


class ClientNotInitializedError(GhostAPIError):
    """Raised when trying to use async client outside context manager."""
    
    def __init__(self):
        super().__init__("Client not initialized. Use 'async with' context manager.")


class ValidationError(GhostAPIError):
    """Raised when request parameters fail validation."""
    pass


class AuthenticationError(GhostAPIError):
    """Raised when API authentication fails."""
    pass


class ResourceNotFoundError(GhostAPIError):
    """Raised when requested resource is not found."""
    pass
