# PyGhost

Python client for the Ghost Security Platform API

## Installation

```bash
pip install -e .
```

## Configuration

Configuration is handled through environment variables. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Required:
- `GHOST_API_KEY`: Your Ghost Security API key

Optional:
- `GHOST_API_URL`: API URL (defaults to https://api.dev.ghostsecurity.com)
- `GHOST_REQUEST_TIMEOUT`: Request timeout in seconds (default: 30)
- `GHOST_MAX_RETRIES`: Maximum retry attempts (default: 3)
- `GHOST_RETRY_DELAY`: Delay between retries in seconds (default: 1)

## Usage

### Basic Usage

```python
from pyghost import GhostClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize client
client = GhostClient(api_key=os.getenv("GHOST_API_KEY"))

# List apps
apps = client.apps.list_apps()

# Get app details and endpoints
app = client.apps.get_app("app-id")
endpoints = client.apps.get_app_endpoints("app-id")
```

### Async Usage

```python
import asyncio
from pyghost import AsyncGhostClient

async def main():
    async with AsyncGhostClient(api_key=os.getenv("GHOST_API_KEY")) as client:
        # List apps
        apps = await client.apps.list_apps()
        
        # Get app details
        app = await client.apps.get_app("app-id")

asyncio.run(main())
```

### Endpoint Filtering

```python
from pyghost import EndpointFilters

# Create filters
filters = EndpointFilters(
    size=25,                    # Results per page
    method=["GET", "POST"],     # HTTP methods
    is_first_party=True,        # First party endpoints only
    min_request_count=100       # Minimum request count
)

# Get filtered endpoints
endpoints = client.endpoints.list_endpoints(filters=filters)
```

## Utility Scripts

### List Endpoints

List all endpoints with details:

```bash
python list_endpoints.py
```

### Find App APIs

Find APIs associated with a specific app:

```bash
python find_app_apis.py <app_id>
```

## Error Handling

```python
from pyghost import (
    GhostAPIError,
    ConnectionError,
    RetryError,
    TimeoutError
)

try:
    endpoints = client.endpoints.list_endpoints()
except ConnectionError as e:
    print(f"Connection failed: {e}")
except RetryError as e:
    print(f"Max retries exceeded: {e}")
except TimeoutError as e:
    print(f"Request timed out: {e}")
except GhostAPIError as e:
    print(f"API error: {e}")
    if e.response:
        print(f"Response: {e.response}")
```

## Available Resources

- Apps: List apps and get app details/endpoints
- Endpoints: List endpoints, get counts and activity
- Domains: List domains and get domain details
- APIs: List APIs and get API details
- Campaigns: List campaigns and get campaign details
- Issues: List issues and get issue details
- Vulnerabilities: List vulnerabilities and get details

## Development

Run the test suite:

```bash
python test_all_endpoints.py
```

## License

MIT License
