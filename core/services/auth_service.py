"""Authentication service for future multi-user support."""

from typing import Optional
from sqlalchemy import select
from loguru import logger

from database import db_manager, User
from config import settings


class AuthService:
    """Service for user authentication.
    
    Note: This is a placeholder for future multi-user support.
    Currently returns the default single user.
    """
    
    async def get_current_user(self) -> Optional[User]:
        """Get the current user (single-user mode)."""
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(User).where(User.id == settings.CURRENT_USER_ID)
            )
            return result.scalar_one_or_none()
    
    async def create_user(
        self,
        username: str,
        email: str,
        password: Optional[str] = None
    ) -> User:
        """Create a new user (for future multi-user support)."""
        async with db_manager.get_session() as session:
            user = User(
                username=username,
                email=email,
                password_hash=None,  # Will hash password in v0.2
                is_active=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            logger.info(f"Created user: {username}")
            return user
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user (placeholder for v0.2)."""
        # TODO: Implement proper authentication
        logger.warning("Authentication not yet implemented")
        return await self.get_current_user()
    
    def hash_password(self, password: str) -> str:
        """Hash a password (placeholder for v0.2)."""
        # TODO: Implement using bcrypt or similar
        raise NotImplementedError("Password hashing not yet implemented")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password (placeholder for v0.2)."""
        # TODO: Implement password verification
        raise NotImplementedError("Password verification not yet implemented")


# Global auth service instance
auth_service = AuthService()
