"""
Main client module for interacting with the Ghost Security API.
"""
from typing import Optional

from .http import SyncHttpClient, AsyncHttpClient
from .resources.apis import SyncApiResource, AsyncApiResource
from .resources.apps import SyncAppResource, AsyncAppResource
from .resources.campaigns import SyncCampaignResource, AsyncCampaignResource
from .resources.endpoints import SyncEndpointResource, AsyncEndpointResource
from .resources.infrastructure import (
    SyncDomainResource, AsyncDomainResource,
    SyncHostResource, AsyncHostResource
)
from .resources.security import (
    SyncIssueCategoryResource, AsyncIssueCategoryResource,
    SyncIssueResource, AsyncIssueResource,
    SyncVulnerabilityResource, AsyncVulnerabilityResource
)


class GhostClient:
    """Synchronous client for interacting with the Ghost Security API."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the Ghost Security API client.
        
        Args:
            api_key (str): The API key for authentication
            base_url (str, optional): The base URL for the API.
                                    If not provided, uses the default from config.
        """
        http_client = SyncHttpClient(api_key=api_key, base_url=base_url)
        
        # Initialize resources
        self.apis = SyncApiResource(http_client)
        self.apps = SyncAppResource(http_client)
        self.campaigns = SyncCampaignResource(http_client)
        self.endpoints = SyncEndpointResource(http_client)
        self.domains = SyncDomainResource(http_client)
        self.hosts = SyncHostResource(http_client)
        self.issue_categories = SyncIssueCategoryResource(http_client)
        self.issues = SyncIssueResource(http_client)
        self.vulnerabilities = SyncVulnerabilityResource(http_client)


class AsyncGhostClient:
    """Asynchronous client for interacting with the Ghost Security API."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the Ghost Security API client.
        
        Args:
            api_key (str): The API key for authentication
            base_url (str, optional): The base URL for the API.
                                    If not provided, uses the default from config.
        """
        self.http_client = AsyncHttpClient(api_key=api_key, base_url=base_url)
        
        # Initialize resources
        self.apis = AsyncApiResource(self.http_client)
        self.apps = AsyncAppResource(self.http_client)
        self.campaigns = AsyncCampaignResource(self.http_client)
        self.endpoints = AsyncEndpointResource(self.http_client)
        self.domains = AsyncDomainResource(self.http_client)
        self.hosts = AsyncHostResource(self.http_client)
        self.issue_categories = AsyncIssueCategoryResource(self.http_client)
        self.issues = AsyncIssueResource(self.http_client)
        self.vulnerabilities = AsyncVulnerabilityResource(self.http_client)

    async def __aenter__(self):
        """Async context manager entry."""
        await self.http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.http_client.__aexit__(exc_type, exc_val, exc_tb)
