# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**StreamlitTurbo PRO** is a production-ready Streamlit template with enterprise features including authentication, database, monitoring, and CI/CD. The project uses modern Python tooling (`uv`, `just`, `ruff`) and follows professional software engineering practices.

## Development Commands

**IMPORTANT:** This project uses `just` as a task runner. All commands below are available via `just`. Run `just help` to see all available commands.

### Setup and Installation
```bash
# Complete project setup (recommended)
just setup

# Manual setup
uv venv --python 3.12
uv sync
uv sync --group dev
pre-commit install
```

### Running the Application
```bash
# Production mode
just run

# Development mode (auto-reload)
just dev

# Manual
uv run streamlit run main.py
```

### Code Quality
```bash
# Format code with Ruff
just format

# Lint with Ruff
just lint

# Format + Lint combo
just check

# Type checking with mypy
just typecheck

# Pre-commit hooks on all files
just pre-commit
```

### Testing
```bash
# All tests
just test

# With coverage (generates HTML report)
just test-cov

# Unit tests only
just test-unit

# Integration tests only
just test-integration

# Specific test file
uv run pytest tests/unit/test_auth.py -v
```

### Database (Alembic Migrations)
```bash
# Create new migration
just db-migrate "description"

# Apply migrations
just db-upgrade

# Rollback last migration
just db-downgrade

# View migration history
just db-history
```

### Docker
```bash
# Build Docker image
just docker-build

# Start full stack (App + PostgreSQL + Adminer)
just docker-up

# Stop containers
just docker-down

# View logs
just docker-logs
```

### Dependencies
```bash
# Add production dependency
just add plotly

# Add dev dependency
just add-dev pytest-mock

# Sync dependencies
just sync

# Generate requirements.txt for deployment
just requirements
```

## Architecture

### Application Structure

**Modern Navigation:** Uses `st.navigation()` with `position="top"` (NO sidebar). All pages are defined in `main.py` using `st.Page()`.

**Key directories:**
- `src/streamlit_template/` - All application code
- `src/streamlit_template/pages/` - Page modules (loaded by st.navigation)
- `tests/` - Test suite (unit + integration)
- `.github/workflows/` - CI/CD pipelines
- `docker/` - Docker configuration

### Key Architectural Patterns

#### 1. **Authentication** (`src/streamlit_template/auth/`)

Uses Streamlit's native Google OAuth (`st.login()`, `st.user`):

- **session.py**: Session management
  - `is_authenticated()`: Check if user is logged in
  - `get_current_user()`: Get user info dict
  - `get_user_role()`: Returns 'admin', 'user', or 'anonymous'
  - `logout_user()`: Calls `st.logout()`
  - Admin emails configured in `st.secrets["admin_emails"]`

- **decorators.py**: Protection decorators
  - `@require_auth`: Requires authentication, shows login button if not authenticated
  - `@require_role(['admin'])`: Requires specific role(s)
  - `@public_page`: Marks a page as public (documentation only)

**Usage example:**
```python
from streamlit_template.auth import require_auth, require_role

@require_auth
def protected_page():
    st.write("Only authenticated users see this")

@require_role(['admin'])
def admin_page():
    st.write("Only admins see this")
```

#### 2. **Database** (`src/streamlit_template/database/`)

SQLModel ORM with Alembic migrations:

- **models.py**: SQLModel models
  - `User`: User profiles (email, google_sub, role, etc.)
  - `ActivityLog`: User actions tracking
  - `DataEntry`: Example business model

- **engine.py**: Database connection
  - `get_database_url()`: Gets URL from secrets (SQLite dev, PostgreSQL prod)
  - `get_engine()`: Singleton engine instance
  - `get_session()`: Generator for DB sessions
  - `init_db()`: Creates all tables (call at startup)

