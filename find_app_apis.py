#!/usr/bin/env python3
"""
Script to find APIs associated with a specific app.
"""
import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
from pyghost import GhostClient, GhostAPIError

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

def print_app_details(app: Dict) -> None:
    """Print app details in a formatted way."""
    print("\nApp Details:")
    print("="*80)
    print(f"ID: {app.get('id', 'Unknown')}")
    print(f"Name: {app.get('name', 'Unknown')}")
    if 'created_at' in app:
        print(f"Created: {format_timestamp(app['created_at'])}")
    if 'updated_at' in app:
        print(f"Updated: {format_timestamp(app['updated_at'])}")
    if 'endpoint_counts' in app:
        counts = app['endpoint_counts']
        print("\nEndpoint Counts:")
        for kind, data in counts.items():
            print(f"  {kind.upper()}:")
            print(f"    Total: {data['total']}")
            print(f"    First Party: {data['first_party']}")
            print(f"    Third Party: {data['third_party']}")

def print_endpoint(endpoint_data: Dict) -> None:
    """Print endpoint details in a formatted way."""
    print("\n" + "-"*80)  # Section separator
    
    # Extract endpoint from wrapper
    endpoint = endpoint_data.get('endpoint', {})
    if not endpoint:
        return
    
    # Print basic information
    print(f"ID: {endpoint.get('id', 'Unknown')}")
    print(f"Method: {endpoint.get('method', 'Unknown')}")
    print(f"Kind: {endpoint.get('kind', 'Unknown')}")
    
    # Print path if available
    if 'path_template' in endpoint:
        print(f"Path: {endpoint['path_template']}")
        
    # Print host information
    if 'host' in endpoint and isinstance(endpoint['host'], dict):
        host = endpoint['host']
        print(f"Host: {host.get('name', 'Unknown')}")
        if 'created_at' in host:
            print(f"Host Created: {format_timestamp(host['created_at'])}")
        
    # Print format and other details
    if 'format' in endpoint:
        print(f"Format: {endpoint['format']}")
    if 'is_first_party' in endpoint:
        print(f"First Party: {endpoint['is_first_party']}")
        
    # Print timestamps
    if 'created_at' in endpoint:
        print(f"Created: {format_timestamp(endpoint['created_at'])}")
    if 'last_scanned_at' in endpoint_data:
        print(f"Last Scanned: {format_timestamp(endpoint_data['last_scanned_at'])}")

def main():
    """Find APIs for a specific app."""
    if len(sys.argv) < 2:
        print("Usage: python find_app_apis.py <app_id>")
        sys.exit(1)
        
    app_id = sys.argv[1]
    
    try:
        # Initialize client
        client = GhostClient(api_key=API_KEY)
        
        try:
            # Get app details
            app = client.apps.get_app(app_id)
            print_app_details(app)
            
            # Get app endpoints
            endpoints = client.apps.get_app_endpoints(app_id)
            
            # Print endpoints
            if isinstance(endpoints, dict) and 'items' in endpoints:
                print(f"\nEndpoints ({endpoints.get('total', 0)} total):")
                print("="*80)
                
                for endpoint_data in endpoints['items']:
                    print_endpoint(endpoint_data)
            else:
                print("\nNo endpoints found")
                
        except GhostAPIError as e:
            logger.error(f"API Error: {str(e)}")
            if e.response:
                logger.debug(f"Error response: {e.response}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
