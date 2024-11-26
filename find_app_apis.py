#!/usr/bin/env python3
"""
Script to fetch app details and find related APIs by hostname.
"""
import argparse
import sys
from pyghost import GhostClient, GhostAPIError

def get_app_details(client, app_id):
    """Fetch details for a specific app."""
    try:
        response = client.get(f"apps/{app_id}")
        if isinstance(response, dict):
            return response
        print(f"Error: Unexpected response format when fetching app {app_id}")
        return None
    except GhostAPIError as e:
        print(f"Error fetching app details: {e}")
        return None

def find_related_apis(client, hostname):
    """Find all APIs that contain the given hostname."""
    related_apis = []
    try:
        # Get all endpoints
        endpoints = client.get_endpoints()
        
        # Filter endpoints that match the hostname
        for endpoint in endpoints:
            if isinstance(endpoint, str):
                if hostname.lower() in endpoint.lower():
                    related_apis.append({"url": endpoint})
            elif isinstance(endpoint, dict):
                if hostname.lower() in endpoint.get('url', '').lower():
                    related_apis.append(endpoint)
                
        return related_apis
    except GhostAPIError as e:
        print(f"Error fetching endpoints: {e}")
        return []

def print_app_info(app):
    """Print basic app information."""
    print("\nApp Details:")
    print(f"Name: {app['name']}")
    print(f"ID: {app['id']}")
    host = app['host']
    print(f"Hostname: {host['name']}")

def print_related_apis(apis):
    """Print information about related APIs."""
    if not apis:
        print("\nNo related APIs found.")
        return
        
    print(f"\nFound {len(apis)} related APIs:")
    for api in apis:
        print("\n---")
        if isinstance(api, dict):
            print(f"URL: {api.get('url', 'N/A')}")
            print(f"Method: {api.get('method', 'N/A')}")
            print(f"First Seen: {api.get('first_seen_at', 'N/A')}")
            print(f"Last Seen: {api.get('last_seen_at', 'N/A')}")
        else:
            print(f"URL: {api}")

def main():
    parser = argparse.ArgumentParser(description="Find app details and related APIs by hostname")
    parser.add_argument("app_id", help="ID of the app to analyze")
    parser.add_argument("api_key", help="Ghost Security API key")
    
    args = parser.parse_args()
    
    # Initialize the client
    client = GhostClient(api_key=args.api_key)
    
    # Get app details
    app = get_app_details(client, args.app_id)
    if not app:
        sys.exit(1)
    
    # Print app information
    print_app_info(app)
    
    # Get hostname and find related APIs
    hostname = app['host']['name']
    related_apis = find_related_apis(client, hostname)
    
    # Print results
    print_related_apis(related_apis)

if __name__ == "__main__":
    main()
