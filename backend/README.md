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

5. **Configure environment variables** (optional):

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env file with your preferred settings
   # The application will work with default values if .env is not present
   ```

6. **Initialize the database**:

   ```bash
   # Run the database initialization script
   python -m app.scripts.init_db
   ```

   This script will:

   - Create the SQLite database file if it doesn't exist
   - Run all pending Alembic migrations
   - Verify the database connection
   - Log all initialization steps

   The script is idempotent and can be run multiple times safely.

7. **Run the development server**:

   ```bash
   uvicorn app.main:app --reload
   ```

   The server will start on `http://localhost:8000` with:

   - Health check endpoint: `http://localhost:8000/health`
   - Interactive API docs: `http://localhost:8000/docs`
   - OpenAPI spec: `http://localhost:8000/openapi.json`

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
│   ├── main.py          # FastAPI application entry point with global error handlers
│   ├── api/             # API endpoints and routing
│   │   ├── __init__.py
│   │   └── v1/          # API version 1
│   │       └── __init__.py
│   ├── core/            # Core functionality and utilities
│   │   ├── __init__.py
│   │   ├── config.py    # Configuration management
│   │   ├── database.py  # Database configuration and session management
│   │   ├── exceptions.py # Custom exception classes
│   │   └── logging.py   # Structured logging configuration
│   ├── models/          # Database models and ORM
│   │   └── __init__.py
│   ├── schemas/         # Pydantic models for validation
│   │   └── __init__.py
│   └── services/        # Business logic services
│       └── __init__.py
├── tests/               # Test files organized by type
│   ├── __init__.py
│   ├── conftest.py      # Shared test fixtures and configuration
│   ├── unit/            # Fast, isolated unit tests
│   │   ├── __init__.py
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── core/
│   │       │   ├── __init__.py
│   │       │   ├── test_config.py     # Configuration tests
│   │       │   ├── test_database.py   # Database configuration tests
│   │       │   ├── test_exceptions.py # Exception classes tests
│   │       │   └── test_logging.py    # Logging tests
│   │       ├── models/
│   │       │   └── __init__.py
│   │       ├── schemas/
│   │       │   └── __init__.py
│   │       └── services/
│   │           └── __init__.py
│   └── integration/     # Tests with real components
│       ├── __init__.py
│       └── app/
│           ├── __init__.py
│           ├── api/
│           │   ├── __init__.py
│           │   └── v1/
│           │       └── __init__.py
│           └── test_main.py # Main application and error handling tests
├── requirements.txt     # Production dependencies
├── .env.example        # Environment variables template
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
- **Pydantic-Settings 2.0.3** - Configuration management with environment variable support
- **Pytest 7.4.3** - Testing framework for Python
- **Pytest-Cov 4.1.0** - Coverage plugin for pytest
- **HTTPX 0.25.2** - HTTP client for testing FastAPI applications

All dependencies are pinned to specific versions in `requirements.txt` for reproducible builds.

### Database Configuration

The application uses SQLAlchemy 2.0 for database operations with SQLite as the default database.

#### Database Module Location

Database configuration is located in `app/core/database.py` and includes:

- **Engine**: SQLAlchemy database engine configured for SQLite
- **SessionLocal**: Session factory for creating database sessions
- **Base**: Declarative base class for all database models
- **get_db()**: FastAPI dependency for database session injection

#### Database Settings

Database settings can be configured via environment variables:

| Setting      | Environment Variable | Default              | Description                         |
| ------------ | -------------------- | -------------------- | ----------------------------------- |
| Database URL | `DATABASE_URL`       | `sqlite:///./app.db` | Database connection URL             |
| DB Echo      | `DB_ECHO`            | `false`              | Enable SQLAlchemy SQL query logging |

#### Using the Database in Endpoints

To use the database in FastAPI endpoints, inject the `get_db` dependency:

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # Use the database session
    users = db.query(User).all()
    return users
