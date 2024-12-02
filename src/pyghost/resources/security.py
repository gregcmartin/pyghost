"""
Security resources for the Ghost Security API.
"""
from typing import Dict, List, Optional
from datetime import datetime

from ..types import (
    ResourceId, PaginationParams, OrderingParams, FilterParams,
    IssueSeverity, LastSeenPeriod
)
from .base import SyncResource, AsyncResource, PaginatedResponse


class BaseIssueCategoryResource:
    """Base class for issue category operations."""
    
    RESOURCE_NAME = "issue_categories"

    def _prepare_category_filters(
        self,
        name: Optional[str] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        active_vulnerabilities_gte: Optional[int] = None,
        resolved_vulnerabilities_gte: Optional[int] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> FilterParams:
        """
        Prepare issue category filters.
        
        Args:
            name: Filter by name (partial match)
            has_active_vulnerabilities: Filter for categories with active vulnerabilities
            active_vulnerabilities_gte: Filter by minimum active vulnerabilities
            resolved_vulnerabilities_gte: Filter by minimum resolved vulnerabilities
            issue_severities: Filter by issue severities
            issue_ids: Filter by issue IDs
            category_ids: Filter by category IDs
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            name=name,
            **{"vulnerabilities.has_active": has_active_vulnerabilities} if has_active_vulnerabilities is not None else {},
            **{"vulnerabilities.active_gte": active_vulnerabilities_gte} if active_vulnerabilities_gte is not None else {},
            **{"vulnerabilities.resolved_gte": resolved_vulnerabilities_gte} if resolved_vulnerabilities_gte is not None else {},
            **{"issue.severity": issue_severities} if issue_severities else {},
            **{"issue.id": issue_ids} if issue_ids else {},
            id=category_ids
        )


class BaseIssueResource:
    """Base class for issue operations."""
    
    RESOURCE_NAME = "issues"

    def _prepare_issue_filters(
        self,
        category_ids: Optional[List[str]] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        active_vulnerabilities_gte: Optional[int] = None,
        resolved_vulnerabilities_gte: Optional[int] = None,
        name: Optional[str] = None,
        severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None
    ) -> FilterParams:
        """
        Prepare issue filters.
        
        Args:
            category_ids: Filter by category IDs
            has_active_vulnerabilities: Filter for issues with active vulnerabilities
            active_vulnerabilities_gte: Filter by minimum active vulnerabilities
            resolved_vulnerabilities_gte: Filter by minimum resolved vulnerabilities
            name: Filter by name (partial match)
            severities: Filter by severities
            issue_ids: Filter by issue IDs
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            **{"category.id": category_ids} if category_ids else {},
            **{"vulnerabilities.has_active": has_active_vulnerabilities} if has_active_vulnerabilities is not None else {},
            **{"vulnerabilities.active_gte": active_vulnerabilities_gte} if active_vulnerabilities_gte is not None else {},
            **{"vulnerabilities.resolved_gte": resolved_vulnerabilities_gte} if resolved_vulnerabilities_gte is not None else {},
            name=name,
            severity=severities,
            id=issue_ids
        )


