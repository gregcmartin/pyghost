"""
Endpoint resources for the Ghost Security API.
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta

from ..types import ResourceId, EndpointKind, LastSeenPeriod
from .base import SyncResource, AsyncResource


def format_rfc3339(dt: datetime) -> str:
    """Format datetime to RFC3339 format."""
    return dt.isoformat() + "Z"


def get_default_time_range(hours: int = 24) -> tuple[str, str]:
    """
    Get default time range for activity queries.
    
    Args:
        hours: Number of hours to look back
        
    Returns:
        tuple: (start_date, end_date) in RFC3339 format
    """
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    return format_rfc3339(start), format_rfc3339(end)

[Rest of the file remains the same]
