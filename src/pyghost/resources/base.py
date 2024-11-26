"""
Base resource class for the Ghost Security API.
"""
from typing import Any, Dict, List, Optional, TypeVar, Generic

from ..types import ResourceId, JsonData, QueryParams
from ..http import SyncHttpClient, AsyncHttpClient

T = TypeVar('T', SyncHttpClient, AsyncHttpClient)


class BaseResource(Generic[T]):
    """Base class for API resources."""
    
    def __init__(self, client: T):
        """
        Initialize the resource.
        
        Args:
            client: HTTP client instance
        """
        self.client = client

    def _build_path(self, *parts: str) -> str:
        """
        Build API path from parts.
        
        Args:
            *parts: Path parts to join
            
        Returns:
            str: Complete API path
        """
        return '/'.join(str(part).strip('/') for part in parts if part)

    def _prepare_params(self, **kwargs) -> QueryParams:
        """
        Prepare query parameters.
        
        Args:
            **kwargs: Parameters to include
            
        Returns:
            dict: Prepared parameters with null values removed
        """
        return {k: v for k, v in kwargs.items() if v is not None}


class SyncResource(BaseResource[SyncHttpClient]):
    """Base class for synchronous API resources."""
    
    def _get(self, path: str, params: Optional[QueryParams] = None) -> Any:
        """Send GET request."""
        return self.client._request("GET", path, params=params)

    def _post(self, path: str, data: Optional[JsonData] = None, params: Optional[QueryParams] = None) -> Any:
        """Send POST request."""
        return self.client._request("POST", path, data=data, params=params)

    def _put(self, path: str, data: Optional[JsonData] = None, params: Optional[QueryParams] = None) -> Any:
        """Send PUT request."""
        return self.client._request("PUT", path, data=data, params=params)

    def _delete(self, path: str, params: Optional[QueryParams] = None) -> Any:
        """Send DELETE request."""
        return self.client._request("DELETE", path, params=params)


class AsyncResource(BaseResource[AsyncHttpClient]):
    """Base class for asynchronous API resources."""
    
    async def _get(self, path: str, params: Optional[QueryParams] = None) -> Any:
        """Send GET request."""
        return await self.client._request("GET", path, params=params)

    async def _post(self, path: str, data: Optional[JsonData] = None, params: Optional[QueryParams] = None) -> Any:
        """Send POST request."""
        return await self.client._request("POST", path, data=data, params=params)

    async def _put(self, path: str, data: Optional[JsonData] = None, params: Optional[QueryParams] = None) -> Any:
        """Send PUT request."""
        return await self.client._request("PUT", path, data=data, params=params)

    async def _delete(self, path: str, params: Optional[QueryParams] = None) -> Any:
        """Send DELETE request."""
        return await self.client._request("DELETE", path, params=params)
