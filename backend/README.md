# Personal Finance Tracker - Backend

Backend API for the Personal Finance Tracker application built with FastAPI.

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
- Git

### Quick Start

1. **Clone the repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd finalproject-JAGM/backend
   ```

2. **Create and activate virtual environment**:

   **On macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **On Windows:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Verify Python version**:

   ```bash
   python --version
   # Should show Python 3.11.x or higher
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the development server** (when implemented):
   ```bash
   uvicorn app.main:app --reload
   ```

### Virtual Environment Management

#### Activation Commands

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

#### Deactivation

To deactivate the virtual environment:

```bash
deactivate
```

#### Verification

After activation, you should see `(venv)` at the beginning of your command prompt, and:

```bash
which python  # Should point to venv/bin/python
pip list      # Should show only packages installed in the virtual environment
```

### Project Structure

```
backend/
├── venv/                 # Virtual environment (not tracked in git)
├── app/                  # Main application code
│   ├── __init__.py      # Main app package
│   ├── main.py          # FastAPI application entry point
│   ├── api/             # API endpoints and routing
│   │   ├── __init__.py
│   │   └── v1/          # API version 1
│   │       └── __init__.py
│   ├── core/            # Core functionality and utilities
│   │   └── __init__.py
│   ├── models/          # Database models and ORM
│   │   └── __init__.py
│   ├── schemas/         # Pydantic models for validation
│   │   └── __init__.py
│   └── services/        # Business logic services
│       └── __init__.py
├── tests/               # Test files (mirrors app structure)
│   ├── __init__.py
│   └── app/             # Mirrors app/ directory structure
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── v1/
│       │       └── __init__.py
│       ├── core/
│       │   └── __init__.py
│       ├── models/
│       │   └── __init__.py
│       ├── schemas/
│       │   └── __init__.py
│       └── services/
│           └── __init__.py
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies (to be created)
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

### Dependencies

The following core dependencies are installed and configured:

- **FastAPI 0.104.1** - Modern, fast web framework for building APIs
- **Uvicorn 0.24.0** - ASGI server for running FastAPI applications
- **SQLAlchemy 2.0.23** - SQL toolkit and Object-Relational Mapping (ORM) library
- **Alembic 1.12.1** - Database migration tool for SQLAlchemy
- **Pydantic 2.11.9** - Data validation and settings management (included with FastAPI)

All dependencies are pinned to specific versions in `requirements.txt` for reproducible builds.

#### Verifying Installation

After installing dependencies, you can verify the installation:

```bash
# Check installed packages
pip list

# Test imports
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
python -c "import uvicorn; print(f'Uvicorn version: {uvicorn.__version__}')"
python -c "import sqlalchemy; print(f'SQLAlchemy version: {sqlalchemy.__version__}')"
python -c "import alembic; print(f'Alembic version: {alembic.__version__}')"
```

### Development Workflow

1. Always activate the virtual environment before working
2. Install new dependencies with `pip install <package>`
3. Update requirements files when adding dependencies
4. Run tests before committing changes
5. Deactivate virtual environment when done

### Troubleshooting

**Virtual environment not activating:**

- Ensure you're in the correct directory (`backend/`)
- Check that the `venv` directory exists
- Try using the full path: `source ./venv/bin/activate`

**Python version issues:**

- Verify Python 3.11+ is installed: `python3 --version`
- If using `python` command, ensure it points to Python 3.11+

**Permission issues (macOS/Linux):**

- You might need to run: `chmod +x venv/bin/activate`

### Next Steps

**Completed:**

- ✅ Virtual environment setup (US0.2-T1)
- ✅ FastAPI project structure (US0.2-T2)
- ✅ Core dependencies installation (US0.2-T3)

**Upcoming tasks:**

- Basic FastAPI application setup (US0.2-T4)
- Configuration management (US0.2-T5)
- Logging setup (US0.2-T6)
- Error handling (US0.2-T7)
- Development server configuration (US0.2-T8)
- Testing framework setup (US0.2-T9)

For detailed task breakdown, see: `../backlog/Epic 0: Development Environment & Project Scaffolding/US0.2-backend-development-environment-setup-tasks.md`
