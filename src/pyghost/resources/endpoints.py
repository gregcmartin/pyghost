"""
Endpoint resources for the Ghost Security API.
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta

from ..types import ResourceId, EndpointKind, LastSeenPeriod
from .base import SyncResource, AsyncResource


def format_rfc3339(dt: datetime) -> str:
    """Format datetime to RFC3339 format."""
    return dt.isoformat() + "Z"


def get_default_time_range(hours: int = 24) -> tuple[str, str]:
    """
    Get default time range for activity queries.
    
    Args:
        hours: Number of hours to look back
        
    Returns:
        tuple: (start_date, end_date) in RFC3339 format
    """
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    return format_rfc3339(start), format_rfc3339(end)


class EndpointFilters:
    """Helper class for endpoint filtering parameters."""
    def __init__(self,
                 size: Optional[int] = None,
                 page: Optional[int] = None,
                 order_by: Optional[str] = None,
                 format: Optional[str] = None,
                 method: Optional[List[str]] = None,
                 last_seen: Optional[str] = None,
                 search: Optional[str] = None,
                 min_request_count: Optional[int] = None,
                 host_id: Optional[List[str]] = None,
                 is_first_party: Optional[bool] = None,
                 kind: Optional[str] = None,
                 port: Optional[List[int]] = None,
                 min_request_rate: Optional[int] = None):
        """
        Initialize endpoint filters.
        
        Args:
            size (int, optional): Results per page
            page (int, optional): Page number
            order_by (str, optional): Ordering attribute with optional '-' prefix for descending order
            format (str, optional): Filter by endpoint format (currently only REST)
            method (List[str], optional): Filter by HTTP methods e.g. ['GET', 'POST']
            last_seen (str, optional): Filter by last seen period (day, week, month, year)
            search (str, optional): Search for fuzzy matches of path template and host
            min_request_count (int, optional): Only return endpoints with at least this many requests
            host_id (List[str], optional): Filter by host IDs
            is_first_party (bool, optional): Filter by first party endpoints
            kind (str, optional): Filter by endpoint kind (html, api, script, unknown)
            port (List[int], optional): Filter by specific ports
            min_request_rate (int, optional): Only return endpoints with this request rate over last 30 days
        """
        self.filters = {}
        if size is not None:
            self.filters['size'] = size
        if page is not None:
            self.filters['page'] = page
        if order_by is not None:
            self.filters['order_by'] = order_by
        if format is not None:
            self.filters['format'] = format
        if method is not None:
            self.filters['method'] = method
        if last_seen is not None:
            self.filters['last_seen'] = last_seen
        if search is not None:
            self.filters['search'] = search
        if min_request_count is not None:
            self.filters['min_request_count'] = min_request_count
        if host_id is not None:
            self.filters['host_id'] = host_id
        if is_first_party is not None:
            self.filters['is_first_party'] = is_first_party
        if kind is not None:
            self.filters['kind'] = kind
        if port is not None:
            self.filters['port'] = port
        if min_request_rate is not None:
            self.filters['min_request_rate'] = min_request_rate


class BaseEndpointResource:
    """Base class for endpoint-related operations."""
    
    RESOURCE_NAME = "endpoints"


class SyncEndpointResource(BaseEndpointResource, SyncResource):
    """Synchronous endpoint resource operations."""
    
    def list_endpoints(self, filters: Optional[EndpointFilters] = None) -> List[Dict]:
        """
        List all endpoints with optional filtering.
        
        Args:
            filters: Optional filtering parameters
            
        Returns:
            List[Dict]: List of endpoints
        """
        params = filters.filters if filters else None
        return self._get(self.RESOURCE_NAME, params=params)

    def get_endpoint_count(self, filters: Optional[EndpointFilters] = None) -> Dict:
        """
        Get count of endpoints matching supplied filters.
        
        Args:
            filters: Optional filtering parameters
            
        Returns:
            Dict: Count information
        """
        params = filters.filters if filters else None
        return self._get(f"{self.RESOURCE_NAME}/count", params=params)

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
        bin_duration: str = "1h",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        hours_back: int = 24
    ) -> Dict:
        """
        Get request volume activity for a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            bin_duration: Time window for request aggregation (e.g., "1h", "8h").
                        Must be >= 1h and <= 1d. Must be a multiple of 1h.
            start_date: Start date in RFC3339 format. If not provided,
                       defaults to hours_back hours ago.
            end_date: End date in RFC3339 format. If not provided,
                     defaults to current time.
            hours_back: Number of hours to look back if start_date/end_date
                       not provided. Defaults to 24 hours.
            
        Returns:
            Dict: Activity information
        """
        if not start_date or not end_date:
            start_date, end_date = get_default_time_range(hours_back)
            
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "activity")
        params = {
            "bin_duration": bin_duration,
            "start_date": start_date,
            "end_date": end_date
        }
        return self._get(path, params=params)

    def get_endpoint_apps(self, endpoint_id: ResourceId) -> List[Dict]:
        """
        Get apps associated with a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            
        Returns:
            List[Dict]: List of associated apps
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "apps")
        return self._get(path)


class AsyncEndpointResource(BaseEndpointResource, AsyncResource):
    """Asynchronous endpoint resource operations."""
    
    async def list_endpoints(self, filters: Optional[EndpointFilters] = None) -> List[Dict]:
        """
        List all endpoints with optional filtering.
        
        Args:
            filters: Optional filtering parameters
            
        Returns:
            List[Dict]: List of endpoints
        """
        params = filters.filters if filters else None
        return await self._get(self.RESOURCE_NAME, params=params)

    async def get_endpoint_count(self, filters: Optional[EndpointFilters] = None) -> Dict:
        """
        Get count of endpoints matching supplied filters.
        
        Args:
            filters: Optional filtering parameters
            
        Returns:
            Dict: Count information
        """
        params = filters.filters if filters else None
        return await self._get(f"{self.RESOURCE_NAME}/count", params=params)

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
        bin_duration: str = "1h",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        hours_back: int = 24
    ) -> Dict:
        """
        Get request volume activity for a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            bin_duration: Time window for request aggregation (e.g., "1h", "8h").
                        Must be >= 1h and <= 1d. Must be a multiple of 1h.
            start_date: Start date in RFC3339 format. If not provided,
                       defaults to hours_back hours ago.
            end_date: End date in RFC3339 format. If not provided,
                     defaults to current time.
            hours_back: Number of hours to look back if start_date/end_date
                       not provided. Defaults to 24 hours.
            
        Returns:
            Dict: Activity information
        """
        if not start_date or not end_date:
            start_date, end_date = get_default_time_range(hours_back)
            
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "activity")
        params = {
            "bin_duration": bin_duration,
            "start_date": start_date,
            "end_date": end_date
        }
        return await self._get(path, params=params)

    async def get_endpoint_apps(self, endpoint_id: ResourceId) -> List[Dict]:
        """
        Get apps associated with a specific endpoint.
        
        Args:
            endpoint_id: Endpoint identifier
            
        Returns:
            List[Dict]: List of associated apps
        """
        path = self._build_path(self.RESOURCE_NAME, str(endpoint_id), "apps")
        return await self._get(path)
