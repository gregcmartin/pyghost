# PyGhost

Python based API client for the Ghost Security Platform

## Installation

```bash
pip install -e .
```

## Features

- Full support for all Ghost Security Platform API v2 endpoints
- Both synchronous and asynchronous clients
- Resource-based API organization
- Type hints and comprehensive documentation
- Robust error handling
- Modular and extensible design

## Usage

### Synchronous Usage

```python
from pyghost import GhostClient, EndpointFilters, EndpointKind

# Initialize the client
client = GhostClient(api_key="your_api_key")

# Access different API resources
apps = client.apps.list_apps()
endpoints = client.endpoints.list_endpoints()
campaigns = client.campaigns.list_campaigns()

# Use filters for endpoints
filters = EndpointFilters(
    size=25,
    kind=EndpointKind.API,
    is_first_party=True,
    method=["GET", "POST"]
)
filtered_endpoints = client.endpoints.list_endpoints(filters)

# Get specific resources
app = client.apps.get_app("app-id")
app_endpoints = client.apps.get_app_endpoints("app-id")
app_assets = client.apps.get_app_assets("app-id")
```

### Asynchronous Usage

```python
import asyncio
from pyghost import AsyncGhostClient, EndpointFilters

async def main():
    # Use async context manager to handle session lifecycle
    async with AsyncGhostClient(api_key="your_api_key") as client:
        # Access different API resources
        apps = await client.apps.list_apps()
        endpoints = await client.endpoints.list_endpoints()
        
        # Run multiple requests concurrently
        apps, endpoints = await asyncio.gather(
            client.apps.list_apps(),
            client.endpoints.list_endpoints()
        )

# Run the async code
asyncio.run(main())
```

## API Resources

The client provides access to all Ghost Security Platform resources:

### APIs
- `client.apis.list_apis()`
- `client.apis.get_api(api_id)`
- `client.apis.get_api_endpoints(api_id)`

### Apps
- `client.apps.list_apps()`
- `client.apps.get_app(app_id)`
- `client.apps.get_app_endpoints(app_id)`
- `client.apps.get_app_assets(app_id)`

### Campaigns
- `client.campaigns.list_campaigns()`
- `client.campaigns.get_campaign(campaign_id)`
- `client.campaigns.get_campaign_issue_categories(campaign_id)`
- `client.campaigns.get_campaign_issues(campaign_id)`
- `client.campaigns.get_campaign_vulnerabilities(campaign_id)`

### Domains
- `client.domains.list_domains()`
- `client.domains.get_domain(domain_id)`

### Endpoints
- `client.endpoints.list_endpoints(filters=None)`
- `client.endpoints.get_endpoint_count(filters=None)`
- `client.endpoints.get_endpoint(endpoint_id)`
- `client.endpoints.get_endpoint_activity(endpoint_id)`
- `client.endpoints.get_endpoint_apps(endpoint_id)`

### Hosts
- `client.hosts.list_hosts()`
- `client.hosts.get_host(host_id)`

### Issue Categories
- `client.issue_categories.list_issue_categories()`
- `client.issue_categories.get_issue_category(category_id)`

### Issues
- `client.issues.list_issues()`
- `client.issues.get_issue(issue_id)`

### Vulnerabilities
- `client.vulnerabilities.list_vulnerabilities()`
- `client.vulnerabilities.get_vulnerability(vulnerability_id)`

## Endpoint Filtering

The `EndpointFilters` class provides a clean interface for filtering endpoints:

```python
from pyghost import EndpointFilters, EndpointKind, LastSeenPeriod

filters = EndpointFilters(
    size=25,                    # Results per page
    page=1,                     # Page number
    order_by="-created_at",     # Order by field (prefix with - for descending)
    format="REST",              # Filter by endpoint format
    method=["GET", "POST"],     # Filter by HTTP methods
    last_seen=LastSeenPeriod.WEEK,  # Filter by last seen period
    search="api",              # Search path template and host
    min_request_count=100,     # Minimum number of requests
    host_id=["host-id"],       # Filter by host IDs
    is_first_party=True,       # Filter first party endpoints
    kind=EndpointKind.API,     # Filter by endpoint kind
    port=[443],               # Filter by ports
    min_request_rate=10       # Minimum request rate over last 30 days
)

endpoints = client.endpoints.list_endpoints(filters=filters)
```

## Error Handling

The client provides detailed error handling through specific exception classes:

```python
from pyghost import (
    GhostAPIError,
    ClientNotInitializedError,
    ValidationError,
    AuthenticationError,
    ResourceNotFoundError
)

try:
    endpoints = client.endpoints.list_endpoints()
except AuthenticationError:
    print("Invalid API key")
except ValidationError:
    print("Invalid request parameters")
except ResourceNotFoundError:
    print("Resource not found")
except GhostAPIError as e:
    print(f"API error: {e.message}")
    print(f"Status code: {e.status_code}")
    print(f"Response: {e.response}")
```

## License

MIT License
