"""Profile manager page for managing user profile."""

import streamlit as st
import asyncio

from core.services import profile_service
from utils import is_valid_email, is_valid_url, is_valid_phone, sanitize_filename
from config import settings


def render_profile_manager():
    """Render the profile manager page."""
    st.title("👤 Profile Manager")
    
    st.markdown("""
    Your profile information is used to automatically fill job application forms.
    Complete as much as possible for better auto-fill results.
    """)
    
    # Get existing profile
    profile = asyncio.run(
        profile_service.get_profile(settings.CURRENT_USER_ID)
    )
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Personal Info",
        "💼 Professional",
        "🎓 Education",
        "📄 Resume"
    ])
    
    with tab1:
        render_personal_info(profile)
    
    with tab2:
        render_professional_info(profile)
    
    with tab3:
        render_education_info(profile)
    
    with tab4:
        render_resume_section(profile)


def render_personal_info(profile):
    """Render personal information section."""
    st.markdown("### Personal Information")
    
    with st.form("personal_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "First Name *",
                value=profile.first_name if profile else "",
                help="Your legal first name"
            )
        
        with col2:
            last_name = st.text_input(
                "Last Name *",
                value=profile.last_name if profile else "",
                help="Your legal last name"
            )
        
        email = st.text_input(
            "Email Address *",
            value=profile.email if profile else "",
            help="Your primary email address"
        )
        
        phone = st.text_input(
            "Phone Number",
            value=profile.phone if profile else "",
            placeholder="+1 (555) 123-4567",
            help="Your phone number with country code"
        )
        
        st.markdown("#### Address")
        
        address_line1 = st.text_input(
            "Address Line 1",
            value=profile.address_line1 if profile else "",
            placeholder="123 Main Street"
        )
        
        address_line2 = st.text_input(
            "Address Line 2",
            value=profile.address_line2 if profile else "",
            placeholder="Apt 4B"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            city = st.text_input(
                "City",
                value=profile.city if profile else "",
                placeholder="San Francisco"
            )
        
        with col2:
            state = st.text_input(
                "State/Province",
                value=profile.state if profile else "",
                placeholder="CA"
            )
        
        with col3:
            zip_code = st.text_input(
                "ZIP/Postal Code",
                value=profile.zip_code if profile else "",
                placeholder="94102"
            )
        
        country = st.text_input(
            "Country",
            value=profile.country if profile else "",
            placeholder="United States"
        )
        
        submitted = st.form_submit_button("💾 Save Personal Info", use_container_width=True)
        
        if submitted:
            # Validation
            errors = []
            
            if not first_name or not last_name:
                errors.append("First and last name are required")
            
            if not email:
                errors.append("Email is required")
            elif not is_valid_email(email):
                errors.append("Invalid email address")
            
            if phone and not is_valid_phone(phone):
                errors.append("Invalid phone number format")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Save profile
                profile_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'address_line1': address_line1,
                    'address_line2': address_line2,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'country': country
                }
                
                if profile:
                    asyncio.run(
                        profile_service.update_profile(settings.CURRENT_USER_ID, profile_data)
                    )
                    st.success("✅ Personal information updated!")
                else:
                    asyncio.run(
                        profile_service.create_profile(settings.CURRENT_USER_ID, profile_data)
                    )
                    st.success("✅ Profile created!")
                
                st.rerun()


def render_professional_info(profile):
    """Render professional information section."""
    st.markdown("### Professional Information")
    
    with st.form("professional_info_form"):
        current_title = st.text_input(
            "Current Job Title",
            value=profile.current_title if profile else "",
            placeholder="Software Engineer"
        )
        
        current_company = st.text_input(
            "Current Company",
            value=profile.current_company if profile else "",
            placeholder="Tech Corp Inc."
        )
        
        years_of_experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=50,
            value=profile.years_of_experience if profile and profile.years_of_experience else 0,
            help="Total years of professional experience"
        )
        
        st.markdown("#### Online Profiles")
        
        linkedin_url = st.text_input(
            "LinkedIn URL",
            value=profile.linkedin_url if profile else "",
            placeholder="https://linkedin.com/in/yourprofile"
        )
        
        github_url = st.text_input(
            "GitHub URL",
            value=profile.github_url if profile else "",
            placeholder="https://github.com/yourusername"
        )
        
        portfolio_url = st.text_input(
            "Portfolio/Website URL",
            value=profile.portfolio_url if profile else "",
            placeholder="https://yourportfolio.com"
        )
        
        submitted = st.form_submit_button("💾 Save Professional Info", use_container_width=True)
        
        if submitted:
            # Validation
            errors = []
            
            if linkedin_url and not is_valid_url(linkedin_url):
                errors.append("Invalid LinkedIn URL")
            
            if github_url and not is_valid_url(github_url):
                errors.append("Invalid GitHub URL")
            
            if portfolio_url and not is_valid_url(portfolio_url):
                errors.append("Invalid Portfolio URL")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Save profile
                profile_data = {
                    'current_title': current_title,
                    'current_company': current_company,
                    'years_of_experience': years_of_experience if years_of_experience > 0 else None,
                    'linkedin_url': linkedin_url,
                    'github_url': github_url,
                    'portfolio_url': portfolio_url
                }
                
                if profile:
                    asyncio.run(
                        profile_service.update_profile(settings.CURRENT_USER_ID, profile_data)
                    )
                    st.success("✅ Professional information updated!")
                else:
                    asyncio.run(
                        profile_service.create_profile(settings.CURRENT_USER_ID, profile_data)
                    )
                    st.success("✅ Profile created!")
                
                st.rerun()


