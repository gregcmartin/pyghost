#!/usr/bin/env python3
"""
Test script to verify all endpoints in the Ghost Security API client.
"""
import os
import sys
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from pyghost import GhostClient
from pyghost.types import (
    PaginationParams, OrderingParams, TimeRangeParams,
    EndpointKind, LastSeenPeriod, CampaignStatus
)

# Load environment variables
load_dotenv()

def get_time_range(days: int = 7) -> TimeRangeParams:
    """Get a time range for the last N days."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    return TimeRangeParams(start_date=start_date, end_date=end_date)

def test_apps(client: GhostClient) -> None:
    """Test app-related endpoints."""
    print("\nTesting App endpoints...")
    
    # List apps
    print("- Testing list_apps")
    apps = client.apps.list_apps(
        pagination=PaginationParams(page=1, size=10),
        ordering=OrderingParams(order_by="name")
    )
    print(f"  Found {len(apps.items)} apps")
    
    if apps.items:
        app_id = apps.items[0]['id']
        
        # Get app details
        print("- Testing get_app")
        app = client.apps.get_app(app_id)
        print(f"  Retrieved app: {app['name']}")
        
        # List app endpoints
        print("- Testing list_app_endpoints")
        endpoints = client.apps.list_app_endpoints(
            app_id,
            pagination=PaginationParams(page=1, size=10),
            kind=EndpointKind.API
        )
        print(f"  Found {len(endpoints.items)} endpoints")
        
        # List app assets
        print("- Testing list_app_assets")
        assets = client.apps.list_app_assets(
            app_id,
            pagination=PaginationParams(page=1, size=10)
        )
        print(f"  Found {len(assets.items)} assets")

def test_apis(client: GhostClient) -> None:
    """Test API-related endpoints."""
    print("\nTesting API endpoints...")
    
    # List APIs
    print("- Testing list_apis")
    time_range = get_time_range()
    apis = client.apis.list_apis(
        time_range=time_range,
        pagination=PaginationParams(page=1, size=10)
    )
    print(f"  Found {len(apis.items)} APIs")
    
    if apis.items:
        api_id = apis.items[0]['id']
        
        # Get API details
        print("- Testing get_api")
        api = client.apis.get_api(api_id, time_range=time_range)
        print(f"  Retrieved API for host: {api['host']['name']}")
        
        # List API endpoints
        print("- Testing list_api_endpoints")
        endpoints = client.apis.list_api_endpoints(
            api_id,
            pagination=PaginationParams(page=1, size=10)
        )
        print(f"  Found {len(endpoints.items)} endpoints")

def test_endpoints(client: GhostClient) -> None:
    """Test endpoint-related endpoints."""
    print("\nTesting Endpoint endpoints...")
    
    # List endpoints
    print("- Testing list_endpoints")
    endpoints = client.endpoints.list_endpoints(
        pagination=PaginationParams(page=1, size=10),
        ordering=OrderingParams(order_by="created_at"),
        last_seen=LastSeenPeriod.WEEK
    )
    print(f"  Found {len(endpoints.items)} endpoints")
    
    if endpoints.items:
        endpoint_id = endpoints.items[0]['id']
        
        # Get endpoint details
        print("- Testing get_endpoint")
        endpoint = client.endpoints.get_endpoint(endpoint_id)
        print(f"  Retrieved endpoint: {endpoint['path_template']}")
        
        # Get endpoint activity
        print("- Testing get_endpoint_activity")
        activity = client.endpoints.get_endpoint_activity(
            endpoint_id,
            time_range=get_time_range()
        )
        print("  Retrieved endpoint activity")
        
        # List endpoint apps
        print("- Testing list_endpoint_apps")
        apps = client.endpoints.list_endpoint_apps(
            endpoint_id,
            pagination=PaginationParams(page=1, size=10)
        )
        print(f"  Found {len(apps.items)} apps")
    
    # Get endpoints count
    print("- Testing get_endpoints_count")
    count = client.endpoints.get_endpoints_count()
    print(f"  Total endpoints: {count['count']}")

def test_campaigns(client: GhostClient) -> None:
    """Test campaign-related endpoints."""
    print("\nTesting Campaign endpoints...")
    
    # List campaigns
    print("- Testing list_campaigns")
    campaigns = client.campaigns.list_campaigns(
        pagination=PaginationParams(page=1, size=10),
        status=CampaignStatus.ACTIVE
    )
    print(f"  Found {len(campaigns.items)} campaigns")
    
    if campaigns.items:
        campaign_id = campaigns.items[0]['id']
        
        # Get campaign details
        print("- Testing get_campaign")
        campaign = client.campaigns.get_campaign(campaign_id)
        print(f"  Retrieved campaign: {campaign['name']}")
        
        # List campaign issue categories
        print("- Testing list_campaign_issue_categories")
        categories = client.campaigns.list_campaign_issue_categories(
            campaign_id,
            pagination=PaginationParams(page=1, size=10)
        )
        print(f"  Found {len(categories.items)} issue categories")
        
        # List campaign issues
        print("- Testing list_campaign_issues")
        issues = client.campaigns.list_campaign_issues(
            campaign_id,
            pagination=PaginationParams(page=1, size=10)
        )
        print(f"  Found {len(issues.items)} issues")
        
        # List campaign vulnerabilities
        print("- Testing list_campaign_vulnerabilities")
        vulnerabilities = client.campaigns.list_campaign_vulnerabilities(
            campaign_id,
            pagination=PaginationParams(page=1, size=10)
        )
        print(f"  Found {len(vulnerabilities.items)} vulnerabilities")

def test_infrastructure(client: GhostClient) -> None:
    """Test infrastructure-related endpoints."""
    print("\nTesting Infrastructure endpoints...")
    
    # List domains
    print("- Testing list_domains")
    domains = client.domains.list_domains(
        pagination=PaginationParams(page=1, size=10),
        ordering=OrderingParams(order_by="name")
    )
    print(f"  Found {len(domains.items)} domains")
    
    if domains.items:
        domain_id = domains.items[0]['id']
        
        # Get domain details
        print("- Testing get_domain")
        domain = client.domains.get_domain(domain_id)
        print(f"  Retrieved domain: {domain['name']}")
    
    # List hosts
    print("- Testing list_hosts")
    hosts = client.hosts.list_hosts(
        pagination=PaginationParams(page=1, size=10),
        ordering=OrderingParams(order_by="name")
    )
    print(f"  Found {len(hosts.items)} hosts")
    
    if hosts.items:
        host_id = hosts.items[0]['id']
        
        # Get host details
        print("- Testing get_host")
        host = client.hosts.get_host(host_id)
        print(f"  Retrieved host: {host['name']}")

def test_security(client: GhostClient) -> None:
    """Test security-related endpoints."""
    print("\nTesting Security endpoints...")
    
    # List issue categories
    print("- Testing list_issue_categories")
    categories = client.issue_categories.list_issue_categories(
        pagination=PaginationParams(page=1, size=10),
        ordering=OrderingParams(order_by="name")
    )
    print(f"  Found {len(categories.items)} issue categories")
    
    if categories.items:
        category_id = categories.items[0]['id']
        
        # Get issue category details
        print("- Testing get_issue_category")
        category = client.issue_categories.get_issue_category(category_id)
        print(f"  Retrieved category: {category['name']}")
    
    # List issues
    print("- Testing list_issues")
    issues = client.issues.list_issues(
        pagination=PaginationParams(page=1, size=10),
        ordering=OrderingParams(order_by="severity")
    )
    print(f"  Found {len(issues.items)} issues")
    
    if issues.items:
        issue_id = issues.items[0]['id']
        
        # Get issue details
        print("- Testing get_issue")
        issue = client.issues.get_issue(issue_id)
        print(f"  Retrieved issue: {issue['name']}")
    
    # List vulnerabilities
    print("- Testing list_vulnerabilities")
    vulnerabilities = client.vulnerabilities.list_vulnerabilities(
        pagination=PaginationParams(page=1, size=10),
        ordering=OrderingParams(order_by="issue.severity")
    )
    print(f"  Found {len(vulnerabilities.items)} vulnerabilities")
    
    if vulnerabilities.items:
        vulnerability_id = vulnerabilities.items[0]['id']
        
        # Get vulnerability details
        print("- Testing get_vulnerability")
        vulnerability = client.vulnerabilities.get_vulnerability(vulnerability_id)
        print(f"  Retrieved vulnerability for resource: {vulnerability['resource']['name']}")

def main():
    """Main test function."""
    # Check for API key
    api_key = os.getenv("GHOST_API_KEY")
    if not api_key:
        print("Error: GHOST_API_KEY environment variable not set")
        sys.exit(1)
    
    # Initialize client
    client = GhostClient(api_key=api_key)
    
    try:
        # Run tests
        test_apps(client)
        test_apis(client)
        test_endpoints(client)
        test_campaigns(client)
        test_infrastructure(client)
        test_security(client)
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
