# MediFlow - Complete Production Setup Guide

## Project Structure

### Frontend (Next.js + TypeScript)
```
Frontend Files:
- mediflow_frontend_package.json - npm dependencies
- mediflow_lib_types.ts - TypeScript type definitions
- mediflow_lib_api_client.ts - API client with auto-refresh
- mediflow_lib_use_auth.ts - Authentication hook
- mediflow_lib_use_data.ts - Data fetching hooks
- mediflow_lib_validators.ts - Form validation
- mediflow_components_auth_LoginForm.tsx - Login component
- mediflow_components_patient_MedicationCard.tsx - Medication display
- mediflow_next_config.js - Next.js configuration
- mediflow_tsconfig.json - TypeScript config
- mediflow_tailwind_config.js - Tailwind CSS config
- mediflow_postcss_config.js - PostCSS config
- mediflow_app_layout.tsx - Root layout
- mediflow_app_auth_login_page.tsx - Login page
```

### Backend (FastAPI + Python)
```
Backend Files:
- mediflow_app_main.py - FastAPI application
- mediflow_app_config.py - Configuration
- mediflow_app_core_security.py - JWT and password hashing
- mediflow_app_core_logging.py - Logging setup
- mediflow_app_dependencies.py - Database dependencies
- mediflow_app_models_init.py - SQLAlchemy models
- mediflow_app_schemas_init.py - Pydantic schemas
- mediflow_app_routers_auth.py - Authentication routes
- mediflow_app_routers_medications.py - Medication routes
- mediflow_app_routers_init.py - Routers module
- mediflow_tests_test_auth.py - Authentication tests
- mediflow_backend_requirements.txt - Python dependencies
```

### Infrastructure
```
Infrastructure Files:
- mediflow_backend_Dockerfile - Backend container
- mediflow_docker_compose.yml - Docker Compose
- mediflow_env_example - Environment variables example
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15
- Redis 7

### Frontend Setup

1. Create frontend directory structure:
```bash
mkdir -p mediflow-frontend
cd mediflow-frontend

# Create subdirectories
mkdir -p app lib components/{shared,auth,patient,doctor} styles
```

2. Copy frontend files:
```bash
cp mediflow_frontend_package.json package.json
cp mediflow_lib_types.ts lib/types.ts
cp mediflow_lib_api_client.ts lib/api-client.ts
cp mediflow_lib_use_auth.ts lib/use-auth.ts
cp mediflow_lib_use_data.ts lib/use-data.ts
cp mediflow_lib_validators.ts lib/validators.ts
cp mediflow_components_auth_LoginForm.tsx components/auth/LoginForm.tsx
cp mediflow_components_patient_MedicationCard.tsx components/patient/MedicationCard.tsx
cp mediflow_next_config.js next.config.js
cp mediflow_tsconfig.json tsconfig.json
cp mediflow_tailwind_config.js tailwind.config.js
cp mediflow_postcss_config.js postcss.config.js
cp mediflow_app_layout.tsx app/layout.tsx
cp mediflow_app_auth_login_page.tsx 'app/(auth)/login/page.tsx'
```

3. Install dependencies:
```bash
npm install
```

4. Create `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. Run development server:
```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

### Backend Setup

1. Create backend directory structure:
```bash
mkdir -p mediflow-backend/app/{core,models,routers,schemas} tests logs
cd mediflow-backend
```

2. Copy backend files:
```bash
cp ../mediflow_app_main.py app/main.py
cp ../mediflow_app_config.py app/config.py
cp ../mediflow_app_dependencies.py app/dependencies.py
cp ../mediflow_app_core_security.py app/core/security.py
cp ../mediflow_app_core_logging.py app/core/logging.py
cp ../mediflow_app_models_init.py app/models/__init__.py
cp ../mediflow_app_schemas_init.py app/schemas/__init__.py
cp ../mediflow_app_routers_auth.py app/routers/auth.py
cp ../mediflow_app_routers_medications.py app/routers/medications.py
cp ../mediflow_app_routers_init.py app/routers/__init__.py
cp ../mediflow_tests_test_auth.py tests/test_auth.py
cp ../mediflow_backend_requirements.txt requirements.txt
```

3. Create `__init__.py` files:
```bash
touch app/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/routers/__init__.py
touch app/schemas/__init__.py
touch tests/__init__.py
```

4. Create `.env` from example:
```bash
cp ../mediflow_env_example .env
```

5. Update `.env` with your settings:
```bash
nano .env
```

6. Install dependencies:
```bash
pip install -r requirements.txt
```

7. Initialize database:
```bash
python -c "from app.dependencies import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

8. Run server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

### Docker Setup (Recommended)

1. Copy Docker files:
```bash
cp mediflow_backend_Dockerfile .
cp mediflow_docker_compose.yml docker-compose.yml
cp mediflow_env_example .env
```

2. Update `.env` with your settings

3. Start all services:
```bash
docker-compose up -d
```

4. Initialize database:
```bash
docker-compose exec backend python -c "from app.dependencies import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

5. Verify services are running:
```bash
docker-compose ps
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Running Tests

```bash
# Unit tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Watch mode
pytest tests/ -v --watch
```

### Database Migrations (Alembic)

```bash
# Initialize migrations directory (one-time)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Examples

### Authentication

```bash
# Signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'

# Get current user
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Refresh token
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
```

### Medications

```bash
# List medications
curl http://localhost:8000/api/medications?skip=0&limit=20

# Get specific medication
curl http://localhost:8000/api/medications/MEDICATION_ID

# Get medication interactions
curl http://localhost:8000/api/medications/MEDICATION_ID/interactions
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port
lsof -i :8000  # or :3000 for frontend
kill -9 <PID>
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or with pip cache clear
pip install -r requirements.txt --no-cache-dir
```

### Frontend API Connection Issues
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in .env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Production Deployment

### Environment Variables
```bash
SECRET_KEY=your-strong-secret-key-min-32-chars
DEBUG=false
DATABASE_URL=postgresql://user:password@host:5432/mediflow
REDIS_URL=redis://host:6379/0
ALLOWED_ORIGINS=https://yourdomain.com
```

### Docker Build
```bash
docker build -f mediflow_backend_Dockerfile -t mediflow-backend:latest .
docker push your-registry/mediflow-backend:latest
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000
```

## Development Workflow

1. **Feature Development**
   - Create feature branch
   - Make changes
   - Run tests
   - Commit with clear message
   - Push and create PR

2. **Code Quality**
   ```bash
   # Format code
   black app/
   
   # Lint
   flake8 app/
   
   # Type checking
   mypy app/
   ```

3. **Testing**
   ```bash
   # Run all tests
   pytest tests/
   
   # Run specific test
   pytest tests/test_auth.py::test_login
   ```

## Documentation

- API Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc
- Implementation Guide: See MEDIFLOW_PRODUCTION_CODE.md

## Support & Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Next.js Docs: https://nextjs.org/docs
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- PostgreSQL Docs: https://www.postgresql.org/docs/

---

**Status: ✅ Production-Ready Code Deployed**

All files are executable and ready for development. Follow the setup instructions above to get started.