```

#### Database Connection Features

- **Thread Safety**: Configured with `check_same_thread=False` for SQLite to work with FastAPI's threading model
- **Connection Pre-ping**: Automatically verifies connections before use
- **Automatic Cleanup**: Database sessions are automatically closed after each request
- **Session Management**: Each request gets its own database session

#### Creating Database Models

All database models should inherit from the `Base` class:

```python
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
```

#### SQLAlchemy 2.0 Compatibility

The database configuration uses SQLAlchemy 2.0 features:

- Modern `DeclarativeBase` class for model inheritance
- Type hints for better IDE support
- Proper session lifecycle management
- SQLite-specific optimizations

### Database Migrations with Alembic

The project uses Alembic for database schema migrations with SQLite.

#### Migration Directory Structure

```
backend/
├── alembic/              # Alembic migration directory
│   ├── versions/         # Migration scripts
│   ├── env.py           # Migration environment configuration
│   ├── script.py.mako   # Migration script template
│   └── README           # Alembic documentation
├── alembic.ini          # Alembic configuration file
└── app.db               # SQLite database file (created on first migration)
```

#### Alembic Configuration

- **Database URL**: `sqlite:///./app.db` (relative path in backend directory)
- **Metadata Import**: Configured to import `Base` from `app.core.database` for autogenerate support
- **Migration Tracking**: Uses `alembic_version` table in the database

#### Initial Migration

The initial migration has been created to establish the migration baseline:

- **Migration File**: `alembic/versions/1f08170cdfb3_initial_migration.py`
- **Purpose**: Establishes the Alembic version tracking system
- **Status**: Empty migration (no schema changes yet) - ready for future model additions
- **Alembic Version Table**: Created in database to track migration state

To apply the initial migration (if not already applied):

```bash
alembic upgrade head
```

To verify the current migration status:

```bash
alembic current
# Output: 1f08170cdfb3 (head)
```

#### Basic Alembic Commands

**Check current migration version:**

```bash
alembic current
```

**View migration history:**

```bash
alembic history --verbose
```

**Create a new migration:**

```bash
# Manual migration
alembic revision -m "description of changes"

# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"
```

**Apply migrations:**

```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade by one version
alembic upgrade +1

# Upgrade to specific version
alembic upgrade <revision_id>
```

**Rollback migrations:**

```bash
# Downgrade by one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

#### Migration Best Practices

1. **Always review auto-generated migrations** before applying them
2. **Test migrations in development** before applying to production
3. **Include both upgrade() and downgrade()** functions in all migrations
4. **Never modify applied migrations** - create a new migration instead
5. **Backup database** before running migrations in production

#### Verifying Alembic Installation

After installing dependencies, you can verify Alembic is configured correctly:

```bash
# Check Alembic version
alembic --version

# Verify configuration (should not error)
alembic current

# List migration directory
ls -la alembic/versions/
```

### Database Initialization Script

The project includes an automated database initialization script that simplifies database setup.

#### What the Script Does

The `init_db.py` script automates the entire database initialization process:

1. **Checks database file status** - Reports if the database exists or will be created
2. **Runs all pending migrations** - Applies all Alembic migrations to bring the database up to date
3. **Verifies connection** - Tests the database connection and reports the current migration version
4. **Logs all steps** - Provides detailed logging of the initialization process

#### Usage

**Run as a module (recommended):**

```bash
python -m app.scripts.init_db
```

**Run as a standalone script:**

```bash
python app/scripts/init_db.py
```

**Import and use in Python code:**

```python
from app.scripts.init_db import init_database

# Initialize the database
success = init_database()
if success:
    print("Database initialized successfully!")
else:
    print("Database initialization failed!")