- **migrations/**: Alembic configuration
  - Auto-configured to read from `secrets.toml`
  - Use `just db-migrate "message"` to create migrations
  - Use `just db-upgrade` to apply

**Usage example:**
```python
from streamlit_template.database import get_session, User
from sqlmodel import select

with next(get_session()) as session:
    statement = select(User).where(User.email == "test@example.com")
    user = session.exec(statement).first()
```

#### 3. **Monitoring** (`src/streamlit_template/monitoring/`)

Structured logging and analytics:

- **logger.py**: Structured logging with structlog
  - `get_logger(name)`: Get a structured logger
  - `log_event(event, **kwargs)`: Log with context
  - Outputs JSON in production, colored console in dev

- **analytics.py**: User analytics
  - `track_page_view(page_name)`: Track page visits
  - `track_action(action, details, page)`: Track user actions
  - `get_user_stats(email)`: Get user statistics
  - `get_app_stats()`: Get global statistics
  - Only saves to DB if `secrets["monitoring"]["enable_analytics"]` is True

**Usage example:**
```python
from streamlit_template.monitoring import track_page_view, track_action

# At top of page
track_page_view("analytics")

# On user action
if st.button("Export"):
    track_action("export_csv", details={"format": "csv"}, page="analytics")
```

#### 4. **Components** (`src/streamlit_template/components/`)

Reusable UI components:

- **charts.py**: Plotly chart functions
  - `create_line_chart()`, `create_bar_chart()`, `create_pie_chart()`
  - `create_scatter_plot()`, `create_heatmap()`, `create_gauge_chart()`
  - `generate_sample_data(type)`: Generate demo data
  - All use `use_container_width=True` for responsive design

- **header.py, footer.py**: Layout components
  - `render_header(title, subtitle)`
  - `render_footer()`

#### 5. **Page Structure**

All pages follow this pattern:

```python
"""
Page Description - StreamlitTurbo PRO
"""
import streamlit as st
from streamlit_template.auth import require_auth
from streamlit_template.monitoring import track_page_view
from streamlit_template.components import render_header, render_footer

# Track page view
track_page_view("page_name")

# Header
render_header("Title", "Subtitle")

# Page content (with auth if needed)
@require_auth
def render_content():
    st.write("Protected content")

render_content()

# Footer
render_footer()
```

**Available pages:**
- `home.py`: Public welcome + authenticated dashboard
- `analytics.py`: Charts and KPIs (auth required)
- `settings.py`: User preferences (auth required)
- `admin.py`: Admin panel (admin role required)

#### 6. **Configuration**

- **Streamlit config**: `.streamlit/config.toml`
  - 4 professional themes (blue, dark, light, green)
  - Server settings (runOnSave, max upload, etc.)

- **Secrets**: `.streamlit/secrets.toml` (NEVER commit!)
  - Google OAuth credentials
  - Database URLs
  - Admin email list
  - Monitoring config
  - See `.streamlit/secrets.toml.example` for template

#### 7. **Testing**

- `tests/conftest.py`: Shared fixtures (mock secrets, sample users, etc.)
- `tests/unit/`: Unit tests for auth, database, monitoring
- `tests/integration/`: Integration tests for pages
- Run with `just test` or `just test-cov`

## Important Notes

### General
- **Language**: French (UI text and comments)
- **Python**: 3.12+ required
- **Line length**: 100 characters (Ruff configured)
- **Layout**: Wide by default, sidebar collapsed (navigation in top bar)
- **Package manager**: `uv` (ultra-fast)
- **Task runner**: `just` (25+ commands)

### Authentication
- Uses Streamlit's native `st.login()` (requires `streamlit[auth]>=1.40.0`)
- Requires `.streamlit/secrets.toml` with Google OAuth credentials
- Admin role determined by email list in `secrets["admin_emails"]`
- Token expiration is NOT checked automatically (see `check_token_expiration()`)

### Database
- SQLite by default (dev), PostgreSQL for production
- Migrations managed with Alembic
- `init_db()` is called in `main.py` at startup
- Connection pooling handled by SQLModel/SQLAlchemy

### Monitoring
- Analytics only saved to DB if enabled in secrets
- Logs output to console (JSON in prod, colored in dev)
- Errors logged but don't block the app

### CI/CD
- GitHub Actions runs on push/PR to main/develop
- Tests must pass before merge
- Deploy workflow auto-generates requirements.txt
- Streamlit Cloud auto-deploys from main branch

### Docker
- Production Dockerfile uses Python 3.12-slim
- docker-compose includes PostgreSQL + Adminer
- Healthchecks configured for all services
- Volume mounted for data persistence

### Security
- NEVER commit `.streamlit/secrets.toml`
- Pre-commit hooks include bandit security checks
- Secrets are in `.gitignore`
- XSRF protection enabled in Streamlit config

### Development Workflow
1. Create feature branch from `develop`
2. Make changes, run `just check` and `just test`
3. Commit (pre-commit hooks run automatically)
4. Push (CI runs on GitHub)
5. Create PR to `develop` (tests must pass)
6. Merge to `develop`, then to `main` for deploy

### Common Patterns

**Adding a new page:**
1. Create `src/streamlit_template/pages/my_page.py`
2. Add to `main.py` pages list: `st.Page("src/streamlit_template/pages/my_page.py", ...)`
3. Use decorators for auth: `@require_auth` or `@require_role(['admin'])`
4. Add tracking: `track_page_view("my_page")`

**Adding a database model:**
1. Add model to `src/streamlit_template/database/models.py`
2. Create migration: `just db-migrate "add my_model"`
3. Apply migration: `just db-upgrade`

**Adding tests:**
1. Create test file in `tests/unit/` or `tests/integration/`
2. Use fixtures from `conftest.py`
3. Run: `just test-unit` or `just test-integration`

### Troubleshooting

**Auth not working:**
- Check `.streamlit/secrets.toml` exists and has correct Google credentials
- Verify `redirect_uri` matches your app URL
- Check Google Cloud Console OAuth configuration

**Database errors:**
- Run `just db-upgrade` to apply migrations
- Check database URL in secrets.toml
- For SQLite, ensure `data/` directory exists

**Import errors:**
- `main.py` adds `src/` to `sys.path`
- Use: `from streamlit_template.module import ...`
- Not: `from src.streamlit_template.module import ...`

**Tests failing:**
- Ensure fixtures mock Streamlit properly
- Check `conftest.py` for available fixtures
- Use `mock_streamlit_secrets` fixture for secrets

### File Naming Conventions
- Python files: `snake_case.py`
- Test files: `test_*.py`
- Modules: Short, descriptive names
- Pages: No prefixes (handled by st.navigation order)
