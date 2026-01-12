"""Main Streamlit application for ApplyMate."""

import streamlit as st
import asyncio
from loguru import logger

# Import utilities first to set up logging
from utils import setup_logging

# Import database
from database import init_db, close_db
from config import settings

# Set page config
st.set_page_config(
    page_title="ApplyMate - Job Application Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


async def initialize_app():
    """Initialize the application."""
    try:
        # Ensure directories exist
        settings.ensure_directories()
        
        # Initialize database
        await init_db()
        
        logger.info("Application initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        return False


def main():
    """Main application entry point."""
    
    # Initialize app on first run
    if 'initialized' not in st.session_state:
        with st.spinner("Initializing ApplyMate..."):
            success = asyncio.run(initialize_app())
            st.session_state.initialized = success
            
            if not success:
                st.error("Failed to initialize application. Check logs for details.")
                st.stop()
    
    # Sidebar navigation
    st.sidebar.title("🎯 ApplyMate")
    st.sidebar.markdown("*Your Job Application Assistant*")
    st.sidebar.divider()
    
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Dashboard", "➕ New Application", "👤 Profile Manager", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    # Page routing
    if page == "📊 Dashboard":
        from ui.pages.dashboard import render_dashboard
        render_dashboard()
    
    elif page == "➕ New Application":
        from ui.pages.new_application import render_new_application
        render_new_application()
    
    elif page == "👤 Profile Manager":
        from ui.pages.profile_manager import render_profile_manager
        render_profile_manager()
    
    elif page == "ℹ️ About":
        render_about()
    
    # Footer
    st.sidebar.divider()
    st.sidebar.markdown(
        f"""
        <div style='text-align: center; font-size: 0.8em; color: gray;'>
        ApplyMate v{settings.APP_VERSION}<br>
        Local & Private 🔒
        </div>
        """,
        unsafe_allow_html=True
    )


def render_about():
    """Render about page."""
    st.title("ℹ️ About ApplyMate")
    
    st.markdown("""
    ## What is ApplyMate?
    
    ApplyMate is a **human-in-the-loop** job application assistant that helps you fill out 
    job applications faster while maintaining complete control.
    
    ### ✨ Key Features
    
    - **🌐 Automated Form Detection**: Opens job applications in a browser and detects form fields
    - **🤖 Intelligent Pre-filling**: Uses AI to match your profile data to form fields
    - **👤 Human Control**: Never submits without your explicit approval
    - **📊 Application Tracking**: Dashboard to monitor all applications
    - **🔒 Local & Private**: All data stays on your machine
    
    ### 🎯 How It Works
    
    1. **Set Up Your Profile**: Enter your personal information once
    2. **Start an Application**: Paste a job application URL
    3. **Review & Approve**: ApplyMate pre-fills fields for your review
    4. **Submit Manually**: You maintain full control over submission
    
    ### 🔒 Privacy & Ethics
    
    - **Local-Only**: No data is sent to external servers
    - **No Auto-Submit**: You always have final control
    - **Ethical**: No CAPTCHA bypassing or ToS violations
    - **Transparent**: Open-source and auditable
    
    ### 🛠️ Tech Stack
    
    - Python 3.10+
    - Playwright (Browser Automation)
    - Streamlit (UI)
    - SQLite (Database)
    - spaCy (NLP)
    
    ### 📚 Getting Started
    
    1. Navigate to **Profile Manager** to set up your information
    2. Go to **New Application** to start applying
    3. Track your progress in **Dashboard**
    
    ---
    
    *ApplyMate is designed to assist with legitimate job applications while respecting 
    website terms of service and maintaining ethical practices.*
    """)


if __name__ == "__main__":
    main()
