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

4. **Install dependencies** (when available):
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
├── app/                  # Main application code (to be created)
├── tests/                # Test files (to be created)
├── requirements.txt      # Production dependencies (to be created)
├── requirements-dev.txt  # Development dependencies (to be created)
├── .gitignore           # Git ignore patterns
└── README.md            # This file
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

This is the initial setup. The following components will be added in subsequent tasks:
- FastAPI project structure
- Core dependencies installation
- Basic application setup
- Configuration management
- Logging setup
- Error handling
- Development server configuration
- Testing framework setup

For detailed task breakdown, see: `../backlog/Epic 0: Development Environment & Project Scaffolding/US0.2-backend-development-environment-setup-tasks.md`
