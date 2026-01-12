# ApplyMate Architecture Documentation

## Overview

ApplyMate is a human-in-the-loop job application assistant built with a clean, extensible architecture that supports future multi-user functionality while starting with a simple single-user implementation.

## Architecture Principles

1. **Separation of Concerns**: Clear boundaries between UI, business logic, data access, and external services
2. **Multi-User Ready**: Database schema and services designed for multiple users from day one
3. **Async-First**: Leverages Python's async/await for non-blocking I/O operations
4. **Modularity**: Each component is independent and can be tested/modified separately
5. **Extensibility**: Easy to add new features without refactoring existing code

## Directory Structure

```
applymate/
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py        # Centralized settings using Pydantic
│
├── database/              # Data persistence layer
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models (User, Profile, Application)
│   └── db_manager.py      # Database connection and session management
│
├── core/                  # Core business logic
│   ├── browser/           # Browser automation
│   │   ├── __init__.py
│   │   ├── playwright_manager.py    # Playwright lifecycle management
│   │   ├── page_analyzer.py         # Form field detection
│   │   └── form_filler.py           # Form field population
│   │
│   ├── nlp/               # Natural language processing
│   │   ├── __init__.py
│   │   ├── field_matcher.py         # Profile-to-form field matching
│   │   └── resume_parser.py         # Resume parsing (future)
│   │
│   └── services/          # Business logic services
│       ├── __init__.py
│       ├── application_service.py   # Application CRUD operations
│       ├── profile_service.py       # Profile management
│       └── auth_service.py          # Authentication (future)
│
├── ui/                    # User interface (Streamlit)
│   ├── __init__.py
│   ├── app.py            # Main application entry point
│   └── pages/            # Page components
│       ├── __init__.py
│       ├── dashboard.py           # Application tracking
│       ├── new_application.py     # New application workflow
│       └── profile_manager.py     # Profile management
│
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── logger.py         # Logging configuration
│   ├── validators.py     # Input validation
│   └── helpers.py        # Helper functions
│
├── storage/              # Storage utilities (future enhancement)
│   └── __init__.py
│
└── data/                 # Runtime data (gitignored)
    ├── database/         # SQLite database
    ├── profiles/         # User profiles (JSON backup)
    ├── uploads/          # Resume uploads
    └── logs/             # Application logs
```

## Component Details

### 1. Configuration Layer (`config/`)

**Purpose**: Centralized configuration management

**Key Components**:
- `Settings` class using Pydantic for type-safe configuration
- Environment variable loading via `.env` file
- Path management for all data directories
- Future-ready for authentication secrets

**Design Decision**: Using Pydantic ensures type safety and validation at the configuration level, preventing runtime errors from misconfiguration.

### 2. Database Layer (`database/`)

**Purpose**: Data persistence and ORM

**Key Components**:
- **Models**:
  - `User`: User accounts (multi-user ready)
  - `Profile`: User profile information for auto-fill
  - `Application`: Job application tracking
  - `FieldMapping`: Learned field mappings for improving matching
  - `ApplicationStatus`: Enum for application states

- **DatabaseManager**: Async SQLAlchemy connection and session management

**Design Decisions**:
- **Multi-User from Day 1**: All tables have `user_id` foreign keys
- **Async/Await**: Using `aiosqlite` for non-blocking database operations
- **JSON Fields**: Flexible storage for dynamic/custom fields
- **Learning System**: `FieldMapping` table stores learned patterns

**Migration Path**: 
- v0.1: Single user (user_id=1 hardcoded)
- v0.2: Add authentication, per-user sessions

### 3. Core Business Logic (`core/`)

#### 3a. Browser Automation (`core/browser/`)

**Purpose**: Interact with web pages using Playwright

**Components**:

1. **PlaywrightManager**:
   - Manages browser lifecycle
   - Creates browser contexts and pages
   - Handles navigation and cleanup
   - Singleton pattern for resource efficiency

2. **PageAnalyzer**:
   - Detects form fields on web pages
   - Extracts field metadata (type, name, id, label, placeholder)
   - Handles input, textarea, and select elements
   - Returns structured `FormField` objects

3. **FormFiller**:
   - Fills detected form fields with profile data
   - Handles different input types appropriately
   - Human-like typing with delays
   - Returns success/failure status per field

**Design Decisions**:
- **Non-intrusive**: Browser remains visible for user control
- **Metadata-rich**: Captures all available field information for matching
- **Async Operations**: Non-blocking page interactions

#### 3b. NLP Field Matching (`core/nlp/`)

**Purpose**: Intelligently map form fields to profile data

**Components**:

1. **FieldMatcher**:
   - Uses spaCy for semantic field matching
   - Pattern-based fallback matching
   - Confidence scoring for matches
   - Predefined patterns for common fields
   - Learning capability (via `FieldMapping` table)

2. **ResumeParser** (placeholder):
   - Will extract structured data from resumes
   - Planned for v0.2

**Design Decisions**:
- **Two-tier matching**: NLP first, pattern fallback
- **Confidence scores**: Allows filtering low-confidence matches
- **Extensible patterns**: Easy to add new field types
- **Learning system**: Improves over time with user feedback

#### 3c. Service Layer (`core/services/`)

**Purpose**: Business logic abstraction

**Components**:

