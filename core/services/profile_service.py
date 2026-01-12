"""Profile service for managing user profiles."""

from typing import Optional, Dict, Any
from pathlib import Path
from sqlalchemy import select
from loguru import logger

from database import db_manager, Profile
from config import settings


class ProfileService:
    """Service for managing user profiles."""
    
    async def get_profile(self, user_id: int) -> Optional[Profile]:
        """Get profile for a user."""
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(Profile).where(Profile.user_id == user_id)
            )
            return result.scalar_one_or_none()
    
    async def create_profile(self, user_id: int, profile_data: Dict[str, Any]) -> Profile:
        """Create a new profile for a user."""
        async with db_manager.get_session() as session:
            # Check if profile already exists
            existing = await self.get_profile(user_id)
            if existing:
                logger.warning(f"Profile already exists for user {user_id}")
                return existing
            
            profile = Profile(user_id=user_id, **profile_data)
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
            
            logger.info(f"Created profile for user {user_id}")
            return profile
    
    async def update_profile(
        self,
        user_id: int,
        profile_data: Dict[str, Any]
    ) -> Optional[Profile]:
        """Update an existing profile."""
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(Profile).where(Profile.user_id == user_id)
            )
            profile = result.scalar_one_or_none()
            
            if not profile:
                logger.warning(f"Profile not found for user {user_id}")
                return None
            
            # Update fields
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            await session.commit()
            await session.refresh(profile)
            
            logger.info(f"Updated profile for user {user_id}")
            return profile
    
    async def save_resume(
        self,
        user_id: int,
        resume_filename: str,
        resume_content: bytes
    ) -> Optional[str]:
        """Save a resume file and update profile."""
        try:
            # Ensure uploads directory exists
            uploads_dir = settings.get_uploads_dir() / str(user_id)
            uploads_dir.mkdir(parents=True, exist_ok=True)
            
            # Save file
            resume_path = uploads_dir / resume_filename
            with open(resume_path, 'wb') as f:
                f.write(resume_content)
            
            # Update profile
            await self.update_profile(
                user_id,
                {
                    'resume_filename': resume_filename,
                    'resume_path': str(resume_path)
                }
            )
            
            logger.info(f"Saved resume for user {user_id}: {resume_filename}")
            return str(resume_path)
        
        except Exception as e:
            logger.error(f"Error saving resume: {e}")
            return None
    
    def profile_to_dict(self, profile: Profile) -> Dict[str, Any]:
        """Convert profile to dictionary for form filling."""
        if not profile:
            return {}
        
        return {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone': profile.phone,
            'address_line1': profile.address_line1,
            'address_line2': profile.address_line2,
            'city': profile.city,
            'state': profile.state,
            'zip_code': profile.zip_code,
            'country': profile.country,
            'linkedin_url': profile.linkedin_url,
            'github_url': profile.github_url,
            'portfolio_url': profile.portfolio_url,
            'current_company': profile.current_company,
            'current_title': profile.current_title,
            'years_of_experience': profile.years_of_experience,
            'education_level': profile.education_level,
            'university': profile.university,
            'major': profile.major,
            'graduation_year': profile.graduation_year,
            'gpa': profile.gpa,
            **(profile.custom_fields or {})
        }


# Global profile service instance
profile_service = ProfileService()
