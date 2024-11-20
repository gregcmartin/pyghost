# PyGhost

A simple Python client for the Ghost Security Platform API.

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

# Get all apps
apps = client.get_apps()

# Get endpoints for a specific app
app_endpoints = client.get_app_endpoints("your-app-id")
```

## API Methods

The client provides three main methods:

- `get_endpoints()`: Get all endpoints
- `get_apps()`: Get all apps
- `get_app_endpoints(app_id)`: Get endpoints for a specific app

## Testing

Run the test script to verify the API client:

```bash
python test_ghost.py
```

## Error Handling

The client includes error handling through the `GhostAPIError` exception class, which provides:
- Error message
- HTTP status code
- API response details (when available)

## License

MIT License
