"""
Base HTTP client implementation for the Ghost Security API.
"""
from typing import Any, Optional
import requests
import aiohttp

from .types import JsonData, QueryParams
from .config import GhostConfig
from .exceptions import GhostAPIError


class BaseHttpClient:
    """Base class for HTTP operations."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize the HTTP client."""
        if not api_key:
            raise ValueError("API key is required")
        self.config = GhostConfig(api_key=api_key, base_url=base_url)


class SyncHttpClient(BaseHttpClient):
    """Synchronous HTTP client implementation."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize the synchronous client."""
        super().__init__(api_key, base_url)
        self.session = requests.Session()

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[QueryParams] = None,
        data: Optional[JsonData] = None,
        **kwargs
    ) -> Any:
        """Make a synchronous HTTP request."""
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


class AsyncHttpClient(BaseHttpClient):
    """Asynchronous HTTP client implementation."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize the asynchronous client."""
        super().__init__(api_key, base_url)
        self._session = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._session:
            await self._session.close()
            self._session = None

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[QueryParams] = None,
        data: Optional[JsonData] = None,
        **kwargs
    ) -> Any:
        """Make an asynchronous HTTP request."""
        if not self._session:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
            
        url = self.config.get_api_url(endpoint)
        
        try:
            async with self._session.request(
                method=method,
                url=url,
                headers=self.config.headers,
                params=params,
                json=data,
                **kwargs
            ) as response:
                response.raise_for_status()
                
                if response.content_length:
                    return await response.json()
                return None
                
        except aiohttp.ClientResponseError as e:
            error_msg = str(e)
            error_response = None
            
            try:
                error_response = await response.json()
                error_msg = error_response.get('message', str(e))
            except (ValueError, AttributeError):
                pass
                
            raise GhostAPIError(
                message=error_msg,
                status_code=e.status if hasattr(e, 'status') else None,
                response=error_response
            )
        except aiohttp.ClientError as e:
            raise GhostAPIError(f"Request failed: {str(e)}")