1. **ApplicationService**:
   - CRUD operations for applications
   - Status management (draft, submitted, skipped)
   - Application statistics
   - Field data storage

2. **ProfileService**:
   - Profile CRUD operations
   - Resume file management
   - Profile-to-dict conversion for filling

3. **AuthService** (placeholder):
   - Future user authentication
   - Password hashing/verification
   - Session management

**Design Decisions**:
- **Service pattern**: Encapsulates business logic separate from UI
- **Async-first**: All service methods are async
- **Transaction management**: Database sessions handled within services
- **Future-ready**: Auth service stub for easy extension

### 4. User Interface (`ui/`)

**Purpose**: Streamlit-based user interface

**Components**:

1. **app.py**: Main entry point
   - Navigation and routing
   - Application initialization
   - Session state management

2. **Pages**:
   - `dashboard.py`: View and manage applications
   - `new_application.py`: Multi-step application workflow
   - `profile_manager.py`: Manage user profile

**Design Decisions**:
- **Multi-page architecture**: Clean separation of concerns
- **Session state**: Maintains state across interactions
- **Async wrapper**: Uses `asyncio.run()` to call async services
- **Progressive disclosure**: Step-by-step workflow for applications

### 5. Utilities (`utils/`)

**Purpose**: Common helper functions

**Components**:
- **logger.py**: Loguru configuration (console + file)
- **validators.py**: Input validation (email, URL, phone)
- **helpers.py**: Formatting and display utilities

## Data Flow

### Application Creation Flow

```
User Input (URL)
    ↓
UI (new_application.py)
    ↓
ApplicationService.create_application()
    ↓
Database (Application model)
    ↓
PlaywrightManager.navigate_to()
    ↓
PageAnalyzer.detect_form_fields()
    ↓
FieldMatcher.match_fields()
    ↓
UI (review screen)
    ↓
User manually submits
    ↓
ApplicationService.submit_application()
    ↓
Database (status update)
```

### Profile to Form Mapping

```
Profile (Database)
    ↓
ProfileService.profile_to_dict()
    ↓
DetectedFields (PageAnalyzer)
    ↓
FieldMatcher (NLP + Patterns)
    ↓
{FormField → (profile_field, confidence)}
    ↓
FormFiller (when implemented)
    ↓
Browser (filled fields)
```

## Key Design Patterns

1. **Service Layer Pattern**: Business logic separated from UI and data access
2. **Repository Pattern**: Database operations encapsulated in services
3. **Singleton Pattern**: Single browser manager instance
4. **Factory Pattern**: Session management in DatabaseManager
5. **Strategy Pattern**: Two-tier field matching (NLP + Pattern)

## Extensibility Points

### Adding Multi-User Authentication (v0.2)

1. **Backend**:
   - Implement `AuthService.authenticate()`
   - Add password hashing (bcrypt)
   - Create session management
   - Add middleware for user context

2. **UI**:
   - Add login page
   - Session-based user_id instead of hardcoded
   - Add logout functionality

3. **Database**:
   - Activate password_hash field
   - Add session table
   - Add user preferences table

### Adding Resume Parsing

1. Implement `ResumeParser` with PDF/DOCX extraction
2. Add spaCy NER for entity extraction
3. Map extracted entities to profile fields
4. Add profile auto-population from resume

### Adding AI-Powered Cover Letters

1. Add OpenAI/Claude integration
2. Create cover letter template system
3. Add job description analysis
4. Generate personalized cover letters

## Testing Strategy

```
tests/
├── test_browser/
│   ├── test_playwright_manager.py
│   ├── test_page_analyzer.py
│   └── test_form_filler.py
│
├── test_nlp/
│   ├── test_field_matcher.py
│   └── test_resume_parser.py
│
├── test_services/
│   ├── test_application_service.py
│   ├── test_profile_service.py
│   └── test_auth_service.py
│
└── test_ui/
    └── test_pages.py
```

## Security Considerations

1. **Local-Only**: No external API calls (except for websites being applied to)
2. **No Auto-Submit**: Human always in control
3. **SQL Injection**: Using SQLAlchemy ORM with parameterized queries
4. **Path Traversal**: Filename sanitization in uploads
5. **Future Auth**: Will use bcrypt for password hashing

## Performance Considerations

1. **Async Operations**: Non-blocking I/O for browser and database
2. **Connection Pooling**: SQLAlchemy async session management
3. **Lazy Loading**: Browser only started when needed
4. **Resource Cleanup**: Proper cleanup of browser resources

## Future Architecture Enhancements

### Phase 1 (v0.2 - Multi-User)
- User authentication system
- Per-user data isolation
- Session management
- Role-based access control

### Phase 2 (v0.3 - Intelligence)
- Resume parsing with spaCy NER
- Cover letter generation
- Job description analysis
- Application quality scoring

### Phase 3 (v0.4 - Scale)
- Background job processing
- Email notifications
- Calendar integration
- Analytics dashboard

### Phase 4 (v0.5 - Enterprise)
- Team features
- Admin dashboard
- Usage analytics
- API for integrations

## Conclusion

ApplyMate's architecture is designed to be:
- **Clean**: Clear separation of concerns
- **Extensible**: Easy to add new features
- **Maintainable**: Well-organized and documented
- **Scalable**: Ready for multi-user from day one
- **Ethical**: Human-in-the-loop, respecting terms of service
