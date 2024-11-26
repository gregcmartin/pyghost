"""
App resources for the Ghost Security API.
"""
from typing import Dict, List

from ..types import ResourceId
from .base import SyncResource, AsyncResource


class BaseAppResource:
    """Base class for app-related operations."""
    
    RESOURCE_NAME = "apps"


class SyncAppResource(BaseAppResource, SyncResource):
    """Synchronous app resource operations."""
    
    def list_apps(self) -> List[Dict]:
        """
        List all apps.
        
        Returns:
            List[Dict]: List of apps
        """
        return self._get(self.RESOURCE_NAME)

    def get_app(self, app_id: ResourceId) -> Dict:
        """
        Get details for a specific app.
        
        Args:
            app_id: App identifier
            
        Returns:
            Dict: App details
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id))
        return self._get(path)

    def get_app_endpoints(self, app_id: ResourceId) -> List[Dict]:
        """
        Get endpoints for a specific app.
        
        Args:
            app_id: App identifier
            
        Returns:
            List[Dict]: List of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "endpoints")
        return self._get(path)

    def get_app_assets(self, app_id: ResourceId) -> List[Dict]:
        """
        Get assets for a specific app.
        
        Args:
            app_id: App identifier
            
        Returns:
            List[Dict]: List of assets
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "assets")
        return self._get(path)


class AsyncAppResource(BaseAppResource, AsyncResource):
    """Asynchronous app resource operations."""
    
    async def list_apps(self) -> List[Dict]:
        """
        List all apps.
        
        Returns:
            List[Dict]: List of apps
        """
        return await self._get(self.RESOURCE_NAME)

    async def get_app(self, app_id: ResourceId) -> Dict:
        """
        Get details for a specific app.
        
        Args:
            app_id: App identifier
            
        Returns:
            Dict: App details
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id))
        return await self._get(path)

    async def get_app_endpoints(self, app_id: ResourceId) -> List[Dict]:
        """
        Get endpoints for a specific app.
        
        Args:
            app_id: App identifier
            
        Returns:
            List[Dict]: List of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "endpoints")
        return await self._get(path)

    async def get_app_assets(self, app_id: ResourceId) -> List[Dict]:
        """
        Get assets for a specific app.
        
        Args:
            app_id: App identifier
            
        Returns:
            List[Dict]: List of assets
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "assets")
        return await self._get(path)
