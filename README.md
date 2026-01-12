# ApplyMate 🎯

**A human-in-the-loop job and internship application assistant**

ApplyMate is a local Python application that helps you fill job application forms faster while maintaining complete control. It opens job applications in a browser, detects form fields, pre-fills them using your stored profile and resume data, and presents everything for your review and approval before submission.

## ✨ Features

- 🌐 **Automated Form Detection**: Opens job applications in a controlled browser
- 🤖 **Intelligent Pre-filling**: Uses AI to match your profile data to form fields
- 👤 **Human-in-the-Loop**: Never submits without your explicit approval
- 📊 **Application Tracking**: Dashboard to monitor all applications (Draft, Submitted, Skipped)
- 🔒 **Local & Private**: All data stays on your machine
- 🚀 **Multi-User Ready**: Architecture supports future authentication and per-user isolation

## 🏗️ Architecture

```
applymate/
├── config/          # Configuration management
├── database/        # SQLite models and schema
├── core/
│   ├── browser/     # Playwright automation
│   ├── nlp/         # spaCy field matching
│   └── services/    # Business logic layer
├── ui/              # Streamlit interface
├── storage/         # JSON and file storage
├── utils/           # Common utilities
└── data/            # Runtime data (gitignored)
```

## 🛠️ Tech Stack

- **Python 3.10+**
- **Playwright** (async) - Browser automation
- **Streamlit** - Web UI
- **SQLite** - Database
- **spaCy** - NLP for field matching
- **SQLAlchemy** - ORM

## 📦 Installation

1. **Clone the repository**
```bash
cd "c:\Users\keert\Downloads\Project X"
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
playwright install chromium
```

4. **Initialize database**
```bash
python -m database.db_manager
```

5. **Configure settings**
```bash
copy .env.example .env
# Edit .env with your preferences
```

## 🚀 Usage

1. **Start the application**
```bash
streamlit run ui/app.py
```

2. **Set up your profile**
   - Navigate to "Profile Manager"
   - Fill in your personal information
   - Upload your resume (optional)

3. **Start applying**
   - Click "New Application"
   - Paste the job application URL
   - Review auto-filled fields
   - Approve and submit

## 🔒 Ethics & Privacy

- **Local-Only**: No data leaves your machine
- **Human-in-the-Loop**: You review and approve every submission
- **No CAPTCHA Bypassing**: Respects website security measures
- **No ToS Evasion**: Complies with platform terms of service
- **Transparent**: Open-source and auditable

## 🗺️ Roadmap

### Current (v0.1 - Single User)
- ✅ Basic browser automation
- ✅ Profile management
- ✅ Application tracking
- ✅ Form field detection

### Future (v0.2 - Multi-User)
- [ ] User authentication
- [ ] Per-user data isolation
- [ ] Role-based access control
- [ ] Advanced resume parsing
- [ ] Cover letter generation assistance

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is a local-first, ethical application. Contributions that maintain these principles are welcome!

## ⚠️ Disclaimer

ApplyMate is designed to assist with legitimate job applications. Users are responsible for ensuring their use complies with the terms of service of job application platforms.
