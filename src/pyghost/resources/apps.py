"""
App resources for the Ghost Security API.
"""
from typing import Dict, List, Optional
from datetime import datetime

from ..types import (
    ResourceId, PaginationParams, OrderingParams, FilterParams,
    EndpointKind
)
from .base import SyncResource, AsyncResource, PaginatedResponse


class BaseAppResource:
    """Base class for app-related operations."""
    
    RESOURCE_NAME = "apps"

    def _prepare_app_filters(
        self,
        name: Optional[str] = None,
        scanned_after: Optional[datetime] = None,
    ) -> FilterParams:
        """
        Prepare app-specific filters.
        
        Args:
            name: Filter by app name (partial match)
            scanned_after: Filter by last scan time
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            name=name,
            scanned_after=scanned_after.timestamp() if scanned_after else None
        )


class SyncAppResource(BaseAppResource, SyncResource):
    """Synchronous app resource operations."""
    
    def list_apps(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        scanned_after: Optional[datetime] = None
    ) -> PaginatedResponse:
        """
        List all apps.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: name, created_at, updated_at, last_scanned_at)
            name: Filter by app name (partial match)
            scanned_after: Filter by last scan time
            
        Returns:
            PaginatedResponse: Paginated list of apps
        """
        filters = self._prepare_app_filters(name, scanned_after)
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

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

    def list_app_endpoints(
        self,
        app_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        kind: Optional[str] = None,
        is_first_party: Optional[bool] = None
    ) -> PaginatedResponse:
        """
        Get endpoints for a specific app.
        
        Args:
            app_id: App identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: host.name, last_scanned_at, path_template, is_first_party)
            kind: Filter by endpoint kind (api, script, html, unknown)
            is_first_party: Filter for first party endpoints
            
        Returns:
            PaginatedResponse: Paginated list of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "endpoints")
        filters = FilterParams(kind=kind, is_first_party=is_first_party)
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(path, params=params))

    def list_app_assets(
        self,
        app_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None
    ) -> PaginatedResponse:
        """
        List assets for a specific app.
        
        Args:
            app_id: App identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: path, last_seen_at, kind)
            
        Returns:
            PaginatedResponse: Paginated list of assets
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "assets")
        params = self._prepare_params(pagination, ordering)
        return PaginatedResponse(self._get(path, params=params))


class AsyncAppResource(BaseAppResource, AsyncResource):
    """Asynchronous app resource operations."""
    
    async def list_apps(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        scanned_after: Optional[datetime] = None
    ) -> PaginatedResponse:
        """
        List all apps.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: name, created_at, updated_at, last_scanned_at)
            name: Filter by app name (partial match)
            scanned_after: Filter by last scan time
            
        Returns:
            PaginatedResponse: Paginated list of apps
        """
        filters = self._prepare_app_filters(name, scanned_after)
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

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

    async def list_app_endpoints(
        self,
        app_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        kind: Optional[str] = None,
        is_first_party: Optional[bool] = None
    ) -> PaginatedResponse:
        """
        Get endpoints for a specific app.
        
        Args:
            app_id: App identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: host.name, last_scanned_at, path_template, is_first_party)
            kind: Filter by endpoint kind (api, script, html, unknown)
            is_first_party: Filter for first party endpoints
            
        Returns:
            PaginatedResponse: Paginated list of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "endpoints")
        filters = FilterParams(kind=kind, is_first_party=is_first_party)
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(path, params=params)
        return PaginatedResponse(response)

    async def list_app_assets(
        self,
        app_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None
    ) -> PaginatedResponse:
        """
        List assets for a specific app.
        
        Args:
            app_id: App identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: path, last_seen_at, kind)
            
        Returns:
            PaginatedResponse: Paginated list of assets
        """
        path = self._build_path(self.RESOURCE_NAME, str(app_id), "assets")
        params = self._prepare_params(pagination, ordering)
        response = await self._get(path, params=params)
        return PaginatedResponse(response)
