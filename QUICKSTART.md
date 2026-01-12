# ApplyMate Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Windows 10/11 (or macOS/Linux)
- Internet connection for downloading dependencies

## Installation

### Option 1: Traditional Installation (Recommended for First-Time Users)

#### 1. Navigate to Project Directory

```powershell
cd "c:\Users\keert\Downloads\Project X"
```

#### 2. Create Virtual Environment

```powershell
python -m venv venv
```

#### 3. Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Streamlit (UI framework)
- Playwright (browser automation)
- spaCy (NLP)
- SQLAlchemy (database ORM)
- And other dependencies

#### 5. Download spaCy Language Model

```powershell
python -m spacy download en_core_web_sm
```

#### 6. Install Playwright Browsers

```powershell
playwright install chromium
```

This downloads the Chromium browser that Playwright will use.

#### 7. Run Setup Script

```powershell
python setup.py
```

This will:
- Create necessary directories
- Initialize the database
- Create .env configuration file

### Option 2: Docker Installation (Modern, Containerized)

If you have Docker installed:

```powershell
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t applymate .
docker run -p 8501:8501 -v ${PWD}/data:/app/data applymate
```

**Advantages of Docker**:
- ✅ No Python version conflicts
- ✅ Isolated environment
- ✅ Easy deployment
- ✅ Consistent across platforms

### Option 3: Development Setup (For Contributors)

```powershell
# Standard installation first (steps 1-7 above)

# Then install development tools
pip install pytest pytest-asyncio pytest-cov ruff mypy pre-commit

# Set up pre-commit hooks (automatic code quality checks)
pre-commit install

# Run tests
pytest

# Run linter
ruff check .

# Run type checker
mypy core/ database/ --ignore-missing-imports
```

## Running the Application

### Start ApplyMate

```powershell
streamlit run ui/app.py
```

The application will open in your default web browser at `http://localhost:8501`

## First-Time Setup

### 1. Set Up Your Profile

1. Click on **"👤 Profile Manager"** in the sidebar
2. Fill out your information in the tabs:
   - **Personal Info**: Name, email, phone, address
   - **Professional**: Job title, company, LinkedIn, GitHub
   - **Education**: Degree, university, graduation year
   - **Resume**: Upload your resume (optional)
3. Click **"💾 Save"** buttons to save each section

**💡 Tip**: The more complete your profile, the better the auto-fill results!

### 2. Create Your First Application

1. Click on **"➕ New Application"** in the sidebar
2. Enter the job application URL (e.g., `https://company.com/careers/apply`)
3. Optionally add job title and company name
4. Click **"🚀 Start Application"**
5. Wait while ApplyMate analyzes the form (may take 10-30 seconds)
6. Review the detected fields and matched data
7. Click **"🌐 Open Application in Browser"**
8. Manually fill and submit the application in your browser
9. Return to ApplyMate and mark the status:
   - **✅ Mark as Submitted**
   - **⏭️ Skip This Application**
   - **💾 Save as Draft**

### 3. Track Your Applications

1. Click on **"📊 Dashboard"** in the sidebar
2. View all your applications with statistics
3. Filter by status (Draft, Submitted, Skipped)
4. Delete applications you no longer need

## Usage Tips

### Best Practices

1. **Complete Your Profile First**: Spend time filling out your profile completely before starting applications
2. **Test with Simple Forms**: Start with simpler application forms to get familiar with the workflow
3. **Review Before Submitting**: Always review auto-filled data before submitting
4. **Keep Browser Open**: Don't close the browser window until you've submitted or saved the application
5. **Add Notes**: Use the notes field to track important details about each application

### Troubleshooting

#### Browser Doesn't Open
- Make sure Playwright browsers are installed: `playwright install chromium`
- Check if the URL is valid and starts with `http://` or `https://`

#### Fields Not Detected
- Some websites use JavaScript to load forms dynamically
- Try waiting a few seconds after the page loads
- Some sites may not be compatible (use manual application)

#### Slow Performance
- Close other applications to free up memory
- Restart the application if it becomes unresponsive
- Check your internet connection

#### Database Errors
- Delete `data/database/applymate.db` and run `python setup.py` again
- Make sure you have write permissions in the project directory

### Command Reference

```powershell
# Start the application
streamlit run ui/app.py

# Initialize/reset database
python -m database.db_manager

# Run setup
python setup.py

# View logs
Get-Content data/logs/applymate.log -Tail 50

# Deactivate virtual environment (when done)
deactivate
```

## Configuration

### Environment Variables (.env)

You can customize settings by editing the `.env` file:

```ini
# Application Settings
DEBUG=False

# Browser Settings
BROWSER_HEADLESS=False          # Set to True to hide browser
BROWSER_TIMEOUT=30000           # Timeout in milliseconds

# NLP Settings
MIN_FIELD_MATCH_SCORE=0.6       # Minimum confidence for field matching (0.0-1.0)
```

## Project Structure Overview

```
Project X/
├── ui/                    # Streamlit UI
│   ├── app.py            # Main app
│   └── pages/            # UI pages
│
├── core/                 # Business logic
│   ├── browser/          # Browser automation
│   ├── nlp/              # Field matching
│   └── services/         # Services
│
├── database/             # Database models
├── config/               # Configuration
├── utils/                # Utilities
├── data/                 # Runtime data (created on first run)
├── requirements.txt      # Dependencies
└── setup.py             # Setup script
```

## Support & Documentation

- **README.md**: Overview and features
- **ARCHITECTURE.md**: Detailed architecture documentation
- **Logs**: Check `data/logs/applymate.log` for detailed logs

## What's Next?

Once you're comfortable with the basics:

1. **Customize Field Matching**: Edit patterns in `core/nlp/field_matcher.py`
2. **Add Custom Fields**: Use the JSON custom_fields in your profile
3. **Explore Logs**: Review logs to understand what's happening
4. **Track Progress**: Use the dashboard to monitor your application pipeline

## Notes

- **Human-in-the-Loop**: ApplyMate never auto-submits forms. You always have final control.
- **Local & Private**: All data stays on your computer. Nothing is sent to external servers.
- **Ethical**: No CAPTCHA bypassing, no ToS violations. Respects website terms of service.

## Version Roadmap

- **v0.1** (Current): Single-user, basic functionality
- **v0.2** (Planned): Multi-user support, authentication
- **v0.3** (Future): Resume parsing, cover letter assistance
- **v0.4** (Future): Advanced analytics, notifications

---

**Happy job hunting with ApplyMate! 🎯**

For issues or questions, check the logs or review the architecture documentation.
