"""
Common types and constants used across the Ghost Security API client.
"""
from typing import Dict, List, Optional, Union, Literal
from uuid import UUID

# Type aliases
ApiId = Union[str, UUID]
ResourceId = Union[str, UUID]
JsonData = Union[Dict, List]
QueryParams = Dict[str, any]

# Constants
DEFAULT_BIN_DURATION = "1h"

# Enums
class EndpointKind:
    HTML = "html"
    API = "api"
    SCRIPT = "script"
    UNKNOWN = "unknown"

class LastSeenPeriod:
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