```

#### Features

- **Idempotent**: Safe to run multiple times - won't duplicate data or cause errors
- **Error Handling**: Gracefully handles missing configuration files and connection failures
- **Detailed Logging**: Provides clear feedback about each initialization step
- **Flexible Execution**: Can be run as a module, script, or imported into other code

#### When to Use

- **First-time setup**: Initialize a new development environment
- **After pulling new migrations**: Apply new schema changes from other developers
- **Database reset**: After manually deleting the database file
- **Deployment**: As part of application deployment to ensure database is ready

#### Output Example

```json
{"timestamp": "2025-10-13T18:14:43.830009", "level": "INFO", "message": "============================================================"}
{"timestamp": "2025-10-13T18:14:43.830058", "level": "INFO", "message": "Starting database initialization"}
{"timestamp": "2025-10-13T18:14:43.830077", "level": "INFO", "message": "============================================================"}
{"timestamp": "2025-10-13T18:14:43.830091", "level": "INFO", "message": "Step 1: Checking database file status..."}
{"timestamp": "2025-10-13T18:14:43.830139", "level": "INFO", "message": "Database file will be created at /path/to/app.db"}
{"timestamp": "2025-10-13T18:14:43.830152", "level": "INFO", "message": "Step 2: Running database migrations..."}
{"timestamp": "2025-10-13T18:14:43.830164", "level": "INFO", "message": "Starting database migrations..."}
```

#### Error Handling

The script handles common errors gracefully:

- **Missing alembic.ini**: Reports the expected location and suggests running from the correct directory
- **Database connection failures**: Logs the specific connection error for troubleshooting
- **Migration failures**: Reports migration errors with full stack traces in the logs
- **Unexpected errors**: Catches and logs any unexpected errors to prevent script crashes

#### Testing

Unit tests for the initialization script are located at:

- `tests/unit/app/scripts/test_init_db.py`

Run the tests with:

```bash
python -m pytest tests/unit/app/scripts/test_init_db.py -v
```

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
python -c "import pydantic_settings; print(f'Pydantic-Settings version: {pydantic_settings.__version__}')"
python -c "import pytest; print(f'Pytest version: {pytest.__version__}')"
python -c "import httpx; print(f'HTTPX version: {httpx.__version__}')"
```

### Configuration Management

The application uses Pydantic Settings for configuration management, supporting:

- **Environment variables** - Set via system environment or `.env` file
- **Default values** - Sensible defaults for all settings
- **Validation** - Type checking and constraint validation
- **Case-insensitive** - Environment variable names are case-insensitive

### Logging Configuration

The application includes structured logging with environment-based configuration:

- **Development mode** (`DEBUG=true`): Human-readable format with timestamps
- **Production mode** (`DEBUG=false`): Structured JSON format for log aggregation
- **Configurable log levels**: Set via `LOG_LEVEL` environment variable
- **Logger instances**: Use `get_logger()` to create configured logger instances

Example usage:

```python
from app.core.logging import get_logger

logger = get_logger(__name__)
logger.info("Application started")
logger.error("An error occurred", extra={"user_id": 123})
```

### Error Handling

The application includes a comprehensive global error handling system:

- **Custom Exceptions**: Structured exception hierarchy with consistent HTTP status codes
- **Global Exception Handlers**: Centralized error handling for all API endpoints
- **Consistent Error Format**: All errors return JSON with `detail` and `status_code` fields
- **Proper Logging**: Errors are logged with appropriate levels and request context
- **Security**: Internal errors don't expose sensitive information to clients

#### Available Exception Classes

```python
from app.core.exceptions import (
    BaseAPIException,      # Base class (500 status)
    ValidationException,   # Request validation errors (400 status)
    NotFoundException,     # Resource not found (404 status)
    UnauthorizedException  # Authentication failures (401 status)
)

# Usage example
raise ValidationException("Invalid email format")
raise NotFoundException("User not found")
raise UnauthorizedException("Token expired")
```

#### Error Response Format

All API errors return consistent JSON responses:

```json
{
  "detail": "Error message describing what went wrong",
  "status_code": 400
}
```

For Pydantic validation errors (422 status), detailed field-level information is provided:

```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["field_name"],
      "msg": "Input should be a valid string",
      "input": 123
    }
  ]
}
```

#### Available Settings

