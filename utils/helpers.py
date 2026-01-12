"""Helper utilities for ApplyMate."""

from typing import Any, Dict, Optional
from datetime import datetime
import json


def format_datetime(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M") -> str:
    """Format datetime object to string."""
    if not dt:
        return "N/A"
    return dt.strftime(format_str)


def format_date(dt: Optional[datetime], format_str: str = "%Y-%m-%d") -> str:
    """Format datetime object to date string."""
    if not dt:
        return "N/A"
    return dt.strftime(format_str)


def safe_json_loads(json_str: Optional[str], default: Any = None) -> Any:
    """Safely parse JSON string."""
    if not json_str:
        return default
    
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: Any = "{}") -> str:
    """Safely serialize object to JSON string."""
    try:
        return json.dumps(obj, indent=2)
    except (TypeError, ValueError):
        return default


def format_phone_display(phone: Optional[str]) -> str:
    """Format phone number for display."""
    if not phone:
        return ""
    
    # Simple formatting: (XXX) XXX-XXXX
    import re
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone


def get_status_emoji(status: str) -> str:
    """Get emoji for application status."""
    emoji_map = {
        'draft': '📝',
        'submitted': '✅',
        'skipped': '⏭️'
    }
    return emoji_map.get(status.lower(), '❓')


def get_status_color(status: str) -> str:
    """Get color for application status."""
    color_map = {
        'draft': 'blue',
        'submitted': 'green',
        'skipped': 'gray'
    }
    return color_map.get(status.lower(), 'black')
