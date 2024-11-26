"""
Main client module for interacting with the Ghost Security API.
"""

from typing import Any, Dict, List, Optional, Union, Literal
from uuid import UUID

import requests
import aiohttp

from .config import GhostConfig


class GhostAPIError(Exception):
    """Custom exception for Ghost API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class EndpointFilters:
    """Helper class for endpoint filtering parameters."""
    def __init__(self,
                 size: Optional[int] = None,
                 page: Optional[int] = None,
                 order_by: Optional[str] = None,
                 format: Optional[str] = None,
                 method: Optional[List[str]] = None,
                 last_seen: Optional[Literal['day', 'week', 'month', 'year']] = None,
                 search: Optional[str] = None,
                 min_request_count: Optional[int] = None,
                 host_id: Optional[List[str]] = None,
                 is_first_party: Optional[bool] = None,
                 kind: Optional[Literal['html', 'api', 'script', 'unknown']] = None,
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
            last_seen (str, optional): Filter by last seen period ('day', 'week', 'month', 'year')
            search (str, optional): Search for fuzzy matches of path template and host
            min_request_count (int, optional): Only return endpoints with at least this many requests
            host_id (List[str], optional): Filter by host IDs
            is_first_party (bool, optional): Filter by first party endpoints
            kind (str, optional): Filter by endpoint kind ('html', 'api', 'script', 'unknown')
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


class BaseGhostClient:
    """Base class for Ghost Security API clients."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the Ghost Security API client.
        
        Args:
            api_key (str): The API key for authentication
            base_url (str, optional): The base URL for the API.
                                    If not provided, uses the default from GhostConfig.
        """
        if not api_key:
            raise ValueError("API key is required")
        self.config = GhostConfig(api_key=api_key, base_url=base_url or GhostConfig.DEFAULT_BASE_URL)


class GhostClient(BaseGhostClient):
    """Synchronous client for interacting with the Ghost Security API."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize the synchronous client."""
        super().__init__(api_key, base_url)
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, list]] = None,
        **kwargs
    ) -> Any:
        """Make a synchronous request to the Ghost Security API."""
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


class AsyncGhostClient(BaseGhostClient):
    """Asynchronous client for interacting with the Ghost Security API."""
    
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

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, list]] = None,
        **kwargs
    ) -> Any:
        """Make an asynchronous request to the Ghost Security API."""
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