| Setting          | Environment Variable     | Default                        | Description                                           |
| ---------------- | ------------------------ | ------------------------------ | ----------------------------------------------------- |
| App Name         | `APP_NAME`               | "Personal Finance Tracker API" | Application name                                      |
| Debug Mode       | `DEBUG`                  | `false`                        | Enable debug mode                                     |
| Log Level        | `LOG_LEVEL`              | `INFO`                         | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| API Prefix       | `API_V1_PREFIX`          | `/api/v1`                      | API version 1 prefix                                  |
| Host             | `HOST`                   | `0.0.0.0`                      | Server host address                                   |
| Port             | `PORT`                   | `8000`                         | Server port (1-65535)                                 |
| CORS Origins     | `CORS_ORIGINS`           | `*`                            | Allowed CORS origins (comma-separated)                |
| CORS Credentials | `CORS_ALLOW_CREDENTIALS` | `true`                         | Allow credentials in CORS                             |
| CORS Methods     | `CORS_ALLOW_METHODS`     | `*`                            | Allowed HTTP methods (comma-separated)                |
| CORS Headers     | `CORS_ALLOW_HEADERS`     | `*`                            | Allowed headers (comma-separated)                     |
| Database URL     | `DATABASE_URL`           | `sqlite:///./app.db`           | Database connection URL (SQLite by default)           |
| DB Echo          | `DB_ECHO`                | `false`                        | Enable SQLAlchemy SQL query logging                   |

#### Configuration Examples

**Development environment:**

```bash
# .env file
DEBUG=true
LOG_LEVEL=DEBUG
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Production environment:**

```bash
# Environment variables
DEBUG=false
LOG_LEVEL=WARNING
PORT=80
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Development Workflow

1. Always activate the virtual environment before working
2. Install new dependencies with `pip install <package>`
3. Update requirements files when adding dependencies
4. Run tests before committing changes
5. Deactivate virtual environment when done

### Running Tests

The project includes comprehensive tests organized into unit and integration tests:

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run only unit tests (fast, isolated tests)
python -m pytest -m unit

# Run only integration tests (tests with real components)
python -m pytest -m integration

# Run tests with coverage
python -m pytest --cov=app --cov-report=term-missing

# Run specific test files
python -m pytest tests/unit/app/core/test_config.py -v
python -m pytest tests/unit/app/core/test_database.py -v
python -m pytest tests/unit/app/core/test_exceptions.py -v
python -m pytest tests/integration/app/test_main.py -v

# Run error handling tests specifically
python -m pytest tests/integration/app/test_main.py::TestErrorHandling -v

# Run tests from a specific directory
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
```

#### Test Organization

- **Unit Tests** (`tests/unit/`): Fast, isolated tests that test individual components without external dependencies
  - `test_config.py` - Configuration management tests
  - `test_database.py` - Database configuration and session management tests
  - `test_exceptions.py` - Custom exception classes tests
  - `test_logging.py` - Logging functionality tests
- **Integration Tests** (`tests/integration/`): Tests that verify multiple components working together, including API endpoints
  - `test_main.py` - FastAPI application tests including error handling
- **Shared Fixtures** (`tests/conftest.py`): Common test fixtures and configuration used across all tests

### API Endpoints

The FastAPI application currently includes:

- **GET /health** - Health check endpoint that returns API status
- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /openapi.json** - OpenAPI specification in JSON format

#### Health Endpoint Response

```json
{
  "status": "healthy",
  "message": "Personal Finance Tracker API is running",
  "version": "0.1.0",
  "debug": false,
  "log_level": "INFO"
}
```

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
- ✅ Basic FastAPI application setup (US0.2-T4)
- ✅ Environment variables management (US0.2-T5)
- ✅ Logging setup (US0.2-T6) - Structured logging with environment-based configuration
- ✅ Error handling (US0.2-T7) - Global exception handlers with consistent error responses
- ✅ Database configuration module (US0.4-T2) - SQLAlchemy engine, session factory, and dependency injection
- ✅ Initial database migration (US0.4-T3) - Alembic migration baseline established
- ✅ Database initialization script (US0.4-T6) - Automated database setup with migration execution and verification

**Upcoming tasks:**

- Continue database setup: health check endpoint, management scripts, backup documentation (US0.4-T4, T5, T7, T8, T9)
- User authentication and authorization (US1.x)

For detailed task breakdown, see: `../backlog/Epic 0: Development Environment & Project Scaffolding/US0.2-backend-development-environment-setup-tasks.md`
