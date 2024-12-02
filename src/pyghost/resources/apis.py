"""
API resources for the Ghost Security API.
"""
from typing import Dict, List, Optional
from datetime import datetime

from ..types import (
    ResourceId, PaginationParams, OrderingParams, FilterParams,
    TimeRangeParams, TimeSeries
)
from .base import SyncResource, AsyncResource, PaginatedResponse


class BaseApiResource:
    """Base class for API-related operations."""
    
    RESOURCE_NAME = "apis"

    def _prepare_api_filters(
        self,
        host_name: Optional[str] = None,
    ) -> FilterParams:
        """
        Prepare API-specific filters.
        
        Args:
            host_name: Filter by host name
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(**{
            "host.name": host_name
        } if host_name else {})


class SyncApiResource(BaseApiResource, SyncResource):
    """Synchronous API resource operations."""
    
    def list_apis(
        self,
        time_range: TimeRangeParams,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        host_name: Optional[str] = None
    ) -> PaginatedResponse:
        """
        List all APIs.
        
        Args:
            time_range: Time range parameters for traffic data
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: host.name, endpoint_count)
            host_name: Filter by host name
            
        Returns:
            PaginatedResponse: Paginated list of APIs
        """
        filters = self._prepare_api_filters(host_name)
        params = self._prepare_params(pagination, ordering, time_range, filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_api(
        self,
        api_id: ResourceId,
        time_range: TimeRangeParams
    ) -> Dict:
        """
        Get details for a specific API.
        
        Args:
            api_id: API identifier
            time_range: Time range parameters for traffic data
            
        Returns:
            Dict: API details including traffic volume data
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id))
        params = self._prepare_params(time_range=time_range)
        return self._get(path, params=params)

    def list_api_endpoints(
        self,
        api_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        last_traffic_after: Optional[datetime] = None,
        min_request_count: Optional[int] = None
    ) -> PaginatedResponse:
        """
        List endpoints for a specific API.
        
        Args:
            api_id: API identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: path_template, method, created_at, last_traffic_at, request_rate, request_count)
            last_traffic_after: Filter by last traffic time
            min_request_count: Filter by minimum request count
            
        Returns:
            PaginatedResponse: Paginated list of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id), "endpoints")
        filters = FilterParams(
            last_traffic_after=last_traffic_after.isoformat() if last_traffic_after else None,
            min_request_count=min_request_count
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(path, params=params))


class AsyncApiResource(BaseApiResource, AsyncResource):
    """Asynchronous API resource operations."""
    
    async def list_apis(
        self,
        time_range: TimeRangeParams,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        host_name: Optional[str] = None
    ) -> PaginatedResponse:
        """
        List all APIs.
        
        Args:
            time_range: Time range parameters for traffic data
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: host.name, endpoint_count)
            host_name: Filter by host name
            
        Returns:
            PaginatedResponse: Paginated list of APIs
        """
        filters = self._prepare_api_filters(host_name)
        params = self._prepare_params(pagination, ordering, time_range, filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_api(
        self,
        api_id: ResourceId,
        time_range: TimeRangeParams
    ) -> Dict:
        """
        Get details for a specific API.
        
        Args:
            api_id: API identifier
            time_range: Time range parameters for traffic data
            
        Returns:
            Dict: API details including traffic volume data
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id))
        params = self._prepare_params(time_range=time_range)
        return await self._get(path, params=params)

    async def list_api_endpoints(
        self,
        api_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        last_traffic_after: Optional[datetime] = None,
        min_request_count: Optional[int] = None
    ) -> PaginatedResponse:
        """
        List endpoints for a specific API.
        
        Args:
            api_id: API identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: path_template, method, created_at, last_traffic_at, request_rate, request_count)
            last_traffic_after: Filter by last traffic time
            min_request_count: Filter by minimum request count
            
        Returns:
            PaginatedResponse: Paginated list of endpoints
        """
        path = self._build_path(self.RESOURCE_NAME, str(api_id), "endpoints")
        filters = FilterParams(
            last_traffic_after=last_traffic_after.isoformat() if last_traffic_after else None,
            min_request_count=min_request_count
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(path, params=params)
        return PaginatedResponse(response)