def render_education_info(profile):
    """Render education information section."""
    st.markdown("### Education Information")
    
    with st.form("education_info_form"):
        education_level = st.selectbox(
            "Highest Education Level",
            options=["", "High School", "Associate's", "Bachelor's", "Master's", "Ph.D.", "Other"],
            index=0 if not profile or not profile.education_level else 
                  ["", "High School", "Associate's", "Bachelor's", "Master's", "Ph.D.", "Other"].index(profile.education_level) 
                  if profile.education_level in ["", "High School", "Associate's", "Bachelor's", "Master's", "Ph.D.", "Other"] else 0
        )
        
        university = st.text_input(
            "University/Institution",
            value=profile.university if profile else "",
            placeholder="Stanford University"
        )
        
        major = st.text_input(
            "Major/Field of Study",
            value=profile.major if profile else "",
            placeholder="Computer Science"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            graduation_year = st.number_input(
                "Graduation Year",
                min_value=1950,
                max_value=2030,
                value=profile.graduation_year if profile and profile.graduation_year else 2024,
                help="Year of graduation or expected graduation"
            )
        
        with col2:
            gpa = st.number_input(
                "GPA (Optional)",
                min_value=0.0,
                max_value=4.0,
                value=profile.gpa if profile and profile.gpa else 0.0,
                step=0.01,
                format="%.2f",
                help="GPA on a 4.0 scale"
            )
        
        submitted = st.form_submit_button("💾 Save Education Info", use_container_width=True)
        
        if submitted:
            # Save profile
            profile_data = {
                'education_level': education_level if education_level else None,
                'university': university,
                'major': major,
                'graduation_year': graduation_year if graduation_year > 0 else None,
                'gpa': gpa if gpa > 0 else None
            }
            
            if profile:
                asyncio.run(
                    profile_service.update_profile(settings.CURRENT_USER_ID, profile_data)
                )
                st.success("✅ Education information updated!")
            else:
                asyncio.run(
                    profile_service.create_profile(settings.CURRENT_USER_ID, profile_data)
                )
                st.success("✅ Profile created!")
            
            st.rerun()


def render_resume_section(profile):
    """Render resume upload section."""
    st.markdown("### Resume")
    
    if profile and profile.resume_filename:
        st.success(f"📄 Current resume: **{profile.resume_filename}**")
        
        if st.button("🗑️ Remove Resume"):
            asyncio.run(
                profile_service.update_profile(
                    settings.CURRENT_USER_ID,
                    {'resume_filename': None, 'resume_path': None}
                )
            )
            st.success("Resume removed")
            st.rerun()
    else:
        st.info("No resume uploaded yet")
    
    st.markdown("#### Upload New Resume")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    if uploaded_file is not None:
        filename = sanitize_filename(uploaded_file.name)
        
        st.write(f"📄 Selected: {filename}")
        
        if st.button("💾 Upload Resume"):
            resume_content = uploaded_file.read()
            
            result = asyncio.run(
                profile_service.save_resume(
                    settings.CURRENT_USER_ID,
                    filename,
                    resume_content
                )
            )
            
            if result:
                st.success("✅ Resume uploaded successfully!")
                st.info("💡 Tip: Resume parsing will be available in a future version.")
                st.rerun()
            else:
                st.error("Failed to upload resume")
    
    st.markdown("""
    ---
    
    **Note:** Resume parsing is not yet implemented in this version. 
    Your resume will be stored for future use, but you'll need to manually 
    enter your information in the profile fields above.
    """)
