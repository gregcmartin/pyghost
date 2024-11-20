"""
Simple test script for the Ghost Security API client.
"""
import json
from pyghost import GhostClient

def print_json(data):
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))

def test_api():
    """Test the Ghost Security API client with basic functionality."""
    
    # Initialize client with API key
    api_key = "REPLACE_WITH_GHOST_API_KEY"
    client = GhostClient(api_key=api_key)
    
    print("\n=== Testing Ghost Security API Client ===")

    # Test each endpoint
    try:
        print("\n1. Getting all endpoints:")
        print("---------------------------")
        endpoints = client.get_endpoints()
        print(f"Found {len(endpoints)} endpoints:")
        print_json(endpoints)
    except Exception as e:
        print(f"Error: {e}")

    try:
        print("\n2. Getting all apps:")
        print("--------------------")
        apps = client.get_apps()
        print(f"Found {len(apps)} apps:")
        print_json(apps)
    except Exception as e:
        print(f"Error: {e}")

    try:
        print("\n3. Getting app endpoints:")
        print("-------------------------")
        app_id = "302b505a-4ecb-4c16-9c46-f91f5ac57b1b"
        app_endpoints = client.get_app_endpoints(app_id)
        print(f"Found {len(app_endpoints)} endpoints for app {app_id}:")
        print_json(app_endpoints)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
