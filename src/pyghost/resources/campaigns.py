"""
Campaign resources for the Ghost Security API.
"""
from typing import Dict, List, Optional
from datetime import datetime

from ..types import (
    ResourceId, PaginationParams, OrderingParams, FilterParams,
    CampaignStatus, IssueSeverity
)
from .base import SyncResource, AsyncResource, PaginatedResponse


class BaseCampaignResource:
    """Base class for campaign-related operations."""
    
    RESOURCE_NAME = "campaigns"

    def _prepare_issue_category_filters(
        self,
        name: Optional[str] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> FilterParams:
        """
        Prepare issue category filters.
        
        Args:
            name: Filter by category name
            has_active_vulnerabilities: Filter for categories with active vulnerabilities
            issue_severities: Filter by issue severities
            issue_ids: Filter by issue IDs
            category_ids: Filter by category IDs
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            name=name,
            **{"vulnerabilities.has_active": has_active_vulnerabilities} if has_active_vulnerabilities is not None else {},
            **{"issue.severity": issue_severities} if issue_severities else {},
            **{"issue.id": issue_ids} if issue_ids else {},
            **{"id": category_ids} if category_ids else {}
        )

    def _prepare_issue_filters(
        self,
        category_ids: Optional[List[str]] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        name: Optional[str] = None,
        severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None
    ) -> FilterParams:
        """
        Prepare issue filters.
        
        Args:
            category_ids: Filter by category IDs
            has_active_vulnerabilities: Filter for issues with active vulnerabilities
            name: Filter by issue name
            severities: Filter by severities
            issue_ids: Filter by issue IDs
            
        Returns:
            FilterParams: Prepared filters
        """
        return FilterParams(
            **{"category.id": category_ids} if category_ids else {},
            **{"vulnerabilities.has_active": has_active_vulnerabilities} if has_active_vulnerabilities is not None else {},
            name=name,
            severity=severities,
            id=issue_ids
        )

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


class SyncCampaignResource(BaseCampaignResource, SyncResource):
    """Synchronous campaign resource operations."""
    
    def list_campaigns(
        self,
        pagination: Optional[PaginationParams] = None,
        status: Optional[str] = None
    ) -> PaginatedResponse:
        """
        List all campaigns.
        
        Args:
            pagination: Pagination parameters
            status: Filter by campaign status
            
        Returns:
            PaginatedResponse: Paginated list of campaigns
        """
        filters = FilterParams(status=status)
        params = self._prepare_params(pagination, filters=filters)
        return PaginatedResponse(self._get(self.RESOURCE_NAME, params=params))

    def get_campaign(self, campaign_id: ResourceId) -> Dict:
        """
        Get details for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Dict: Campaign details
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id))
        return self._get(path)

    def list_campaign_issue_categories(
        self,
        campaign_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """
        List issue categories for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            pagination: Pagination parameters
            ordering: Ordering parameters
            name: Filter by category name
            has_active_vulnerabilities: Filter for categories with active vulnerabilities
            issue_severities: Filter by issue severities
            issue_ids: Filter by issue IDs
            category_ids: Filter by category IDs
            
        Returns:
            PaginatedResponse: Paginated list of issue categories
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issue_categories")
        filters = self._prepare_issue_category_filters(
            name, has_active_vulnerabilities, issue_severities,
            issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(path, params=params))

    def list_campaign_issues(
        self,
        campaign_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        category_ids: Optional[List[str]] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        name: Optional[str] = None,
        severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """
        List issues for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            pagination: Pagination parameters
            ordering: Ordering parameters
            category_ids: Filter by category IDs
            has_active_vulnerabilities: Filter for issues with active vulnerabilities
            name: Filter by issue name
            severities: Filter by severities
            issue_ids: Filter by issue IDs
            
        Returns:
            PaginatedResponse: Paginated list of issues
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issues")
        filters = self._prepare_issue_filters(
            category_ids, has_active_vulnerabilities,
            name, severities, issue_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(path, params=params))

    def list_campaign_vulnerabilities(
        self,
        campaign_id: ResourceId,
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
        """
        List vulnerabilities for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            pagination: Pagination parameters
            ordering: Ordering parameters
            statuses: Filter by vulnerability statuses
            first_detected_at: Filter by first detection period
            last_detected_at: Filter by last detection period
            resource_kinds: Filter by resource kinds
            issue_severities: Filter by issue severities
            issue_ids: Filter by issue IDs
            category_ids: Filter by category IDs
            
        Returns:
            PaginatedResponse: Paginated list of vulnerabilities
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "vulnerabilities")
        filters = self._prepare_vulnerability_filters(
            statuses, first_detected_at, last_detected_at,
            resource_kinds, issue_severities, issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        return PaginatedResponse(self._get(path, params=params))


class AsyncCampaignResource(BaseCampaignResource, AsyncResource):
    """Asynchronous campaign resource operations."""
    
    async def list_campaigns(
        self,
        pagination: Optional[PaginationParams] = None,
        status: Optional[str] = None
    ) -> PaginatedResponse:
        """
        List all campaigns.
        
        Args:
            pagination: Pagination parameters
            status: Filter by campaign status
            
        Returns:
            PaginatedResponse: Paginated list of campaigns
        """
        filters = FilterParams(status=status)
        params = self._prepare_params(pagination, filters=filters)
        response = await self._get(self.RESOURCE_NAME, params=params)
        return PaginatedResponse(response)

    async def get_campaign(self, campaign_id: ResourceId) -> Dict:
        """
        Get details for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Dict: Campaign details
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id))
        return await self._get(path)

    async def list_campaign_issue_categories(
        self,
        campaign_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        name: Optional[str] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        issue_severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None,
        category_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """
        List issue categories for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            pagination: Pagination parameters
            ordering: Ordering parameters
            name: Filter by category name
            has_active_vulnerabilities: Filter for categories with active vulnerabilities
            issue_severities: Filter by issue severities
            issue_ids: Filter by issue IDs
            category_ids: Filter by category IDs
            
        Returns:
            PaginatedResponse: Paginated list of issue categories
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issue_categories")
        filters = self._prepare_issue_category_filters(
            name, has_active_vulnerabilities, issue_severities,
            issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(path, params=params)
        return PaginatedResponse(response)

    async def list_campaign_issues(
        self,
        campaign_id: ResourceId,
        pagination: Optional[PaginationParams] = None,
        ordering: Optional[OrderingParams] = None,
        category_ids: Optional[List[str]] = None,
        has_active_vulnerabilities: Optional[bool] = None,
        name: Optional[str] = None,
        severities: Optional[List[str]] = None,
        issue_ids: Optional[List[str]] = None
    ) -> PaginatedResponse:
        """
        List issues for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            pagination: Pagination parameters
            ordering: Ordering parameters
            category_ids: Filter by category IDs
            has_active_vulnerabilities: Filter for issues with active vulnerabilities
            name: Filter by issue name
            severities: Filter by severities
            issue_ids: Filter by issue IDs
            
        Returns:
            PaginatedResponse: Paginated list of issues
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issues")
        filters = self._prepare_issue_filters(
            category_ids, has_active_vulnerabilities,
            name, severities, issue_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(path, params=params)
        return PaginatedResponse(response)

    async def list_campaign_vulnerabilities(
        self,
        campaign_id: ResourceId,
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
        """
        List vulnerabilities for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            pagination: Pagination parameters
            ordering: Ordering parameters
            statuses: Filter by vulnerability statuses
            first_detected_at: Filter by first detection period
            last_detected_at: Filter by last detection period
            resource_kinds: Filter by resource kinds
            issue_severities: Filter by issue severities
            issue_ids: Filter by issue IDs
            category_ids: Filter by category IDs
            
        Returns:
            PaginatedResponse: Paginated list of vulnerabilities
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "vulnerabilities")
        filters = self._prepare_vulnerability_filters(
            statuses, first_detected_at, last_detected_at,
            resource_kinds, issue_severities, issue_ids, category_ids
        )
        params = self._prepare_params(pagination, ordering, filters=filters)
        response = await self._get(path, params=params)
        return PaginatedResponse(response)
