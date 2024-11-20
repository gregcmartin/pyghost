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
endpoints = client.get_endpoints()
# Returns a list of endpoints with details like:
# - id
# - path_template
# - method
# - format
# - host information
# - traffic summary
# - endpoint kinds

# Get all apps
apps = client.get_apps()
# Returns a list of apps with details like:
# - id
# - name
# - is_public
# - created_at/updated_at
# - host information
# - screenshot_url
# - endpoint counts by type

# Get endpoints for a specific app
app_endpoints = client.get_app_endpoints("app-id")
# Returns a list of endpoints for the specified app with details like:
# - endpoint information
# - last scanned timestamp
# - endpoint configuration
# - host details

```

## API Methods

The client provides three main methods:

- `get_endpoints()`: Get all endpoints in the Ghost Security Platform
- `get_apps()`: Get all applications being monitored
- `get_app_endpoints(app_id)`: Get detailed endpoint information for a specific app

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
                "name": "hostname",
                # ... host details
            },
            "traffic_summary": {
                "request_count": 1000,
                "average_requests_per_hour": 100,
                # ... traffic statistics
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
                "name": "hostname",
                # ... host details
            },
            "screenshot_url": "url",
            "endpoint_counts": {
                "api": {
                    "total": 10,
                    "first_party": 8,
                    "third_party": 2
                },
                # ... counts for other endpoint types
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
