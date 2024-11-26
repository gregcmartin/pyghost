#!/usr/bin/env python3
"""
Script to list all endpoints from the Ghost Security API.
"""
import os
import logging
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
from pyghost import GhostClient, EndpointFilters, GhostAPIError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Simplified format for cleaner output
)
logger = logging.getLogger(__name__)

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

def format_host(host: Dict) -> str:
    """Format host information in a readable way."""
    if not isinstance(host, dict):
        return str(host)
    
    parts = []
    if 'name' in host:
        parts.append(f"Name: {host['name']}")
    if 'created_at' in host:
        parts.append(f"Created: {format_timestamp(host['created_at'])}")
    if 'domain_id' in host:
        parts.append(f"Domain ID: {host['domain_id']}")
        
    return ', '.join(parts)

def print_endpoint(endpoint: Dict) -> None:
    """Print endpoint details in a formatted way."""
    print("\n" + "="*80)  # Section separator
    
    # Print basic information
    print(f"ID: {endpoint.get('id', 'Unknown')}")
    print(f"Method: {endpoint.get('method', 'Unknown')}")
    print(f"Kind: {endpoint.get('kind', 'Unknown')}")
    
    # Print host information
    if 'host' in endpoint:
        print(f"Host: {format_host(endpoint['host'])}")
        
    # Print additional details if available
    if 'path' in endpoint:
        print(f"Path: {endpoint['path']}")
    if 'format' in endpoint:
        print(f"Format: {endpoint['format']}")
        
    # Print request statistics
    if 'request_count' in endpoint:
        print(f"Request Count: {endpoint['request_count']}")
    if 'request_rate' in endpoint:
        print(f"Request Rate: {endpoint['request_rate']}")
        
    # Print timestamps
    if 'created_at' in endpoint:
        print(f"Created: {format_timestamp(endpoint['created_at'])}")
    if 'last_seen' in endpoint:
        print(f"Last Seen: {format_timestamp(endpoint['last_seen'])}")

def main():
    """List all endpoints."""
    try:
        # Initialize client
        client = GhostClient(api_key=API_KEY)
        
        # Create filters (get 100 results per page, sort by newest first)
        filters = EndpointFilters(
            size=100,
            order_by="-created_at"
        )
        
        # Get endpoints
        endpoints = client.endpoints.list_endpoints(filters)
        
        # Print summary
        if isinstance(endpoints, dict) and 'items' in endpoints:
            print(f"\nTotal Endpoints: {endpoints.get('total', 0)}")
            print(f"Page {endpoints.get('page', 1)} of {endpoints.get('pages', 1)}")
            print("\nEndpoint Details:")
            
            # Print each endpoint
            for endpoint in endpoints['items']:
                print_endpoint(endpoint)
        else:
            print("No endpoints found")
            
    except GhostAPIError as e:
        logger.error(f"API Error: {str(e)}")
        if e.response:
            logger.debug(f"Error response: {e.response}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
