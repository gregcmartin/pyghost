"""
Base resource class for the Ghost Security API.
"""
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from datetime import datetime

from ..types import (
    ResourceId, JsonData, QueryParams, PaginationParams,
    OrderingParams, TimeRangeParams, FilterParams
)
from ..http import SyncHttpClient, AsyncHttpClient

T = TypeVar('T', SyncHttpClient, AsyncHttpClient)

class PaginatedResponse:
    """Wrapper for paginated API responses."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize paginated response.
        
        Args:
            data: Raw API response containing pagination data
        """
        self.items = data.get('items', [])
        self.page = data.get('page', 1)
        self.pages = data.get('pages', 1)
        self.size = data.get('size', len(self.items))
        self.total = data.get('total', len(self.items))

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

    def _prepare_params(self, 
                       pagination: Optional[PaginationParams] = None,
                       ordering: Optional[OrderingParams] = None,
                       time_range: Optional[TimeRangeParams] = None,
                       filters: Optional[FilterParams] = None) -> QueryParams:
        """
        Prepare query parameters.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters
            time_range: Time range parameters
            filters: Additional filter parameters
            
        Returns:
            dict: Prepared parameters with null values removed
        """
        params = {}

        # Add pagination params
        if pagination:
            if pagination.page is not None:
                params['page'] = pagination.page
            if pagination.size is not None:
                params['size'] = pagination.size

        # Add ordering params
        if ordering and ordering.order_by:
            params['order_by'] = ordering.order_by

        # Add time range params
        if time_range:
            params['start_date'] = time_range.start_date.isoformat()
            params['end_date'] = time_range.end_date.isoformat()
            params['bin_duration'] = time_range.bin_duration

        # Add filter params
        if filters:
            params.update(filters.filters)

        return {k: v for k, v in params.items() if v is not None}


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
