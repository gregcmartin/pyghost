"""
Infrastructure resources for the Ghost Security API.
"""
from typing import Dict, List, Optional
from datetime import datetime

from ..types import (
    ResourceId, PaginationParams, OrderingParams, FilterParams
)
from .base import SyncResource, AsyncResource, PaginatedResponse


class BaseDomainResource:
    """Base class for domain-related operations."""
    
    RESOURCE_NAME = "domains"

    def _prepare_domain_filters(
        self,
        name: Optional[str] = None,
        is_healthy: Optional[bool] = None,
        first_party: Optional[bool] = None
    ) -> FilterParams:
        """
        Prepare domain-specific filters.
        
        Args:
            name: Filter by domain name (partial match)
            is_healthy: Filter by domain health status
            first_party: Filter by first party status
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            name=name,
            is_healthy=is_healthy,
            first_party=first_party
        )


class BaseHostResource:
    """Base class for host-related operations."""
    
    RESOURCE_NAME = "hosts"

    def _prepare_host_filters(
        self,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        domain_id: Optional[str] = None
    ) -> FilterParams:
        """
        Prepare host-specific filters.
        
        Args:
            name: Filter by host name
            provider: Filter by cloud provider
            domain_id: Filter by domain ID
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            name=name,
            provider=provider,
            domain_id=domain_id
        )


class SyncDomainResource(BaseDomainResource, SyncResource):
    """Synchronous domain resource operations."""
    
    def list_domains(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        is_healthy: Optional[bool] = None,
        first_party: Optional[bool] = None
    ) -> PaginatedResponse:
        """
        List all domains.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters
            name: Filter by domain name (partial match)
            is_healthy: Filter by domain health status
            first_party: Filter by first party status
            
        Returns:
            PaginatedResponse: Paginated list of domains
        """
        filters = self._prepare_domain_filters(name, is_healthy, first_party)
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_domain(self, domain_id: ResourceId) -> Dict:
        """
        Get details for a specific domain.
        
        Args:
            domain_id: Domain identifier
            
        Returns:
            Dict: Domain details
        """
        path = self._build_path(self.RESOURCE_NAME, str(domain_id))
        return self._get(path)


class AsyncDomainResource(BaseDomainResource, AsyncResource):
    """Asynchronous domain resource operations."""
    
    async def list_domains(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        is_healthy: Optional[bool] = None,
        first_party: Optional[bool] = None
    ) -> PaginatedResponse:
        """
        List all domains.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters
            name: Filter by domain name (partial match)
            is_healthy: Filter by domain health status
            first_party: Filter by first party status
            
        Returns:
            PaginatedResponse: Paginated list of domains
        """
        filters = self._prepare_domain_filters(name, is_healthy, first_party)
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_domain(self, domain_id: ResourceId) -> Dict:
        """
        Get details for a specific domain.
        
        Args:
            domain_id: Domain identifier
            
        Returns:
            Dict: Domain details
        """
        path = self._build_path(self.RESOURCE_NAME, str(domain_id))
        return await self._get(path)


class SyncHostResource(BaseHostResource, SyncResource):
    """Synchronous host resource operations."""
    
    def list_hosts(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        domain_id: Optional[str] = None
    ) -> PaginatedResponse:
        """
        List all hosts.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters
            name: Filter by host name
            provider: Filter by cloud provider
            domain_id: Filter by domain ID
            
        Returns:
            PaginatedResponse: Paginated list of hosts
        """
        filters = self._prepare_host_filters(name, provider, domain_id)
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_host(self, host_id: ResourceId) -> Dict:
        """
        Get details for a specific host.
        
        Args:
            host_id: Host identifier
            
        Returns:
            Dict: Host details
        """
        path = self._build_path(self.RESOURCE_NAME, str(host_id))
        return self._get(path)


class AsyncHostResource(BaseHostResource, AsyncResource):
    """Asynchronous host resource operations."""
    
    async def list_hosts(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        domain_id: Optional[str] = None
    ) -> PaginatedResponse:
        """
        List all hosts.
        
        Args:
            pagination: Pagination parameters
            ordering: Ordering parameters
            name: Filter by host name
            provider: Filter by cloud provider
            domain_id: Filter by domain ID
            
        Returns:
            PaginatedResponse: Paginated list of hosts
        """
        filters = self._prepare_host_filters(name, provider, domain_id)
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_host(self, host_id: ResourceId) -> Dict:
        """
        Get details for a specific host.
        
        Args:
            host_id: Host identifier
            
        Returns:
            Dict: Host details
        """
        path = self._build_path(self.RESOURCE_NAME, str(host_id))
        return await self._get(path)
