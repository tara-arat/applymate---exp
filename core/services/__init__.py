"""Services package for ApplyMate."""

from core.services.profile_service import ProfileService, profile_service
from core.services.application_service import ApplicationService, application_service
from core.services.auth_service import AuthService, auth_service

__all__ = [
    "ProfileService",
    "profile_service",
    "ApplicationService",
    "application_service",
    "AuthService",
    "auth_service"
]
