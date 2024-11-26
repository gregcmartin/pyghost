#!/usr/bin/env python3
"""
Script to list all apps and their endpoints.
"""
import argparse
from pprint import pprint
from typing import Optional, List

from pyghost import GhostClient
from pyghost.client import EndpointFilters

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="List all apps and their endpoints")
    parser.add_argument("api_key", help="Ghost Security API key")
    parser.add_argument("--count", action="store_true", help="Show only the count of endpoints")
    parser.add_argument("--page", type=int, help="Specific page to fetch (default: all pages)")
    
    # Add filter options
    parser.add_argument("--size", type=int, help="Results per page")
    parser.add_argument("--order-by", help="Order results by field (prefix with - for descending)")
    parser.add_argument("--format", help="Filter by endpoint format (e.g., REST)")
    parser.add_argument("--method", nargs="+", help="Filter by HTTP methods (e.g., GET POST)")
    parser.add_argument("--last-seen", choices=['day', 'week', 'month', 'year'], 
                       help="Filter by last seen period")
    parser.add_argument("--search", help="Search path template and host")
    parser.add_argument("--min-request-count", type=int, 
                       help="Minimum number of requests")
    parser.add_argument("--host-id", nargs="+", help="Filter by host IDs")
    parser.add_argument("--first-party", action="store_true", 
                       help="Filter first party endpoints")
    parser.add_argument("--kind", choices=['html', 'api', 'script', 'unknown'],
                       help="Filter by endpoint kind")
    parser.add_argument("--port", type=int, nargs="+", help="Filter by ports")
    parser.add_argument("--min-request-rate", type=int,
                       help="Minimum request rate over last 30 days")
    
    return parser

def create_filters(args) -> Optional[EndpointFilters]:
    """Create EndpointFilters from command line arguments."""
    if not any([args.size, args.order_by, args.format,
                args.method, args.last_seen, args.search,
                args.min_request_count, args.host_id, args.first_party,
                args.kind, args.port, args.min_request_rate]):
        return None
        
    return EndpointFilters(
        size=args.size,
        page=None,  # Handle pagination separately
        order_by=args.order_by,
        format=args.format,
        method=args.method,
        last_seen=args.last_seen,
        search=args.search,
        min_request_count=args.min_request_count,
        host_id=args.host_id,
        is_first_party=args.first_party,
        kind=args.kind,
        port=args.port,
        min_request_rate=args.min_request_rate
    )

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    client = GhostClient(api_key=args.api_key)
    filters = create_filters(args)
    
    try:
        # First get all apps
        print("Fetching apps...")
        current_page = args.page if args.page else 1
        total_pages = 1
        all_apps = []
        
        while current_page <= total_pages:
            print(f"Fetching page {current_page}...")
            response = client.get("apps", params={'page': current_page})
            
            if not response or 'items' not in response:
                print("No apps found.")
                return 0
                
            apps = response['items']
            total_pages = response.get('pages', 1)
            
            print(f"\nFound {len(apps)} apps on page {current_page} of {total_pages}:")
            for app in apps:
                print(f"\nApp: {app.get('name', 'Unknown')} (ID: {app.get('id', 'Unknown')})")
                print("Endpoint counts:")
                endpoint_counts = app.get('endpoint_counts', {})
                for type_name, counts in endpoint_counts.items():
                    print(f"  {type_name}:")
                    for count_type, count in counts.items():
                        print(f"    {count_type}: {count}")
            
            all_apps.extend(apps)
            
            if args.page:  # If specific page requested, don't fetch more
                break
                
            current_page += 1
        
        # Then get endpoints for each app
        print(f"\nFetching endpoints for {len(all_apps)} apps...")
        total_endpoints = 0
        
        for app in all_apps:
            app_id = app.get('id')
            if not app_id:
                print("\nSkipping app with no ID")
                continue
                
            app_name = app.get('name', app_id)
            print(f"\nFetching endpoints for app: {app_name}")
            
            try:
                endpoints = client.get_app_endpoints(app_id)
                if endpoints:
                    if isinstance(endpoints, dict) and 'items' in endpoints:
                        endpoint_list = endpoints['items']
                        endpoint_count = len(endpoint_list)
                    elif isinstance(endpoints, list):
                        endpoint_list = endpoints
                        endpoint_count = len(endpoints)
                    else:
                        endpoint_list = [endpoints]
                        endpoint_count = 1
                        
                    print(f"Found {endpoint_count} endpoints")
                    if not args.count:
                        print("Endpoint details:")
                        pprint(endpoint_list)
                    total_endpoints += endpoint_count
                else:
                    print("No endpoints found for this app")
            except Exception as e:
                print(f"Error fetching endpoints for app {app_name}: {str(e)}")
                continue
        
        print(f"\nTotal endpoints found across all fetched apps: {total_endpoints}")
        if args.page and args.page < total_pages:
            print(f"Note: There are more apps on pages {args.page + 1} to {total_pages}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    main()
