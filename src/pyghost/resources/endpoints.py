"""
Endpoint resources for the Ghost Security API.
"""
from typing import Dict, List, Optional, Union
from datetime import datetime

from ..types import (
    ResourceId, PaginationParams, OrderingParams, FilterParams,
    TimeRangeParams, LastSeenPeriod, EndpointKind
)
from .base import SyncResource, AsyncResource, PaginatedResponse


class BaseEndpointResource:
    """Base class for endpoint-related operations."""
    
    RESOURCE_NAME = "endpoints"

    def _prepare_endpoint_filters(
        self,
        format: Optional[str] = None,
        methods: Optional[List[str]] = None,
        last_seen: Optional[str] = None,
        search: Optional[str] = None,
        min_request_count: Optional[int] = None,
        host_ids: Optional[List[str]] = None,
        is_first_party: Optional[bool] = None,
        kind: Optional[str] = None,
        ports: Optional[List[int]] = None,
        min_request_rate: Optional[int] = None
    ) -> FilterParams:
        """
        Prepare endpoint-specific filters.
        
        Args:
            format: Filter by endpoint format (e.g., 'REST')
            methods: Filter by HTTP methods
            last_seen: Filter by last seen period
            search: Search term for path template and host
            min_request_count: Minimum request count filter
            host_ids: Filter by host IDs
            is_first_party: Filter by first party status
            kind: Filter by endpoint kind
            ports: Filter by ports
            min_request_rate: Minimum request rate filter
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            format=format,
            method=methods,
            last_seen=last_seen,
            search=search,
            min_request_count=min_request_count,
            host_id=host_ids,
            is_first_party=is_first_party,
            kind=kind,
            port=ports,
            min_request_rate=min_request_rate
        )


class SyncEndpointResource(BaseEndpointResource, SyncResource):
    """Synchronous endpoint resource operations."""
    
    def list_endpoints(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        format: Optional[str] = None,
        methods: Optional[List[str]] = None,
        last_seen: Optional[str] = None,
        search: Optional[str] = None,
        min_request_count: Optional[int] = None,
        host_ids: Optional[List[str]] = None,
        is_first_party: Optional[bool] = None,
        kind: Optional[str] = None,
        ports: Optional[List[int]] = None,
        min_request_rate: Optional[int] = None
    ) -> PaginatedResponse:
        """
        List all endpoints.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters
            format: Filter by endpoint format (e.g., 'REST')
            methods: Filter by HTTP methods
            last_seen: Filter by last seen period
            search: Search term for path template and host
            min_request_count: Minimum request count filter
            host_ids: Filter by host IDs
            is_first_party: Filter by first party status
            kind: Filter by endpoint kind
            ports: Filter by ports
            min_request_rate: Minimum request rate filter
            
        Returns:
            PaginatedResponse: Paginated list of endpoints
        """
        filters = self._prepare_endpoint_filters(
            format, methods, last_seen, search, min_request_count,
            host_ids, is_first_party, kind, ports, min_request_rate
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_endpoint(self, endpoint_id: ResourceId) -> Dict:
        """
        Get details for a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            
        Returns:
            Dict: Endpoint details
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id))
        return self._get(path)

    def get_endpoint_activity(
        self,
        endpoint_id: ResourceId,
        time_range: TimeRangeParams
    ) -> Dict:
        """
        Get activity data for a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            time_range: Time range parameters for activity data
            
        Returns:
            Dict: Endpoint activity data
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "activity")
        params = self._prepare_params(time_range=time_range)
        return self._get(path, params=params)

    def list_endpoint_apps(
        self,
        endpoint_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        scanned_after: Optional[datetime] = None
    ) -> PaginatedResponse:
        """
        List apps that use a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: name, last_scanned_at)
            scanned_after: Filter by scan time
            
        Returns:
            PaginatedResponse: Paginated list of apps
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "apps")
        filters = FilterParams(
            scanned_after=scanned_after.isoformat() if scanned_after else None
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(path, params=params))

    def get_endpoints_count(
        self,
        format: Optional[str] = None,
        methods: Optional[List[str]] = None,
        last_seen: Optional[str] = None,
        search: Optional[str] = None,
        min_request_count: Optional[int] = None,
        host_ids: Optional[List[str]] = None,
        is_first_party: Optional[bool] = None,
        kind: Optional[str] = None,
        ports: Optional[List[int]] = None,
        min_request_rate: Optional[int] = None
    ) -> Dict:
        """
        Get count of endpoints matching filters.
        
        Args:
            format: Filter by endpoint format (e.g., 'REST')
            methods: Filter by HTTP methods
            last_seen: Filter by last seen period
            search: Search term for path template and host
            min_request_count: Minimum request count filter
            host_ids: Filter by host IDs
            is_first_party: Filter by first party status
            kind: Filter by endpoint kind
            ports: Filter by ports
            min_request_rate: Minimum request rate filter
            
        Returns:
            Dict: Endpoint count
        """
        path = self._build_path(self.RESOURCE_NAME, "count")
        filters = self._prepare_endpoint_filters(
            format, methods, last_seen, search, min_request_count,
            host_ids, is_first_party, kind, ports, min_request_rate
        )
        params = self._prepare_params(filters=filters)
        return self._get(path, params=params)


