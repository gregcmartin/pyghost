#!/usr/bin/env python3
"""
Comprehensive test script for both synchronous and asynchronous Ghost Security API clients.
Tests all available endpoints and prints results.
"""
import asyncio
import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

from pyghost import (
    GhostClient,
    AsyncGhostClient,
    EndpointFilters,
    GhostAPIError,
    ConnectionError,
    RetryError,
    TimeoutError
)
from pyghost.resources.endpoints import format_rfc3339

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set debug logging for HTTP client
http_logger = logging.getLogger('pyghost.http')
http_logger.setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()

# Get API configuration from environment
API_KEY = os.getenv("GHOST_API_KEY")
if not API_KEY:
    raise ValueError("GHOST_API_KEY environment variable is required")

def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp string to a more readable format."""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return timestamp_str

def print_section(title: str) -> None:
    """Print a section header."""
    logger.info("\n" + "="*80)
    logger.info(f" {title} ".center(80, "="))
    logger.info("="*80)

def print_result(name: str, result: Any) -> None:
    """Print the result of an API call."""
    logger.info(f"\n--- {name} ---")
    if isinstance(result, (list, dict)):
        if isinstance(result, dict) and 'items' in result:
            logger.info(f"Total items: {result.get('total', len(result['items']))}")
            logger.info(f"Page {result.get('page', 1)} of {result.get('pages', 1)}")
            for item in result['items'][:3]:  # Show first 3 items
                logger.info(f"\nItem ID: {item.get('id')}")
                if 'name' in item:
                    logger.info(f"Name: {item['name']}")
                if 'created_at' in item:
                    logger.info(f"Created: {format_timestamp(item['created_at'])}")
        else:
            logger.info(f"Count: {len(result) if isinstance(result, list) else 1}")
    else:
        logger.info(result)

async def test_async_client():
    """Test all AsyncGhostClient endpoints."""
    print_section("Testing Async Client")
    
    try:
        async with AsyncGhostClient(api_key=API_KEY) as client:
            # Test Apps
            print_section("Testing App Endpoints")
            try:
                apps = await client.apps.list_apps()
                print_result("List Apps", apps)
                
                if isinstance(apps, dict) and 'items' in apps and apps['items']:
                    app_id = apps['items'][0]['id']
                    app = await client.apps.get_app(app_id)
                    print_result(f"Get App {app_id}", app)
                    
                    app_endpoints = await client.apps.get_app_endpoints(app_id)
                    print_result(f"Get App Endpoints for {app_id}", app_endpoints)
            except GhostAPIError as e:
                logger.error(f"API Error in Apps section: {str(e)}")
                if e.response:
                    logger.debug(f"Error response: {e.response}")

            # Test Endpoints
            print_section("Testing Endpoint Endpoints")
            try:
                filters = EndpointFilters(size=10, page=1)
                endpoints = await client.endpoints.list_endpoints(filters)
                print_result("List Endpoints", endpoints)
                
                count = await client.endpoints.get_endpoint_count(filters)
                print_result("Get Endpoint Count", count)
                
                if isinstance(endpoints, dict) and 'items' in endpoints and endpoints['items']:
                    endpoint_id = endpoints['items'][0]['id']
                    endpoint = await client.endpoints.get_endpoint(endpoint_id)
                    print_result(f"Get Endpoint {endpoint_id}", endpoint)
                    
                    # Get activity for the last 24 hours
                    end = datetime.now(timezone.utc)
                    start = end - timedelta(hours=24)
                    activity = await client.endpoints.get_endpoint_activity(
                        endpoint_id,
                        bin_duration="1h",
                        start_date=format_rfc3339(start),
                        end_date=format_rfc3339(end)
                    )
                    print_result(f"Get Endpoint Activity for {endpoint_id}", activity)
                    
                    endpoint_apps = await client.endpoints.get_endpoint_apps(endpoint_id)
                    print_result(f"Get Endpoint Apps for {endpoint_id}", endpoint_apps)
            except GhostAPIError as e:
                logger.error(f"API Error in Endpoints section: {str(e)}")
                if e.response:
                    logger.debug(f"Error response: {e.response}")

            # Test Domains
            print_section("Testing Domain Endpoints")
            try:
                domains = await client.domains.list_domains()
                print_result("List Domains", domains)
                
                if isinstance(domains, dict) and 'items' in domains and domains['items']:
                    domain_id = domains['items'][0]['id']
                    domain = await client.domains.get_domain(domain_id)
                    print_result(f"Get Domain {domain_id}", domain)
            except GhostAPIError as e:
                logger.error(f"API Error in Domains section: {str(e)}")
                if e.response:
                    logger.debug(f"Error response: {e.response}")

    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
    except RetryError as e:
        logger.error(f"Retry error: {str(e)}")
    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in async client: {str(e)}")

def test_sync_client():
    """Test all GhostClient endpoints."""
    print_section("Testing Sync Client")
    client = GhostClient(api_key=API_KEY)
    
    try:
        # Test Apps
        print_section("Testing App Endpoints")
        try:
            apps = client.apps.list_apps()
            print_result("List Apps", apps)
            
            if isinstance(apps, dict) and 'items' in apps and apps['items']:
                app_id = apps['items'][0]['id']
                app = client.apps.get_app(app_id)
                print_result(f"Get App {app_id}", app)
                
                app_endpoints = client.apps.get_app_endpoints(app_id)
                print_result(f"Get App Endpoints for {app_id}", app_endpoints)
        except GhostAPIError as e:
            logger.error(f"API Error in Apps section: {str(e)}")
            if e.response:
                logger.debug(f"Error response: {e.response}")

        # Test Endpoints
        print_section("Testing Endpoint Endpoints")
        try:
            filters = EndpointFilters(size=10, page=1)
            endpoints = client.endpoints.list_endpoints(filters)
            print_result("List Endpoints", endpoints)
            
            count = client.endpoints.get_endpoint_count(filters)
            print_result("Get Endpoint Count", count)
            
            if isinstance(endpoints, dict) and 'items' in endpoints and endpoints['items']:
                endpoint_id = endpoints['items'][0]['id']
                endpoint = client.endpoints.get_endpoint(endpoint_id)
                print_result(f"Get Endpoint {endpoint_id}", endpoint)
                
                # Get activity for the last 24 hours
                end = datetime.now(timezone.utc)
                start = end - timedelta(hours=24)
                activity = client.endpoints.get_endpoint_activity(
                    endpoint_id,
                    bin_duration="1h",
                    start_date=format_rfc3339(start),
                    end_date=format_rfc3339(end)
                )
                print_result(f"Get Endpoint Activity for {endpoint_id}", activity)
                
                endpoint_apps = client.endpoints.get_endpoint_apps(endpoint_id)
                print_result(f"Get Endpoint Apps for {endpoint_id}", endpoint_apps)
        except GhostAPIError as e:
            logger.error(f"API Error in Endpoints section: {str(e)}")
            if e.response:
                logger.debug(f"Error response: {e.response}")

        # Test Domains
        print_section("Testing Domain Endpoints")
        try:
            domains = client.domains.list_domains()
            print_result("List Domains", domains)
            
            if isinstance(domains, dict) and 'items' in domains and domains['items']:
                domain_id = domains['items'][0]['id']
                domain = client.domains.get_domain(domain_id)
                print_result(f"Get Domain {domain_id}", domain)
        except GhostAPIError as e:
            logger.error(f"API Error in Domains section: {str(e)}")
            if e.response:
                logger.debug(f"Error response: {e.response}")

    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in sync client: {str(e)}")

def main():
    """Run both sync and async tests."""
    logger.info("\nTesting Synchronous Client...")
    test_sync_client()
    
    logger.info("\nTesting Asynchronous Client...")
    asyncio.run(test_async_client())

if __name__ == "__main__":
    main()
