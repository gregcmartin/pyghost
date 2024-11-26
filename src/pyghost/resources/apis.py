"""
API resources for the Ghost Security API.
"""
from typing import Dict, List

from ..types import ApiId, DEFAULT_BIN_DURATION
from .base import SyncResource, AsyncResource


class BaseApiResource:
    """Base class for API-related operations."""
    
    RESOURCE_NAME = "apis"

    def _get_list_params(self, bin_duration: str = DEFAULT_BIN_DURATION) -> Dict:
        """Get parameters for list operation."""
        return self._prepare_params(bin_duration=bin_duration)


class SyncApiResource(BaseApiResource, SyncResource):
    """Synchronous API resource operations."""
    
    def list_apis(self, bin_duration: str = DEFAULT_BIN_DURATION) -> List[Dict]:
        """
        List all APIs.
        
        Args:
            bin_duration (str): Time window for request aggregation (e.g., "1h", "8h").
                              Must be >= 1h and <= 1d. Must be a multiple of 1h.
            
        Returns:
            List[Dict]: List of APIs
        """
        return self._get(self.RESOURCE_NAME, params=self._get_list_params(bin_duration))

    def get_api(self, api_id: ApiId) -> Dict:
        """
        Get details for a specific API.
        
        Args:
            api_id: API identifier
            
        Returns:
            Dict: API details
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id))
        return self._get(path)

    def get_api_endpoints(self, api_id: ApiId) -> List[Dict]:
        """
        Get endpoints for a specific API.
        
        Args:
            api_id: API identifier
            
        Returns:
            List[Dict]: List of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id), "endpoints")
        return self._get(path)


class AsyncApiResource(BaseApiResource, AsyncResource):
    """Asynchronous API resource operations."""
    
    async def list_apis(self, bin_duration: str = DEFAULT_BIN_DURATION) -> List[Dict]:
        """
        List all APIs.
        
        Args:
            bin_duration (str): Time window for request aggregation (e.g., "1h", "8h").
                              Must be >= 1h and <= 1d. Must be a multiple of 1h.
            
        Returns:
            List[Dict]: List of APIs
        """
        return await self._get(self.RESOURCE_NAME, params=self._get_list_params(bin_duration))

    async def get_api(self, api_id: ApiId) -> Dict:
        """
        Get details for a specific API.
        
        Args:
            api_id: API identifier
            
        Returns:
            Dict: API details
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id))
        return await self._get(path)

    async def get_api_endpoints(self, api_id: ApiId) -> List[Dict]:
        """
        Get endpoints for a specific API.
        
        Args:
            api_id: API identifier
            
        Returns:
            List[Dict]: List of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id), "endpoints")
        return await self._get(path)