class BaseVulnerabilityResource:
    """Base class for vulnerability operations."""
    
    RESOURCE_NAME = "vulnerabilities"

    def _prepare_vulnerability_filters(
        self,
        statuses: Optional[List[str]] = None,
        first_detected_at: Optional[str] = None,
        last_detected_at: Optional[str] = None,
        resource_kinds: Optional[List[str]] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> FilterParams:
        """
        Prepare vulnerability filters.
        
        Args:
            statuses: Filter by vulnerability statuses
            first_detected_at: Filter by first detection period
            last_detected_at: Filter by last detection period
            resource_kinds: Filter by resource kinds
            issue_severities: Filter by issue severities
            issue_ids: Filter by issue IDs
            category_ids: Filter by category IDs
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            status=statuses,
            first_detected_at=first_detected_at,
            last_detected_at=last_detected_at,
            **{"resource.kind": resource_kinds} if resource_kinds else {},
            **{"issue.severity": issue_severities} if issue_severities else {},
            **{"issue.id": issue_ids} if issue_ids else {},
            **{"issue.category.id": category_ids} if category_ids else {}
        )


class SyncIssueCategoryResource(BaseIssueCategoryResource, SyncResource):
    """Synchronous issue category operations."""
    
    def list_issue_categories(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        active_vulnerabilities_gte: Optional[int] = None,
        resolved_vulnerabilities_gte: Optional[int] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """List issue categories with filtering."""
        filters = self._prepare_category_filters(
            name, has_active_vulnerabilities,
            active_vulnerabilities_gte, resolved_vulnerabilities_gte,
            issue_severities, issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_issue_category(self, category_id: ResourceId) -> Dict:
        """Get a specific issue category."""
        path = self._build_path(self.RESOURCE_NAME, str(category_id))
        return self._get(path)

    def create_issue_category(
        self,
        name: str,
        description: str,
        best_practices: str,
        executive_summary: str,
        icon: Optional[Dict[str, str]] = None
    ) -> Dict:
        """Create a new issue category."""
        data = {
            "name": name,
            "description": description,
            "best_practices": best_practices,
            "executive_summary": executive_summary,
            "icon": icon
        }
        return self._post(self.RESOURCE_NAME, data=data)


class SyncIssueResource(BaseIssueResource, SyncResource):
    """Synchronous issue operations."""
    
    def list_issues(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        category_ids: Optional[List[str]] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        active_vulnerabilities_gte: Optional[int] = None,
        resolved_vulnerabilities_gte: Optional[int] = None,
        name: Optional[str] = None,
        severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """List issues with filtering."""
        filters = self._prepare_issue_filters(
            category_ids, has_active_vulnerabilities,
            active_vulnerabilities_gte, resolved_vulnerabilities_gte,
            name, severities, issue_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_issue(self, issue_id: ResourceId) -> Dict:
        """Get a specific issue."""
        path = self._build_path(self.RESOURCE_NAME, str(issue_id))
        return self._get(path)


class SyncVulnerabilityResource(BaseVulnerabilityResource, SyncResource):
    """Synchronous vulnerability operations."""
    
    def list_vulnerabilities(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        statuses: Optional[List[str]] = None,
        first_detected_at: Optional[str] = None,
        last_detected_at: Optional[str] = None,
        resource_kinds: Optional[List[str]] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """List vulnerabilities with filtering."""
        filters = self._prepare_vulnerability_filters(
            statuses, first_detected_at, last_detected_at,
            resource_kinds, issue_severities, issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_vulnerability(self, vulnerability_id: ResourceId) -> Dict:
        """Get a specific vulnerability."""
        path = self._build_path(self.RESOURCE_NAME, str(vulnerability_id))
        return self._get(path)

    def create_vulnerability(
        self,
        issue_id: ResourceId,
        resource_id: ResourceId,
        demo_data: Optional[str] = None
    ) -> Dict:
        """Create or update a vulnerability."""
        data = {
            "issue_id": str(issue_id),
            "resource_id": str(resource_id),
            "demo_data": demo_data
        }
        return self._post(self.RESOURCE_NAME, data=data)


class AsyncIssueCategoryResource(BaseIssueCategoryResource, AsyncResource):
    """Asynchronous issue category operations."""
    
    async def list_issue_categories(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        active_vulnerabilities_gte: Optional[int] = None,
        resolved_vulnerabilities_gte: Optional[int] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """List issue categories with filtering."""
        filters = self._prepare_category_filters(
            name, has_active_vulnerabilities,
            active_vulnerabilities_gte, resolved_vulnerabilities_gte,
            issue_severities, issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_issue_category(self, category_id: ResourceId) -> Dict:
        """Get a specific issue category."""
        path = self._build_path(self.RESOURCE_NAME, str(category_id))
        return await self._get(path)

    async def create_issue_category(
        self,
        name: str,
        description: str,
        best_practices: str,
        executive_summary: str,
        icon: Optional[Dict[str, str]] = None
    ) -> Dict:
        """Create a new issue category."""
        data = {
            "name": name,
            "description": description,
            "best_practices": best_practices,
            "executive_summary": executive_summary,
            "icon": icon
        }
        return await self._post(self.RESOURCE_NAME, data=data)


class AsyncIssueResource(BaseIssueResource, AsyncResource):
    """Asynchronous issue operations."""
    
    async def list_issues(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        category_ids: Optional[List[str]] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        active_vulnerabilities_gte: Optional[int] = None,
        resolved_vulnerabilities_gte: Optional[int] = None,
        name: Optional[str] = None,
        severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """List issues with filtering."""
        filters = self._prepare_issue_filters(
            category_ids, has_active_vulnerabilities,
            active_vulnerabilities_gte, resolved_vulnerabilities_gte,
            name, severities, issue_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_issue(self, issue_id: ResourceId) -> Dict:
        """Get a specific issue."""
        path = self._build_path(self.RESOURCE_NAME, str(issue_id))
        return await self._get(path)


class AsyncVulnerabilityResource(BaseVulnerabilityResource, AsyncResource):
    """Asynchronous vulnerability operations."""
    
    async def list_vulnerabilities(
        self,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        statuses: Optional[List[str]] = None,
        first_detected_at: Optional[str] = None,
        last_detected_at: Optional[str] = None,
        resource_kinds: Optional[List[str]] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """List vulnerabilities with filtering."""
        filters = self._prepare_vulnerability_filters(
            statuses, first_detected_at, last_detected_at,
            resource_kinds, issue_severities, issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_vulnerability(self, vulnerability_id: ResourceId) -> Dict:
        """Get a specific vulnerability."""
        path = self._build_path(self.RESOURCE_NAME, str(vulnerability_id))
        return await self._get(path)

    async def create_vulnerability(
        self,
        issue_id: ResourceId,
        resource_id: ResourceId,
        demo_data: Optional[str] = None
    ) -> Dict:
        """Create or update a vulnerability."""
        data = {
            "issue_id": str(issue_id),
            "resource_id": str(resource_id),
            "demo_data": demo_data
        }
        return await self._post(self.RESOURCE_NAME, data=data)
