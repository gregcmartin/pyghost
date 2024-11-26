#!/usr/bin/env python3
"""
Script to find APIs associated with a specific app.
"""
import os
import sys
from dotenv import load_dotenv
from pyghost import GhostClient

# Load environment variables
load_dotenv()

# Get API configuration from environment
API_KEY = os.getenv("GHOST_API_KEY")
if not API_KEY:
    raise ValueError("GHOST_API_KEY environment variable is required")

def main():
    """Find APIs for a specific app."""
    if len(sys.argv) < 2:
        print("Usage: python find_app_apis.py <app_id>")
        sys.exit(1)
        
    app_id = sys.argv[1]
    
    # Initialize client
    client = GhostClient(api_key=API_KEY)
    
    try:
        # Get app details
        app = client.apps.get_app(app_id)
        print(f"\nApp: {app.get('name', app_id)}")
        
        # Get app endpoints
        endpoints = client.apps.get_app_endpoints(app_id)
        
        if isinstance(endpoints, dict) and 'items' in endpoints:
            print(f"\nTotal endpoints: {endpoints.get('total', 0)}")
            print(f"Page {endpoints.get('page', 1)} of {endpoints.get('pages', 1)}\n")
            
            for endpoint in endpoints['items']:
                print(f"ID: {endpoint.get('id')}")
                if 'path' in endpoint:
                    print(f"Path: {endpoint['path']}")
                if 'method' in endpoint:
                    print(f"Method: {endpoint['method']}")
                if 'created_at' in endpoint:
                    print(f"Created: {endpoint['created_at']}")
                print()
        else:
            print("No endpoints found")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
