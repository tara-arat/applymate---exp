"""Input validation utilities."""

import re
from typing import Optional
from urllib.parse import urlparse


def is_valid_email(email: str) -> bool:
    """Validate email address format."""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    if not url:
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_valid_phone(phone: str) -> bool:
    """Validate phone number (basic validation)."""
    if not phone:
        return False
    
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check if it's mostly digits (allowing for country code +)
    return bool(re.match(r'^\+?\d{10,15}$', cleaned))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal."""
    # Remove any path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove or replace dangerous characters
    filename = re.sub(r'[^\w\s\-\.]', '_', filename)
    
    return filename


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_whitespace(text: str) -> str:
    """Clean excessive whitespace from text."""
    if not text:
        return ""
    
    # Replace multiple spaces/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
