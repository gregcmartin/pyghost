#!/usr/bin/env python3
"""
Script to list all endpoints from the Ghost Security API.
"""
import os
from dotenv import load_dotenv
from pyghost import GhostClient, EndpointFilters

# Load environment variables
load_dotenv()

# Get API configuration from environment
API_KEY = os.getenv("GHOST_API_KEY")
if not API_KEY:
    raise ValueError("GHOST_API_KEY environment variable is required")

def main():
    """List all endpoints."""
    # Initialize client
    client = GhostClient(api_key=API_KEY)
    
    # Create filters
    filters = EndpointFilters(size=100)  # Get 100 results per page
    
    # Get endpoints
    endpoints = client.endpoints.list_endpoints(filters)
    
    # Print results
    if isinstance(endpoints, dict) and 'items' in endpoints:
        print(f"\nTotal endpoints: {endpoints.get('total', 0)}")
        print(f"Page {endpoints.get('page', 1)} of {endpoints.get('pages', 1)}\n")
        
        for endpoint in endpoints['items']:
            print(f"ID: {endpoint.get('id')}")
            if 'name' in endpoint:
                print(f"Name: {endpoint['name']}")
            if 'created_at' in endpoint:
                print(f"Created: {endpoint['created_at']}")
            print()
    else:
        print("No endpoints found")

if __name__ == "__main__":
    main()
