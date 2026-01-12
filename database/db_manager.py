"""Database manager for ApplyMate."""

import asyncio
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, event
from loguru import logger

from database.models import Base, User, Profile, Application, ApplicationStatus
from config import settings


class DatabaseManager:
    """Manages database connections and initialization."""
    
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize database connection and create tables."""
        if self._initialized:
            return
        
        # Ensure database directory exists
        settings.ensure_directories()
        db_path = settings.get_database_path()
        
        # Create async engine
        database_url = f"sqlite+aiosqlite:///{db_path}"
        self.engine = create_async_engine(
            database_url,
            echo=settings.DEBUG,
            future=True
        )
        
        # Enable foreign keys for SQLite
        @event.listens_for(self.engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        
        # Create session maker
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Create default user if doesn't exist (for single-user mode)
        await self._ensure_default_user()
        
        self._initialized = True
        logger.info(f"Database initialized at {db_path}")
    
    async def _ensure_default_user(self):
        """Create default user for single-user mode."""
        async with self.get_session() as session:
            result = await session.execute(
                select(User).where(User.id == settings.CURRENT_USER_ID)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                user = User(
                    id=settings.CURRENT_USER_ID,
                    username="default_user",
                    email="user@applymate.local",
                    is_active=True
                )
                session.add(user)
                await session.commit()
                logger.info("Created default user for single-user mode")
    
    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """Get a database session context manager."""
        if not self._initialized:
            await self.initialize()
        
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()
    
    async def close(self):
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connections closed")


# Global database manager instance
db_manager = DatabaseManager()


# Convenience functions
async def get_session():
    """Get a database session (for dependency injection)."""
    async with db_manager.get_session() as session:
        yield session


async def init_db():
    """Initialize the database."""
    await db_manager.initialize()


async def close_db():
    """Close database connections."""
    await db_manager.close()


if __name__ == "__main__":
    """Run this to initialize the database manually."""
    async def main():
        logger.info("Initializing ApplyMate database...")
        await init_db()
        logger.info("Database initialization complete!")
    
    asyncio.run(main())
