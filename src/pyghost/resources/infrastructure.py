"""
Infrastructure resources (domains and hosts) for the Ghost Security API.
"""
from typing import Dict, List

from ..types import ResourceId
from .base import SyncResource, AsyncResource


class BaseDomainResource:
    """Base class for domain-related operations."""
    
    RESOURCE_NAME = "domains"


class BaseHostResource:
    """Base class for host-related operations."""
    
    RESOURCE_NAME = "hosts"


class SyncDomainResource(BaseDomainResource, SyncResource):
    """Synchronous domain resource operations."""
    
    def list_domains(self) -> List[Dict]:
        """
        List all domains.
        
        Returns:
            List[Dict]: List of domains
        """
        return self._get(self.RESOURCE_NAME)

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
    
    async def list_domains(self) -> List[Dict]:
        """
        List all domains.
        
        Returns:
            List[Dict]: List of domains
        """
        return await self._get(self.RESOURCE_NAME)

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
    
    def list_hosts(self) -> List[Dict]:
        """
        List all hosts.
        
        Returns:
            List[Dict]: List of hosts
        """
        return self._get(self.RESOURCE_NAME)

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
    
    async def list_hosts(self) -> List[Dict]:
        """
        List all hosts.
        
        Returns:
            List[Dict]: List of hosts
        """
        return await self._get(self.RESOURCE_NAME)

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
