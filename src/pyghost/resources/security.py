"""
Security resources (issues, issue categories, and vulnerabilities) for the Ghost Security API.
"""
from typing import Dict, List

from ..types import ResourceId
from .base import SyncResource, AsyncResource


class BaseIssueResource:
    """Base class for issue-related operations."""
    
    RESOURCE_NAME = "issues"


class BaseIssueCategoryResource:
    """Base class for issue category-related operations."""
    
    RESOURCE_NAME = "issue_categories"


class BaseVulnerabilityResource:
    """Base class for vulnerability-related operations."""
    
    RESOURCE_NAME = "vulnerabilities"


class SyncIssueResource(BaseIssueResource, SyncResource):
    """Synchronous issue resource operations."""
    
    def list_issues(self) -> List[Dict]:
        """
        List all issues.
        
        Returns:
            List[Dict]: List of issues
        """
        return self._get(self.RESOURCE_NAME)

    def get_issue(self, issue_id: ResourceId) -> Dict:
        """
        Get details for a specific issue.
        
        Args:
            issue_id: Issue identifier
            
        Returns:
            Dict: Issue details
        """
        path = self._build_path(self.RESOURCE_NAME, str(issue_id))
        return self._get(path)


class AsyncIssueResource(BaseIssueResource, AsyncResource):
    """Asynchronous issue resource operations."""
    
    async def list_issues(self) -> List[Dict]:
        """
        List all issues.
        
        Returns:
            List[Dict]: List of issues
        """
        return await self._get(self.RESOURCE_NAME)

    async def get_issue(self, issue_id: ResourceId) -> Dict:
        """
        Get details for a specific issue.
        
        Args:
            issue_id: Issue identifier
            
        Returns:
            Dict: Issue details
        """
        path = self._build_path(self.RESOURCE_NAME, str(issue_id))
        return await self._get(path)


class SyncIssueCategoryResource(BaseIssueCategoryResource, SyncResource):
    """Synchronous issue category resource operations."""
    
    def list_issue_categories(self) -> List[Dict]:
        """
        List all issue categories.
        
        Returns:
            List[Dict]: List of issue categories
        """
        return self._get(self.RESOURCE_NAME)

    def get_issue_category(self, category_id: ResourceId) -> Dict:
        """
        Get details for a specific issue category.
        
        Args:
            category_id: Category identifier
            
        Returns:
            Dict: Category details
        """
        path = self._build_path(self.RESOURCE_NAME, str(category_id))
        return self._get(path)


class AsyncIssueCategoryResource(BaseIssueCategoryResource, AsyncResource):
    """Asynchronous issue category resource operations."""
    
    async def list_issue_categories(self) -> List[Dict]:
        """
        List all issue categories.
        
        Returns:
            List[Dict]: List of issue categories
        """
        return await self._get(self.RESOURCE_NAME)

    async def get_issue_category(self, category_id: ResourceId) -> Dict:
        """
        Get details for a specific issue category.
        
        Args:
            category_id: Category identifier
            
        Returns:
            Dict: Category details
        """
        path = self._build_path(self.RESOURCE_NAME, str(category_id))
        return await self._get(path)


class SyncVulnerabilityResource(BaseVulnerabilityResource, SyncResource):
    """Synchronous vulnerability resource operations."""
    
    def list_vulnerabilities(self) -> List[Dict]:
        """
        List all vulnerabilities.
        
        Returns:
            List[Dict]: List of vulnerabilities
        """
        return self._get(self.RESOURCE_NAME)

    def get_vulnerability(self, vulnerability_id: ResourceId) -> Dict:
        """
        Get details for a specific vulnerability.
        
        Args:
            vulnerability_id: Vulnerability identifier
            
        Returns:
            Dict: Vulnerability details
        """
        path = self._build_path(self.RESOURCE_NAME, str(vulnerability_id))
        return self._get(path)


class AsyncVulnerabilityResource(BaseVulnerabilityResource, AsyncResource):
    """Asynchronous vulnerability resource operations."""
    
    async def list_vulnerabilities(self) -> List[Dict]:
        """
        List all vulnerabilities.
        
        Returns:
            List[Dict]: List of vulnerabilities
        """
        return await self._get(self.RESOURCE_NAME)

    async def get_vulnerability(self, vulnerability_id: ResourceId) -> Dict:
        """
        Get details for a specific vulnerability.
        
        Args:
            vulnerability_id: Vulnerability identifier
            
        Returns:
            Dict: Vulnerability details
        """
        path = self._build_path(self.RESOURCE_NAME, str(vulnerability_id))
        return await self._get(path)