# Define API methods for both sync and async clients
def _define_api_methods(cls):
    """Define API methods for a client class."""
    
    # API Methods
    async def list_apis(self) -> List[Dict]:
        """List all APIs."""
        return await self._request("GET", "apis") if cls == AsyncGhostClient else self._request("GET", "apis")

    async def get_api(self, api_id: Union[str, UUID]) -> Dict:
        """Get details for a specific API."""
        api_id = str(api_id)
        return await self._request("GET", f"apis/{api_id}") if cls == AsyncGhostClient else self._request("GET", f"apis/{api_id}")

    async def get_api_endpoints(self, api_id: Union[str, UUID]) -> List[Dict]:
        """Get endpoints for a specific API."""
        api_id = str(api_id)
        return await self._request("GET", f"apis/{api_id}/endpoints") if cls == AsyncGhostClient else self._request("GET", f"apis/{api_id}/endpoints")

    # App Methods
    async def list_apps(self) -> List[Dict]:
        """List all apps."""
        return await self._request("GET", "apps") if cls == AsyncGhostClient else self._request("GET", "apps")

    async def get_app(self, app_id: Union[str, UUID]) -> Dict:
        """Get details for a specific app."""
        app_id = str(app_id)
        return await self._request("GET", f"apps/{app_id}") if cls == AsyncGhostClient else self._request("GET", f"apps/{app_id}")

    async def get_app_endpoints(self, app_id: Union[str, UUID]) -> List[Dict]:
        """Get endpoints for a specific app."""
        app_id = str(app_id)
        return await self._request("GET", f"apps/{app_id}/endpoints") if cls == AsyncGhostClient else self._request("GET", f"apps/{app_id}/endpoints")

    async def get_app_assets(self, app_id: Union[str, UUID]) -> List[Dict]:
        """Get assets for a specific app."""
        app_id = str(app_id)
        return await self._request("GET", f"apps/{app_id}/assets") if cls == AsyncGhostClient else self._request("GET", f"apps/{app_id}/assets")

    # Campaign Methods
    async def list_campaigns(self) -> List[Dict]:
        """List all campaigns."""
        return await self._request("GET", "campaigns") if cls == AsyncGhostClient else self._request("GET", "campaigns")

    async def get_campaign(self, campaign_id: Union[str, UUID]) -> Dict:
        """Get details for a specific campaign."""
        campaign_id = str(campaign_id)
        return await self._request("GET", f"campaigns/{campaign_id}") if cls == AsyncGhostClient else self._request("GET", f"campaigns/{campaign_id}")

    async def get_campaign_issue_categories(self, campaign_id: Union[str, UUID]) -> List[Dict]:
        """Get issue categories for a specific campaign."""
        campaign_id = str(campaign_id)
        return await self._request("GET", f"campaigns/{campaign_id}/issue_categories") if cls == AsyncGhostClient else self._request("GET", f"campaigns/{campaign_id}/issue_categories")

    async def get_campaign_issues(self, campaign_id: Union[str, UUID]) -> List[Dict]:
        """Get issues for a specific campaign."""
        campaign_id = str(campaign_id)
        return await self._request("GET", f"campaigns/{campaign_id}/issues") if cls == AsyncGhostClient else self._request("GET", f"campaigns/{campaign_id}/issues")

    async def get_campaign_vulnerabilities(self, campaign_id: Union[str, UUID]) -> List[Dict]:
        """Get vulnerabilities for a specific campaign."""
        campaign_id = str(campaign_id)
        return await self._request("GET", f"campaigns/{campaign_id}/vulnerabilities") if cls == AsyncGhostClient else self._request("GET", f"campaigns/{campaign_id}/vulnerabilities")

    # Domain Methods
    async def list_domains(self) -> List[Dict]:
        """List all domains."""
        return await self._request("GET", "domains") if cls == AsyncGhostClient else self._request("GET", "domains")

    async def get_domain(self, domain_id: Union[str, UUID]) -> Dict:
        """Get details for a specific domain."""
        domain_id = str(domain_id)
        return await self._request("GET", f"domains/{domain_id}") if cls == AsyncGhostClient else self._request("GET", f"domains/{domain_id}")

    # Endpoint Methods
    async def list_endpoints(self, filters: Optional[EndpointFilters] = None) -> List[Dict]:
        """List all endpoints with optional filtering."""
        params = filters.filters if filters else None
        return await self._request("GET", "endpoints", params=params) if cls == AsyncGhostClient else self._request("GET", "endpoints", params=params)

    async def get_endpoint_count(self, filters: Optional[EndpointFilters] = None) -> Dict:
        """Get count of endpoints matching supplied filters."""
        params = filters.filters if filters else None
        return await self._request("GET", "endpoints/count", params=params) if cls == AsyncGhostClient else self._request("GET", "endpoints/count", params=params)

    async def get_endpoint(self, endpoint_id: Union[str, UUID]) -> Dict:
        """Get details for a specific endpoint."""
        endpoint_id = str(endpoint_id)
        return await self._request("GET", f"endpoints/{endpoint_id}") if cls == AsyncGhostClient else self._request("GET", f"endpoints/{endpoint_id}")

    async def get_endpoint_activity(self, endpoint_id: Union[str, UUID]) -> Dict:
        """Get request volume activity for a specific endpoint."""
        endpoint_id = str(endpoint_id)
        return await self._request("GET", f"endpoints/{endpoint_id}/activity") if cls == AsyncGhostClient else self._request("GET", f"endpoints/{endpoint_id}/activity")

    async def get_endpoint_apps(self, endpoint_id: Union[str, UUID]) -> List[Dict]:
        """Get apps associated with a specific endpoint."""
        endpoint_id = str(endpoint_id)
        return await self._request("GET", f"endpoints/{endpoint_id}/apps") if cls == AsyncGhostClient else self._request("GET", f"endpoints/{endpoint_id}/apps")

    # Host Methods
    async def list_hosts(self) -> List[Dict]:
        """List all hosts."""
        return await self._request("GET", "hosts") if cls == AsyncGhostClient else self._request("GET", "hosts")

    async def get_host(self, host_id: Union[str, UUID]) -> Dict:
        """Get details for a specific host."""
        host_id = str(host_id)
        return await self._request("GET", f"hosts/{host_id}") if cls == AsyncGhostClient else self._request("GET", f"hosts/{host_id}")

    # Issue Category Methods
    async def list_issue_categories(self) -> List[Dict]:
        """List all issue categories."""
        return await self._request("GET", "issue_categories") if cls == AsyncGhostClient else self._request("GET", "issue_categories")

    async def get_issue_category(self, category_id: Union[str, UUID]) -> Dict:
        """Get details for a specific issue category."""
        category_id = str(category_id)
        return await self._request("GET", f"issue_categories/{category_id}") if cls == AsyncGhostClient else self._request("GET", f"issue_categories/{category_id}")

    # Issue Methods
    async def list_issues(self) -> List[Dict]:
        """List all issues."""
        return await self._request("GET", "issues") if cls == AsyncGhostClient else self._request("GET", "issues")

    async def get_issue(self, issue_id: Union[str, UUID]) -> Dict:
        """Get details for a specific issue."""
        issue_id = str(issue_id)
        return await self._request("GET", f"issues/{issue_id}") if cls == AsyncGhostClient else self._request("GET", f"issues/{issue_id}")

    # Vulnerability Methods
    async def list_vulnerabilities(self) -> List[Dict]:
        """List all vulnerabilities."""
        return await self._request("GET", "vulnerabilities") if cls == AsyncGhostClient else self._request("GET", "vulnerabilities")

    async def get_vulnerability(self, vulnerability_id: Union[str, UUID]) -> Dict:
        """Get details for a specific vulnerability."""
        vulnerability_id = str(vulnerability_id)
        return await self._request("GET", f"vulnerabilities/{vulnerability_id}") if cls == AsyncGhostClient else self._request("GET", f"vulnerabilities/{vulnerability_id}")

    # Base HTTP method implementations
    async def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Any:
        """Send a GET request to the API."""
        return await self._request("GET", endpoint, params=params, **kwargs) if cls == AsyncGhostClient else self._request("GET", endpoint, params=params, **kwargs)
        
    async def post(self, endpoint: str, data: Optional[Union[Dict, list]] = None, **kwargs) -> Any:
        """Send a POST request to the API."""
        return await self._request("POST", endpoint, data=data, **kwargs) if cls == AsyncGhostClient else self._request("POST", endpoint, data=data, **kwargs)
        
    async def put(self, endpoint: str, data: Optional[Union[Dict, list]] = None, **kwargs) -> Any:
        """Send a PUT request to the API."""
        return await self._request("PUT", endpoint, data=data, **kwargs) if cls == AsyncGhostClient else self._request("PUT", endpoint, data=data, **kwargs)
        
    async def delete(self, endpoint: str, **kwargs) -> Any:
        """Send a DELETE request to the API."""
        return await self._request("DELETE", endpoint, **kwargs) if cls == AsyncGhostClient else self._request("DELETE", endpoint, **kwargs)

    # Add all methods to the class
    for name, method in locals().copy().items():
        if not name.startswith('_'):
            setattr(cls, name, method)

# Apply API methods to both client classes
_define_api_methods(GhostClient)
_define_api_methods(AsyncGhostClient)
