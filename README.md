# ApplyMate 🎯

**A human-in-the-loop job and internship application assistant**

ApplyMate is a local Python application that helps you fill job application forms faster while maintaining complete control. It opens job applications in a browser, detects form fields, pre-fills them using your stored profile and resume data, and presents everything for your review and approval before submission.


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




This is a local-first, ethical application. Contributions that maintain these principles are welcome!

## ⚠️ Disclaimer

ApplyMate is designed to assist with legitimate job applications. Users are responsible for ensuring their use complies with the terms of service of job application platforms.
