"""
Main client module for interacting with the Ghost Security API.
"""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import requests

from .config import GhostConfig


class GhostAPIError(Exception):
    """Custom exception for Ghost API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class GhostClient:
    """Client for interacting with the Ghost Security API."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the Ghost Security API client.
        
        Args:
            api_key (str): The API key for authentication
            base_url (str, optional): The base URL for the API.
                                    If not provided, uses the default from GhostConfig.
        """
        self.config = GhostConfig(api_key=api_key, base_url=base_url or GhostConfig.DEFAULT_BASE_URL)
        self.session = requests.Session()
        
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, list]] = None,
        **kwargs
    ) -> Any:
        """
        Make a request to the Ghost Security API.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters
            data (dict or list, optional): Request body data
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            The parsed response data
            
        Raises:
            GhostAPIError: If the API request fails
        """
        url = self.config.get_api_url(endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.config.headers,
                params=params,
                json=data,
                **kwargs
            )
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return None
            
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            error_response = None
            
            try:
                error_response = e.response.json()
                error_msg = error_response.get('message', str(e))
            except (ValueError, AttributeError):
                pass
                
            raise GhostAPIError(
                message=error_msg,
                status_code=e.response.status_code if e.response else None,
                response=error_response
            )
        except requests.exceptions.RequestException as e:
            raise GhostAPIError(f"Request failed: {str(e)}")

    def get_endpoints(self) -> List[Dict]:
        """
        Get all endpoints.
        
        Returns:
            List[Dict]: List of endpoints
            
        Raises:
            GhostAPIError: If the API request fails
        """
        return self.get("endpoints")

    def get_apps(self) -> List[Dict]:
        """
        Get all apps.
        
        Returns:
            List[Dict]: List of apps
            
        Raises:
            GhostAPIError: If the API request fails
        """
        return self.get("apps")

    def get_app_endpoints(self, app_id: Union[str, UUID]) -> List[Dict]:
        """
        Get endpoints for a specific app.
        
        Args:
            app_id (str or UUID): The ID of the app
            
        Returns:
            List[Dict]: List of endpoints for the specified app
            
        Raises:
            GhostAPIError: If the API request fails
        """
        app_id = str(app_id)
        return self.get(f"apps/{app_id}/endpoints")

    # Base HTTP method implementations
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Any:
        """Send a GET request to the API."""
        return self._request("GET", endpoint, params=params, **kwargs)
        
    def post(self, endpoint: str, data: Optional[Union[Dict, list]] = None, **kwargs) -> Any:
        """Send a POST request to the API."""
        return self._request("POST", endpoint, data=data, **kwargs)
        
    def put(self, endpoint: str, data: Optional[Union[Dict, list]] = None, **kwargs) -> Any:
        """Send a PUT request to the API."""
        return self._request("PUT", endpoint, data=data, **kwargs)
        
    def delete(self, endpoint: str, **kwargs) -> Any:
        """Send a DELETE request to the API."""
        return self._request("DELETE", endpoint, **kwargs)
