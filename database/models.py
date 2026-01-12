"""Database models for ApplyMate."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, 
    Boolean, Float, JSON, Enum as SQLEnum, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ApplicationStatus(str, Enum):
    """Status of a job application."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    SKIPPED = "skipped"


class User(Base):
    """User model for future multi-user support."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Null for single-user mode
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Profile(Base):
    """User profile containing personal information for auto-fill."""
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Personal Information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    
    # Address
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Professional
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)
    current_company = Column(String(200), nullable=True)
    current_title = Column(String(200), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    
    # Education
    education_level = Column(String(100), nullable=True)  # e.g., "Bachelor's", "Master's"
    university = Column(String(200), nullable=True)
    major = Column(String(200), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    gpa = Column(Float, nullable=True)
    
    # Additional fields as JSON for flexibility
    custom_fields = Column(JSON, nullable=True)
    
    # Resume storage
    resume_filename = Column(String(255), nullable=True)
    resume_path = Column(String(500), nullable=True)
    resume_parsed_data = Column(JSON, nullable=True)  # Parsed resume content
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="profiles")
    
    # Ensure one active profile per user
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_profile"),)
    
    def __repr__(self):
        return f"<Profile(id={self.id}, user_id={self.user_id}, name='{self.first_name} {self.last_name}')>"


class Application(Base):
    """Job application tracking."""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Job Information
    job_title = Column(String(300), nullable=True)
    company_name = Column(String(200), nullable=True)
    job_url = Column(String(1000), nullable=False)
    job_description = Column(Text, nullable=True)
    
    # Application Status
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.DRAFT, nullable=False, index=True)
    
    # Form Data
    detected_fields = Column(JSON, nullable=True)  # Fields detected on the page
    filled_data = Column(JSON, nullable=True)  # Data that was filled
    
    # Metadata
    applied_at = Column(DateTime, nullable=True)  # When submitted
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    
    def __repr__(self):
        return f"<Application(id={self.id}, job_title='{self.job_title}', company='{self.company_name}', status='{self.status}')>"


class FieldMapping(Base):
    """Store learned field mappings to improve matching over time."""
    __tablename__ = "field_mappings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Field information
    field_label = Column(String(500), nullable=False)  # Label text on the form
    field_name = Column(String(500), nullable=True)  # HTML name attribute
    field_id = Column(String(500), nullable=True)  # HTML id attribute
    field_type = Column(String(100), nullable=False)  # input type (text, email, etc.)
    
    # Mapping
    profile_field = Column(String(200), nullable=False)  # Which profile field it maps to
    confidence_score = Column(Float, nullable=False)  # How confident we are
    
    # Learning
    times_used = Column(Integer, default=0, nullable=False)
    user_confirmed = Column(Boolean, default=False, nullable=False)  # User manually confirmed
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<FieldMapping(label='{self.field_label}' -> '{self.profile_field}', score={self.confidence_score})>"
