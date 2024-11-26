# PyGhost

Python based API client for the Ghost Security Platform

## Installation

```bash
pip install -e .
```

## Usage

```python
from pyghost import GhostClient

# Initialize the client with your API key
client = GhostClient(api_key="your_api_key")

# Get all endpoints
endpoints = client.list_endpoints()

# Get all apps
apps = client.list_apps()

# Get endpoints for a specific app
app_endpoints = client.get_app_endpoints("app-id")
```

## API Methods

The client provides comprehensive access to the Ghost Security Platform API:

### APIs
- `list_apis()`: List all APIs
- `get_api(api_id)`: Get details for a specific API
- `get_api_endpoints(api_id)`: Get endpoints for a specific API

### Apps
- `list_apps()`: List all applications
- `get_app(app_id)`: Get details for a specific app
- `get_app_endpoints(app_id)`: Get endpoints for a specific app
- `get_app_assets(app_id)`: Get assets for a specific app

### Campaigns
- `list_campaigns()`: List all campaigns
- `get_campaign(campaign_id)`: Get details for a specific campaign
- `get_campaign_issue_categories(campaign_id)`: Get issue categories for a campaign
- `get_campaign_issues(campaign_id)`: Get issues for a campaign
- `get_campaign_vulnerabilities(campaign_id)`: Get vulnerabilities for a campaign

### Domains
- `list_domains()`: List all domains
- `get_domain(domain_id)`: Get details for a specific domain

### Endpoints
- `list_endpoints(filters=None)`: List all endpoints with optional filtering
- `get_endpoint_count(filters=None)`: Get count of endpoints matching filters
- `get_endpoint(endpoint_id)`: Get details for a specific endpoint
- `get_endpoint_activity(endpoint_id)`: Get endpoint request volume activity
- `get_endpoint_apps(endpoint_id)`: Get apps associated with an endpoint

### Hosts
- `list_hosts()`: List all hosts
- `get_host(host_id)`: Get details for a specific host

### Issue Categories
- `list_issue_categories()`: List all issue categories
- `get_issue_category(category_id)`: Get details for a specific issue category

### Issues
- `list_issues()`: List all issues
- `get_issue(issue_id)`: Get details for a specific issue

### Vulnerabilities
- `list_vulnerabilities()`: List all vulnerabilities
- `get_vulnerability(vulnerability_id)`: Get details for a specific vulnerability

## Endpoint Filtering

The `list_endpoints()` method accepts an optional `EndpointFilters` object for filtering results:

```python
from pyghost import GhostClient, EndpointFilters

client = GhostClient(api_key="your_api_key")

# Create filters
filters = EndpointFilters(
    size=25,                    # Results per page
    page=1,                     # Page number
    order_by="-created_at",     # Order by field (prefix with - for descending)
    format="REST",              # Filter by endpoint format
    method=["GET", "POST"],     # Filter by HTTP methods
    last_seen="week",          # Filter by last seen period
    search="api",              # Search path template and host
    min_request_count=100,     # Minimum number of requests
    host_id=["host-id"],       # Filter by host IDs
    is_first_party=True,       # Filter first party endpoints
    kind="api",                # Filter by endpoint kind
    port=[443],               # Filter by ports
    min_request_rate=10       # Minimum request rate over last 30 days
)

# Get filtered endpoints
endpoints = client.list_endpoints(filters=filters)
```

## Response Structure

### Endpoints Response
```python
{
    "items": [
        {
            "id": "endpoint-id",
            "created_at": "timestamp",
            "port": 443,
            "path_template": "/api/path",
            "method": "GET",
            "format": "REST",
            "is_first_party": true,
            "kinds": ["api"],
            "host": {
                "id": "host-id",
                "name": "hostname"
            },
            "traffic_summary": {
                "request_count": 1000,
                "average_requests_per_hour": 100
            }
        }
    ],
    "page": 1,
    "pages": 1,
    "size": 25,
    "total": 100
}
```

### Apps Response
```python
{
    "items": [
        {
            "id": "app-id",
            "name": "app-name",
            "is_public": true,
            "created_at": "timestamp",
            "updated_at": "timestamp",
            "host": {
                "id": "host-id",
                "name": "hostname"
            },
            "screenshot_url": "url",
            "endpoint_counts": {
                "api": {
                    "total": 10,
                    "first_party": 8,
                    "third_party": 2
                }
            }
        }
    ],
    "page": 1,
    "pages": 1,
    "size": 25,
    "total": 100
}
```

## Error Handling

The client includes error handling through the `GhostAPIError` exception class, which provides:
- Error message
- HTTP status code
- API response details (when available)

## License

MIT License
