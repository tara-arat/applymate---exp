"""Dashboard page for tracking applications."""

import streamlit as st
import asyncio
from datetime import datetime
from typing import List

from database import Application, ApplicationStatus
from core.services import application_service
from utils import format_datetime, get_status_emoji, get_status_color
from config import settings


def render_dashboard():
    """Render the dashboard page."""
    st.title("📊 Application Dashboard")
    
    # Get applications
    applications = asyncio.run(
        application_service.get_user_applications(settings.CURRENT_USER_ID)
    )
    
    # Get statistics
    stats = asyncio.run(
        application_service.get_application_stats(settings.CURRENT_USER_ID)
    )
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Applications", stats['total'])
    
    with col2:
        st.metric("📝 Draft", stats['draft'])
    
    with col3:
        st.metric("✅ Submitted", stats['submitted'])
    
    with col4:
        st.metric("⏭️ Skipped", stats['skipped'])
    
    st.divider()
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=["Draft", "Submitted", "Skipped"],
            default=["Draft", "Submitted"]
        )
    
    with col2:
        sort_order = st.selectbox(
            "Sort by",
            options=["Newest First", "Oldest First"],
            index=0
        )
    
    # Filter applications
    filtered_apps = filter_applications(applications, status_filter)
    
    if sort_order == "Oldest First":
        filtered_apps = list(reversed(filtered_apps))
    
    # Display applications
    if not filtered_apps:
        st.info("No applications found. Start by creating a new application!")
        
        if st.button("➕ Create New Application"):
            st.session_state.page = "new_application"
            st.rerun()
    else:
        st.markdown(f"### Applications ({len(filtered_apps)})")
        
        for app in filtered_apps:
            render_application_card(app)


def filter_applications(
    applications: List[Application],
    status_filter: List[str]
) -> List[Application]:
    """Filter applications by status."""
    if not status_filter:
        return applications
    
    status_map = {
        "Draft": ApplicationStatus.DRAFT,
        "Submitted": ApplicationStatus.SUBMITTED,
        "Skipped": ApplicationStatus.SKIPPED
    }
    
    allowed_statuses = [status_map[s] for s in status_filter]
    
    return [app for app in applications if app.status in allowed_statuses]


def render_application_card(app: Application):
    """Render a single application card."""
    status_emoji = get_status_emoji(app.status.value)
    status_color = get_status_color(app.status.value)
    
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            # Title and company
            job_title = app.job_title or "Untitled Position"
            company_name = app.company_name or "Unknown Company"
            
            st.markdown(f"### {status_emoji} {job_title}")
            st.markdown(f"**{company_name}**")
            
            # URL
            if app.job_url:
                st.markdown(f"🔗 [{app.job_url[:50]}...]({app.job_url})")
        
        with col2:
            # Status and dates
            st.markdown(f"**Status:** :{status_color}[{app.status.value.upper()}]")
            st.markdown(f"**Created:** {format_datetime(app.created_at)}")
            
            if app.applied_at:
                st.markdown(f"**Submitted:** {format_datetime(app.applied_at)}")
        
        with col3:
            # Actions
            st.markdown("**Actions:**")
            
            if app.status == ApplicationStatus.DRAFT:
                if st.button("📝 Edit", key=f"edit_{app.id}"):
                    st.session_state.edit_application_id = app.id
                    st.rerun()
            
            if st.button("🗑️ Delete", key=f"delete_{app.id}"):
                if asyncio.run(application_service.delete_application(app.id)):
                    st.success("Application deleted")
                    st.rerun()
        
        # Notes (if any)
        if app.notes:
            with st.expander("📝 Notes"):
                st.text(app.notes)
        
        st.divider()
