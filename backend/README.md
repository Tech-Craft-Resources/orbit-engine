# FastAPI Project - Backend

## Requirements

* [Docker](https://www.docker.com/)
* [uv](https://docs.astral.sh/uv/) for Python package and environment management

## Development with Docker Compose (Recommended)

Start the full stack with Docker Compose from the project root:

```bash
# First time or after changing Dockerfiles
docker compose build

# Start services
docker compose up -d
```

The backend runs with **automatic hot-reload** thanks to:
- Volume mounting configured in `compose.override.yml` (syncs `./backend` to container)
- Command override: `fastapi run --reload app/main.py`

Changes to Python files are detected automatically and the server reloads instantly.

### When to restart the backend container:

- ✅ **NO need to restart** when changing Python code (auto-reload enabled)
- ⚠️ **YES, restart required** when installing/updating/removing dependencies:
  ```bash
  docker compose restart backend
  ```

### View logs in real-time:

```bash
docker compose logs -f backend
```

### Accessing the backend container:

```bash
docker compose exec backend bash
```

### Available endpoints:

- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/v1/utils/health-check/

## Local Development (without Docker)

If you prefer to run the backend locally without Docker:

```bash
cd backend

# Install uv if not already installed
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run migrations (requires database running)
alembic upgrade head

# Start development server with hot-reload
uv run fastapi dev app/main.py
```

**Note:** You'll still need the database running. You can start only the database with:
```bash
docker compose up db -d
```

## Code Structure

- `app/api/` - API endpoints organized by domain
- `app/api/deps.py` - Dependency injection (database session, current user, etc.)
- `app/core/` - Core configuration (settings, security, database)
- `app/models.py` - SQLModel models (database tables + Pydantic schemas)
- `app/crud.py` - Database CRUD operations
- `app/alembic/` - Database migrations
- `tests/` - Pytest tests

## Backend Tests

### Run all tests with coverage:

```bash
# From backend directory
uv run bash scripts/test.sh
```

### Run specific tests:

```bash
# Single test file
uv run pytest tests/api/routes/test_users.py -v

# Single test function
uv run pytest tests/api/routes/test_users.py::test_get_users_superuser_me -v

# Tests matching a pattern
uv run pytest -k "test_create" -v
```

### Run tests inside Docker:

```bash
# From project root
docker compose exec backend bash scripts/test.sh

# Or with specific pytest options
docker compose exec backend bash scripts/tests-start.sh -x  # stop on first error
```

### Test Coverage

After running tests, open `htmlcov/index.html` in your browser to see detailed coverage reports.

## Migrations

Database migrations are managed with Alembic. Always run migrations inside the Docker container to ensure proper database connectivity.

### Create a new migration:

```bash
docker compose exec backend alembic revision --autogenerate -m "Add column last_name to User model"
```

### Apply migrations:

```bash
docker compose exec backend alembic upgrade head
```

### Rollback last migration:

```bash
docker compose exec backend alembic downgrade -1
```

### Migration workflow:

1. Modify models in `app/models.py`
2. Create migration: `docker compose exec backend alembic revision --autogenerate -m "description"`
3. Review generated migration file in `app/alembic/versions/`
4. Apply migration: `docker compose exec backend alembic upgrade head`
5. Commit both `models.py` and migration files to git

**Important:** Alembic is configured to import models from `app/models.py`. Make sure all your SQLModel models are defined there.

## Code Quality

### Linting:

```bash
uv run bash scripts/lint.sh
```

This runs:
- `ruff check` - Fast Python linter
- `mypy` - Static type checker

### Formatting:

```bash
uv run bash scripts/format.sh
```

This runs `ruff format` to auto-format code.

## VS Code Setup

The project includes VS Code configurations for:
- Running backend through the debugger with breakpoints
- Running tests through the Python tests tab
- Python interpreter set to `backend/.venv/bin/python`

Make sure your editor is using the correct Python virtual environment.

## Email Templates

Email templates are in `app/email-templates/`:
- `src/` - Source MJML files (editable)
- `build/` - Compiled HTML files (used by the app)

To edit email templates:
1. Install [MJML extension](https://github.com/mjmlio/vscode-mjml) for VS Code
2. Edit `.mjml` files in `src/`
3. Use `Ctrl+Shift+P` → "MJML: Export to HTML"
4. Save compiled `.html` file to `build/`

## Environment Variables

Key environment variables (set in root `.env` file):

```env
# Database
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app

# Security
SECRET_KEY=your-secret-key-change-in-production

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost"]

# Email (development with mailcatcher)
SMTP_HOST=mailcatcher
SMTP_PORT=1025
SMTP_TLS=false
EMAILS_FROM_EMAIL=noreply@example.com
```

See `.env.example` in project root for complete list.