class AsyncEndpointResource(BaseEndpointResource, AsyncResource):
    """Asynchronous endpoint resource operations."""
    
    async def list_endpoints(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        format: Optional[str] = None,
        methods: Optional[List[str]] = None,
        last_seen: Optional[str] = None,
        search: Optional[str] = None,
        min_request_count: Optional[int] = None,
        host_ids: Optional[List[str]] = None,
        is_first_party: Optional[bool] = None,
        kind: Optional[str] = None,
        ports: Optional[List[int]] = None,
        min_request_rate: Optional[int] = None
    ) -> PaginatedResponse:
        """
        List all endpoints.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters
            format: Filter by endpoint format (e.g., 'REST')
            methods: Filter by HTTP methods
            last_seen: Filter by last seen period
            search: Search term for path template and host
            min_request_count: Minimum request count filter
            host_ids: Filter by host IDs
            is_first_party: Filter by first party status
            kind: Filter by endpoint kind
            ports: Filter by ports
            min_request_rate: Minimum request rate filter
            
        Returns:
            PaginatedResponse: Paginated list of endpoints
        """
        filters = self._prepare_endpoint_filters(
            format, methods, last_seen, search, min_request_count,
            host_ids, is_first_party, kind, ports, min_request_rate
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_endpoint(self, endpoint_id: ResourceId) -> Dict:
        """
        Get details for a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            
        Returns:
            Dict: Endpoint details
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id))
        return await self._get(path)

    async def get_endpoint_activity(
        self,
        endpoint_id: ResourceId,
        time_range: TimeRangeParams
    ) -> Dict:
        """
        Get activity data for a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            time_range: Time range parameters for activity data
            
        Returns:
            Dict: Endpoint activity data
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "activity")
        params = self._prepare_params(time_range=time_range)
        return await self._get(path, params=params)

    async def list_endpoint_apps(
        self,
        endpoint_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        scanned_after: Optional[datetime] = None
    ) -> PaginatedResponse:
        """
        List apps that use a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            pagination: Pagination parameters
            ordering: Ordering parameters (valid fields: name, last_scanned_at)
            scanned_after: Filter by scan time
            
        Returns:
            PaginatedResponse: Paginated list of apps
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "apps")
        filters = FilterParams(
            scanned_after=scanned_after.isoformat() if scanned_after else None
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(path, params=params)
        return PaginatedResponse(response)

    async def get_endpoints_count(
        self,
        format: Optional[str] = None,
        methods: Optional[List[str]] = None,
        last_seen: Optional[str] = None,
        search: Optional[str] = None,
        min_request_count: Optional[int] = None,
        host_ids: Optional[List[str]] = None,
        is_first_party: Optional[bool] = None,
        kind: Optional[str] = None,
        ports: Optional[List[int]] = None,
        min_request_rate: Optional[int] = None
    ) -> Dict:
        """
        Get count of endpoints matching filters.
        
        Args:
            format: Filter by endpoint format (e.g., 'REST')
            methods: Filter by HTTP methods
            last_seen: Filter by last seen period
            search: Search term for path template and host
            min_request_count: Minimum request count filter
            host_ids: Filter by host IDs
            is_first_party: Filter by first party status
            kind: Filter by endpoint kind
            ports: Filter by ports
            min_request_rate: Minimum request rate filter
            
        Returns:
            Dict: Endpoint count
        """
        path = self._build_path(self.RESOURCE_NAME, "count")
        filters = self._prepare_endpoint_filters(
            format, methods, last_seen, search, min_request_count,
            host_ids, is_first_party, kind, ports, min_request_rate
        )
        params = self._prepare_params(filters=filters)
        return await self._get(path, params=params)
