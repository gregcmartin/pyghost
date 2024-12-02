# PyGhost 👻

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
from pyghost import (
    GhostClient,
    PaginationParams,
    OrderingParams,
    TimeRangeParams,
    FilterParams
)
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize client
client = GhostClient(api_key=os.getenv("GHOST_API_KEY"))

# List apps with pagination and ordering
apps = client.apps.list_apps(
    pagination=PaginationParams(page=1, size=10),
    ordering=OrderingParams(order_by="name")
)

# Get app details and endpoints
app = client.apps.get_app("app-id")
endpoints = client.apps.list_app_endpoints(
    "app-id",
    pagination=PaginationParams(page=1, size=10),
    is_first_party=True
)

# Get API traffic data
time_range = TimeRangeParams(
    start_date=datetime.now(timezone.utc).replace(hour=0, minute=0),
    end_date=datetime.now(timezone.utc),
    bin_duration="1h"
)
apis = client.apis.list_apis(time_range=time_range)
```

### Async Usage

```python
import asyncio
from pyghost import AsyncGhostClient, PaginationParams

async def main():
    async with AsyncGhostClient(api_key=os.getenv("GHOST_API_KEY")) as client:
        # List apps with pagination
        apps = await client.apps.list_apps(
            pagination=PaginationParams(page=1, size=10)
        )
        
        # Get app details
        app = await client.apps.get_app("app-id")

asyncio.run(main())
```

### Advanced Filtering

```python
from pyghost import EndpointKind, LastSeenPeriod

# List endpoints with multiple filters
endpoints = client.endpoints.list_endpoints(
    pagination=PaginationParams(page=1, size=25),
    ordering=OrderingParams(order_by="created_at"),
    methods=["GET", "POST"],
    is_first_party=True,
    kind=EndpointKind.API,
    last_seen=LastSeenPeriod.WEEK,
    min_request_count=100
)

# List vulnerabilities with filters
vulnerabilities = client.vulnerabilities.list_vulnerabilities(
    pagination=PaginationParams(page=1, size=10),
    ordering=OrderingParams(order_by="issue.severity"),
    statuses=["active"],
    first_detected_at=LastSeenPeriod.MONTH,
    issue_severities=["critical", "high"]
)
```

## Available Resources

### Apps and APIs
- Apps: List apps, get details, list endpoints and assets
- APIs: List APIs with traffic data, get details, list endpoints

### Endpoints and Infrastructure
- Endpoints: List endpoints, get details, activity data, and associated apps
- Domains: List domains and get domain details
- Hosts: List hosts and get host details

### Security Features
- Campaigns: Manage security campaigns and track progress
- Issue Categories: Organize and manage security issue categories
- Issues: Track security issues and their status
- Vulnerabilities: Monitor and manage security vulnerabilities

### Common Features Across Resources
- Pagination support with customizable page size
- Flexible ordering options
- Advanced filtering capabilities
- Time-based data retrieval
- First-party vs third-party filtering

## Error Handling

```python
from pyghost import (
    GhostAPIError,
    ConnectionError,
    RetryError,
    TimeoutError,
    ValidationError,
    AuthenticationError,
    ResourceNotFoundError
)

try:
    endpoints = client.endpoints.list_endpoints()
except ConnectionError as e:
    print(f"Connection failed: {e}")
except RetryError as e:
    print(f"Max retries exceeded: {e}")
except TimeoutError as e:
    print(f"Request timed out: {e}")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ResourceNotFoundError as e:
    print(f"Resource not found: {e}")
except GhostAPIError as e:
    print(f"API error: {e}")
    if e.response:
        print(f"Response: {e.response}")
```

## Development

### Running Tests

The test suite verifies all API endpoints and features:

```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run tests
python test_all_endpoints.py
```

### Key Test Areas
- Resource CRUD operations
- Pagination and ordering
- Filtering capabilities
- Time series data retrieval
- Error handling
- Both sync and async implementations

## License

MIT License
