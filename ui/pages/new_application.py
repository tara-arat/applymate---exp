"""New application page for starting job applications."""

import streamlit as st
import asyncio
from playwright.async_api import Page

from core.browser import browser_manager, page_analyzer, form_filler
from core.nlp import field_matcher
from core.services import application_service, profile_service
from utils import is_valid_url
from config import settings


def render_new_application():
    """Render the new application page."""
    st.title("➕ New Application")
    
    # Initialize session state
    if 'application_step' not in st.session_state:
        st.session_state.application_step = 'url_input'
    
    if 'current_application_id' not in st.session_state:
        st.session_state.current_application_id = None
    
    if 'detected_fields' not in st.session_state:
        st.session_state.detected_fields = []
    
    if 'field_mappings' not in st.session_state:
        st.session_state.field_mappings = {}
    
    # Render based on current step
    if st.session_state.application_step == 'url_input':
        render_url_input()
    
    elif st.session_state.application_step == 'field_detection':
        render_field_detection()
    
    elif st.session_state.application_step == 'review':
        render_review()


def render_url_input():
    """Render URL input step."""
    st.markdown("""
    ### Step 1: Enter Job Application URL
    
    Paste the URL of the job application form you want to fill.
    """)
    
    with st.form("url_input_form"):
        job_url = st.text_input(
            "Job Application URL",
            placeholder="https://company.com/careers/apply/12345",
            help="Enter the full URL of the job application page"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input(
                "Job Title (Optional)",
                placeholder="e.g., Software Engineer"
            )
        
        with col2:
            company_name = st.text_input(
                "Company Name (Optional)",
                placeholder="e.g., Tech Corp"
            )
        
        submitted = st.form_submit_button("🚀 Start Application", use_container_width=True)
        
        if submitted:
            if not job_url:
                st.error("Please enter a job application URL")
            elif not is_valid_url(job_url):
                st.error("Please enter a valid URL (must start with http:// or https://)")
            else:
                # Create application
                application = asyncio.run(
                    application_service.create_application(
                        user_id=settings.CURRENT_USER_ID,
                        job_url=job_url,
                        job_title=job_title or None,
                        company_name=company_name or None
                    )
                )
                
                st.session_state.current_application_id = application.id
                st.session_state.application_step = 'field_detection'
                st.rerun()


def render_field_detection():
    """Render field detection step."""
    st.markdown("### Step 2: Analyzing Application Form")
    
    # Get profile
    profile = asyncio.run(
        profile_service.get_profile(settings.CURRENT_USER_ID)
    )
    
    if not profile:
        st.warning("⚠️ No profile found. Please set up your profile first.")
        if st.button("Go to Profile Manager"):
            st.session_state.page = "profile_manager"
            st.rerun()
        return
    
    # Get application
    application = asyncio.run(
        application_service.get_application(st.session_state.current_application_id)
    )
    
    if not application:
        st.error("Application not found")
        return
    
    st.info(f"🌐 Opening: {application.job_url}")
    
    with st.spinner("Detecting form fields... This may take a moment."):
        detected_fields, field_mappings = asyncio.run(
            detect_and_match_fields(application.job_url, profile)
        )
    
    if not detected_fields:
        st.error("❌ Could not detect any form fields on this page. The page might require JavaScript or have a different structure.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Again"):
                st.rerun()
        with col2:
            if st.button("⬅️ Back"):
                st.session_state.application_step = 'url_input'
                st.rerun()
        return
    
    # Save detected fields
    asyncio.run(
        application_service.save_detected_fields(
            st.session_state.current_application_id,
            [field.to_dict() for field in detected_fields]
        )
    )
    
    st.session_state.detected_fields = detected_fields
    st.session_state.field_mappings = field_mappings
    
    st.success(f"✅ Detected {len(detected_fields)} form fields!")
    
    # Show preview
    st.markdown("#### Detected Fields")
    
    matched_count = sum(1 for pf, score in field_mappings.values() if pf and score >= settings.MIN_FIELD_MATCH_SCORE)
    
    st.info(f"📊 Matched {matched_count}/{len(detected_fields)} fields with confidence ≥ {settings.MIN_FIELD_MATCH_SCORE}")
    
    # Display fields in a table
    for field in detected_fields[:5]:  # Show first 5
        profile_field, score = field_mappings.get(field, (None, 0.0))
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.text(f"📝 {field.label or field.placeholder or field.name or 'Unnamed'}")
        
        with col2:
            if profile_field and score >= settings.MIN_FIELD_MATCH_SCORE:
                st.text(f"➡️ {profile_field} ({score:.0%})")
            else:
                st.text("❓ No match")
        
        with col3:
            st.text(f"[{field.field_type}]")
    
    if len(detected_fields) > 5:
        st.text(f"... and {len(detected_fields) - 5} more fields")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.application_step = 'url_input'
            st.rerun()
    
    with col2:
        if st.button("➡️ Continue to Review", use_container_width=True):
            st.session_state.application_step = 'review'
            st.rerun()


def render_review():
    """Render review step."""
    st.markdown("### Step 3: Review & Submit")
    
    st.info("""
    ⚠️ **Manual Submission Required**
    
    ApplyMate has detected the form fields and prepared the data. 
    You'll need to manually open the browser, review the pre-filled information, 
    and submit the application yourself.
    
    This ensures you maintain full control and comply with website terms of service.
    """)
    
    # Get profile
    profile = asyncio.run(
        profile_service.get_profile(settings.CURRENT_USER_ID)
    )
    
    profile_dict = profile_service.profile_to_dict(profile)
    
    # Show matched data
    st.markdown("#### 📋 Data Ready to Fill")
    
    matched_fields = {
        field: (pf, score)
        for field, (pf, score) in st.session_state.field_mappings.items()
        if pf and score >= settings.MIN_FIELD_MATCH_SCORE
    }
    
    if matched_fields:
        for field, (profile_field, score) in list(matched_fields.items())[:10]:
            value = profile_dict.get(profile_field)
            if value:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.text(field.label or field.name or "Unnamed")
                with col2:
                    st.code(str(value))
    
    # Next steps
    st.markdown("#### 🚀 Next Steps")
    
    st.markdown("""
    1. Click **"Open Application in Browser"** below
    2. Review the detected fields and matched data above
    3. Manually fill the form using your profile information
    4. Submit the application when ready
    5. Return here to mark the application status
    """)
    
    # Get application
    application = asyncio.run(
        application_service.get_application(st.session_state.current_application_id)
    )
    
    if st.button("🌐 Open Application in Browser", use_container_width=True):
        st.markdown(f"Opening: [{application.job_url}]({application.job_url})")
        st.info("Please complete the application in your browser and return here.")
    
    st.divider()
    
    # Status update
    st.markdown("#### Update Application Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Mark as Submitted", use_container_width=True):
            asyncio.run(
                application_service.submit_application(st.session_state.current_application_id)
            )
            st.success("Application marked as submitted!")
            reset_application_state()
            st.rerun()
    
    with col2:
        if st.button("⏭️ Skip This Application", use_container_width=True):
            asyncio.run(
                application_service.skip_application(st.session_state.current_application_id)
            )
            st.info("Application marked as skipped")
            reset_application_state()
            st.rerun()
    
    with col3:
        if st.button("💾 Save as Draft", use_container_width=True):
            st.success("Application saved as draft")
            reset_application_state()
            st.rerun()


async def detect_and_match_fields(url: str, profile):
    """Detect fields on page and match to profile."""
    try:
        # Initialize field matcher
        field_matcher.initialize()
        
        # Start browser
        await browser_manager.start()
        page = await browser_manager.new_page()
        
        # Navigate to URL
        success = await browser_manager.navigate_to(page, url)
        
        if not success:
            return [], {}
        
        # Detect fields
        detected_fields = await page_analyzer.detect_form_fields(page)
        
        # Match fields to profile
        if profile:
            field_mappings = field_matcher.match_fields(detected_fields)
        else:
            field_mappings = {}
        
        # Keep browser open for user
        # await browser_manager.close_page(page)
        
        return detected_fields, field_mappings
    
    except Exception as e:
        st.error(f"Error detecting fields: {e}")
        return [], {}


def reset_application_state():
    """Reset application state."""
    st.session_state.application_step = 'url_input'
    st.session_state.current_application_id = None
    st.session_state.detected_fields = []
    st.session_state.field_mappings = {}
