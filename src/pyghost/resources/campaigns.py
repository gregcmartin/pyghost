"""
Campaign resources for the Ghost Security API.
"""
from typing import Dict, List

from ..types import ResourceId
from .base import SyncResource, AsyncResource


class BaseCampaignResource:
    """Base class for campaign-related operations."""
    
    RESOURCE_NAME = "campaigns"


class SyncCampaignResource(BaseCampaignResource, SyncResource):
    """Synchronous campaign resource operations."""
    
    def list_campaigns(self) -> List[Dict]:
        """
        List all campaigns.
        
        Returns:
            List[Dict]: List of campaigns
        """
        return self._get(self.RESOURCE_NAME)

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

    def get_campaign_issue_categories(self, campaign_id: ResourceId) -> List[Dict]:
        """
        Get issue categories for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List[Dict]: List of issue categories
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issue_categories")
        return self._get(path)

    def get_campaign_issues(self, campaign_id: ResourceId) -> List[Dict]:
        """
        Get issues for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List[Dict]: List of issues
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issues")
        return self._get(path)

    def get_campaign_vulnerabilities(self, campaign_id: ResourceId) -> List[Dict]:
        """
        Get vulnerabilities for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List[Dict]: List of vulnerabilities
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "vulnerabilities")
        return self._get(path)


class AsyncCampaignResource(BaseCampaignResource, AsyncResource):
    """Asynchronous campaign resource operations."""
    
    async def list_campaigns(self) -> List[Dict]:
        """
        List all campaigns.
        
        Returns:
            List[Dict]: List of campaigns
        """
        return await self._get(self.RESOURCE_NAME)

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

    async def get_campaign_issue_categories(self, campaign_id: ResourceId) -> List[Dict]:
        """
        Get issue categories for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List[Dict]: List of issue categories
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issue_categories")
        return await self._get(path)

    async def get_campaign_issues(self, campaign_id: ResourceId) -> List[Dict]:
        """
        Get issues for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List[Dict]: List of issues
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "issues")
        return await self._get(path)

    async def get_campaign_vulnerabilities(self, campaign_id: ResourceId) -> List[Dict]:
        """
        Get vulnerabilities for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List[Dict]: List of vulnerabilities
        """
        path = self._build_path(self.RESOURCE_NAME, str(campaign_id), "vulnerabilities")
        return await self._get(path)
