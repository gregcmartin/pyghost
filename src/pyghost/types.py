"""
Common types and constants used across the Ghost Security API client.
"""
from typing import Dict, List, Optional, Union, Literal
from uuid import UUID
from datetime import datetime

# Type aliases
ApiId = Union[str, UUID]
ResourceId = Union[str, UUID]
JsonData = Union[Dict, List]
QueryParams = Dict[str, any]

# Constants
DEFAULT_BIN_DURATION = "1h"

# Enums
class EndpointKind:
    """Endpoint types"""
    HTML = "html"
    API = "api"
    SCRIPT = "script"
    UNKNOWN = "unknown"

class LastSeenPeriod:
    """Time periods for last seen filters"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

class VulnerabilityStatus:
    """Vulnerability statuses"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

class IssueSeverity:
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ResourceKind:
    """Resource types"""
    HOST = "host"
    ENDPOINT = "endpoint"
    APP = "app"
    API = "api"
    DOMAIN = "domain"

class CampaignStatus:
    """Campaign statuses"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Common Models
class TimeSeries:
    """Time series data structure"""
    def __init__(self, bins: List[Dict[str, Union[int, str]]]):
        self.bins = bins

class EndpointCount:
    """Endpoint count structure"""
    def __init__(self, first_party: int, third_party: int, total: int):
        self.first_party = first_party
        self.third_party = third_party
        self.total = total

class EndpointCounts:
    """Endpoint counts by type"""
    def __init__(self, api: EndpointCount, html: EndpointCount, 
                 script: EndpointCount, unknown: EndpointCount):
        self.api = api
        self.html = html
        self.script = script
        self.unknown = unknown

class VulnerabilityCount:
    """Vulnerability count structure"""
    def __init__(self, active: int, resolved: int, suppressed: int):
        self.active = active
        self.resolved = resolved
        self.suppressed = suppressed

class PaginationParams:
    """Common pagination parameters"""
    def __init__(self, page: Optional[int] = None, size: Optional[int] = None):
        self.page = page
        self.size = size

class OrderingParams:
    """Common ordering parameters"""
    def __init__(self, order_by: Optional[str] = None):
        self.order_by = order_by

class TimeRangeParams:
    """Common time range parameters"""
    def __init__(self, start_date: datetime, end_date: datetime, 
                 bin_duration: str = DEFAULT_BIN_DURATION):
        self.start_date = start_date
        self.end_date = end_date
        self.bin_duration = bin_duration

class FilterParams:
    """Common filter parameters"""
    def __init__(self, **kwargs):
        self.filters = {k: v for k, v in kwargs.items() if v is not None}
