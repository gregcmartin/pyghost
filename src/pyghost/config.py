"""
Configuration module for the Ghost Security API client.
"""

class GhostConfig:
    """Configuration class for the Ghost Security API client."""
    
    DEFAULT_BASE_URL = "https://api.dev.ghostsecurity.com"
    API_VERSION = "v2"
    
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        """
        Initialize the Ghost Security API configuration.
        
        Args:
            api_key (str): The API key for authentication (JWT token)
            base_url (str, optional): The base URL for the API. 
                                    Defaults to https://api.dev.ghostsecurity.com
        """
        if not api_key:
            raise ValueError("API key is required")
            
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
    @property
    def headers(self) -> dict:
        """
        Get the headers required for API requests.
        
        Returns:
            dict: Headers including authentication with Bearer token
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
    def get_api_url(self, endpoint: str) -> str:
        """
        Get the full API URL for a given endpoint.
        
        Args:
            endpoint (str): The API endpoint path
            
        Returns:
            str: The full API URL
        """
        return f"{self.base_url}/{self.API_VERSION}/{endpoint.lstrip('/')}"
