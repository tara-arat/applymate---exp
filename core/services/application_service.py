"""Application service for managing job applications."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import select
from loguru import logger

from database import db_manager, Application, ApplicationStatus
from config import settings


class ApplicationService:
    """Service for managing job applications."""
    
    async def create_application(
        self,
        user_id: int,
        job_url: str,
        job_title: Optional[str] = None,
        company_name: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> Application:
        """Create a new application."""
        async with db_manager.get_session() as session:
            application = Application(
                user_id=user_id,
                job_url=job_url,
                job_title=job_title,
                company_name=company_name,
                job_description=job_description,
                status=ApplicationStatus.DRAFT
            )
            session.add(application)
            await session.commit()
            await session.refresh(application)
            
            logger.info(f"Created application {application.id} for user {user_id}")
            return application
    
    async def get_application(self, application_id: int) -> Optional[Application]:
        """Get application by ID."""
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(Application).where(Application.id == application_id)
            )
            return result.scalar_one_or_none()
    
    async def get_user_applications(
        self,
        user_id: int,
        status: Optional[ApplicationStatus] = None
    ) -> List[Application]:
        """Get all applications for a user, optionally filtered by status."""
        async with db_manager.get_session() as session:
            query = select(Application).where(Application.user_id == user_id)
            
            if status:
                query = query.where(Application.status == status)
            
            query = query.order_by(Application.created_at.desc())
            
            result = await session.execute(query)
            return list(result.scalars().all())
    
    async def update_application(
        self,
        application_id: int,
        **kwargs
    ) -> Optional[Application]:
        """Update application fields."""
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(Application).where(Application.id == application_id)
            )
            application = result.scalar_one_or_none()
            
            if not application:
                logger.warning(f"Application {application_id} not found")
                return None
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(application, key):
                    setattr(application, key, value)
            
            await session.commit()
            await session.refresh(application)
            
            logger.info(f"Updated application {application_id}")
            return application
    
    async def save_detected_fields(
        self,
        application_id: int,
        detected_fields: List[Dict[str, Any]]
    ) -> Optional[Application]:
        """Save detected form fields to application."""
        return await self.update_application(
            application_id,
            detected_fields=detected_fields
        )
    
    async def save_filled_data(
        self,
        application_id: int,
        filled_data: Dict[str, Any]
    ) -> Optional[Application]:
        """Save filled form data to application."""
        return await self.update_application(
            application_id,
            filled_data=filled_data
        )
    
    async def submit_application(
        self,
        application_id: int,
        notes: Optional[str] = None
    ) -> Optional[Application]:
        """Mark application as submitted."""
        return await self.update_application(
            application_id,
            status=ApplicationStatus.SUBMITTED,
            applied_at=datetime.utcnow(),
            notes=notes
        )
    
    async def skip_application(
        self,
        application_id: int,
        notes: Optional[str] = None
    ) -> Optional[Application]:
        """Mark application as skipped."""
        return await self.update_application(
            application_id,
            status=ApplicationStatus.SKIPPED,
            notes=notes
        )
    
    async def delete_application(self, application_id: int) -> bool:
        """Delete an application."""
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(Application).where(Application.id == application_id)
            )
            application = result.scalar_one_or_none()
            
            if not application:
                return False
            
            await session.delete(application)
            await session.commit()
            
            logger.info(f"Deleted application {application_id}")
            return True
    
    async def get_application_stats(self, user_id: int) -> Dict[str, int]:
        """Get application statistics for a user."""
        applications = await self.get_user_applications(user_id)
        
        stats = {
            'total': len(applications),
            'draft': 0,
            'submitted': 0,
            'skipped': 0
        }
        
        for app in applications:
            if app.status == ApplicationStatus.DRAFT:
                stats['draft'] += 1
            elif app.status == ApplicationStatus.SUBMITTED:
                stats['submitted'] += 1
            elif app.status == ApplicationStatus.SKIPPED:
                stats['skipped'] += 1
        
        return stats


# Global application service instance
application_service = ApplicationService()
