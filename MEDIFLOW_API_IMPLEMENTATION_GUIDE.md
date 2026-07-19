# MediFlow REST API - Complete Implementation Guide

## Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/mediflow/api.git
cd mediflow-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r mediflow_api_requirements.txt

# Create .env file
cp .env.example .env
```

### 2. Configure Environment Variables

```env
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/mediflow
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=1
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# External Services
OPENAI_API_KEY=sk-...
GOOGLE_CLOUD_VISION_KEY=path/to/key.json
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=mediflow-documents

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://mediflow.com

# Logging
LOG_LEVEL=INFO
```

### 3. Initialize Database

```bash
# Create PostgreSQL database
createdb mediflow

# Run migrations
alembic upgrade head

# Load initial data
python scripts/load_seed_data.py
```

### 4. Run Application

```bash
# Development
uvicorn mediflow_api_implementation:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn mediflow_api_implementation:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### 5. Access API Documentation

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI spec: http://localhost:8000/api/openapi.json

---

## API Usage Examples

### Authentication

#### Register New User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe",
    "date_of_birth": "1965-05-15",
    "phone": "+14155550100",
    "role": "PATIENT"
  }'
```

#### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "SecurePass123!"
  }'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

#### Refresh Token

```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### Patient APIs

#### Get Patient Profile

```bash
curl -X GET http://localhost:8000/api/patients/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer <access_token>"
```

#### Update Patient Profile

```bash
curl -X PUT http://localhost:8000/api/patients/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "phone": "+14155550100",
    "preferences": {
      "communication_preference": "EMAIL"
    }
  }'
```

#### Add Allergy

```bash
curl -X POST http://localhost:8000/api/patients/550e8400-e29b-41d4-a716-446655440000/allergies \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "allergen": "Penicillin",
    "severity": "SEVERE",
    "reaction": "Anaphylaxis"
  }'
```

### Medication APIs

#### Get Patient Medications

```bash
curl -X GET "http://localhost:8000/api/patients/550e8400-e29b-41d4-a716-446655440000/medications?include_inactive=false" \
  -H "Authorization: Bearer <access_token>"
```

#### Add Medication

```bash
curl -X POST http://localhost:8000/api/patients/550e8400-e29b-41d4-a716-446655440000/medications \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "drug_name": "Lisinopril",
    "strength": "10mg",
    "frequency": "ONCE_DAILY",
    "start_date": "2024-01-15",
    "indication": "Hypertension"
  }'
```

#### Check Drug Interactions

```bash
curl -X POST http://localhost:8000/api/medications/check-interactions \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "primary_drug": "Lisinopril",
    "query_medication": "Potassium supplement",
    "include_supplements": true
  }'
```

### Appointment APIs

#### Get Appointments

```bash
curl -X GET "http://localhost:8000/api/appointments?patient_id=550e8400-e29b-41d4-a716-446655440000&status=SCHEDULED" \
  -H "Authorization: Bearer <access_token>"
```

#### Schedule Appointment

```bash
curl -X POST http://localhost:8000/api/appointments \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "550e8400-e29b-41d4-a716-446655440001",
    "appointment_date": "2024-01-20",
    "appointment_time": "14:00",
    "chief_complaint": "Blood pressure check"
  }'
```

### Document APIs

#### Upload Document

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@prescription.pdf" \
  -F "document_type=PRESCRIPTION" \
  -F "patient_id=550e8400-e29b-41d4-a716-446655440000"
```

#### Get Document Status

```bash
curl -X GET http://localhost:8000/api/documents/doc-789/status \
  -H "Authorization: Bearer <access_token>"
```

### Timeline APIs

#### Get Patient Timeline

```bash
curl -X GET "http://localhost:8000/api/patients/550e8400-e29b-41d4-a716-446655440000/timeline?limit=50" \
  -H "Authorization: Bearer <access_token>"
```

### Analytics APIs

#### Get Health Summary

```bash
curl -X GET http://localhost:8000/api/patients/550e8400-e29b-41d4-a716-446655440000/analytics/health-summary \
  -H "Authorization: Bearer <access_token>"
```

---

## Database Operations

### Create Tables

```bash
# Using SQLAlchemy ORM
python -c "from mediflow_api_implementation import Base, engine; Base.metadata.create_all(engine)"
```

### Seed Database

```bash
python scripts/load_seed_data.py
```

### Backup Database

```bash
pg_dump mediflow > backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
psql mediflow < backup_20240115.sql
```

---

## Testing

### Run Unit Tests

```bash
pytest tests/ -v
```

### Run Integration Tests

```bash
pytest tests/integration/ -v
```

### Test Coverage

```bash
pytest --cov=mediflow_api_implementation tests/
```

### Test Specific Endpoint

```bash
pytest tests/test_auth.py::test_login -v
```

---

## Deployment

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY mediflow_api_requirements.txt .
RUN pip install -r mediflow_api_requirements.txt

COPY mediflow_api_implementation.py .
COPY .env .

CMD ["uvicorn", "mediflow_api_implementation:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://mediflow:password@db:5432/mediflow
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mediflow
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mediflow-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mediflow-api
  template:
    metadata:
      labels:
        app: mediflow-api
    spec:
      containers:
      - name: api
        image: mediflow/api:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: mediflow-secrets
              key: database-url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

---

## Monitoring & Logging

### Health Check

```bash
curl http://localhost:8000/api/health
```

### API Metrics (Prometheus)

```bash
curl http://localhost:8000/api/metrics
```

### View Logs

```bash
# Docker
docker logs mediflow-api

# Kubernetes
kubectl logs deployment/mediflow-api

# System logs
tail -f /var/log/mediflow/api.log
```

---

## Security Best Practices

1. **Never commit .env file** - Use .gitignore
2. **Use HTTPS in production** - Set up SSL certificates
3. **Rotate secrets regularly** - Change SECRET_KEY, API keys
4. **Rate limiting** - Enabled by default (1000 req/hour)
5. **Input validation** - All endpoints validate inputs
6. **CORS configuration** - Whitelist trusted origins
7. **SQL injection prevention** - Using ORM (SQLAlchemy)
8. **XSS prevention** - Input sanitization
9. **Audit logging** - All actions logged

---

## Performance Tuning

### Database Optimization

```sql
-- Create indexes on frequently queried columns
CREATE INDEX idx_patients_email ON patients(email);
CREATE INDEX idx_medications_patient_id ON medications(patient_id);
CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);
```

### Caching Strategy

```python
# Cache frequently accessed data
# - Patient profiles: 1 hour TTL
# - Medication lists: 30 minutes TTL
# - Drug interactions: 24 hours TTL
```

### Connection Pooling

```python
# SQLAlchemy pool configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Database Connection Error

```bash
# Test connection
psql -h localhost -U mediflow -d mediflow

# Check credentials in .env
cat .env | grep DATABASE_URL
```

### JWT Token Expired

```bash
# Use refresh endpoint to get new token
POST /api/auth/refresh
```

### Rate Limit Exceeded

```bash
# Wait for reset (check X-RateLimit-Reset header)
# Or use higher tier account
```

---

## API Versioning

Current version: **v1.0.0**

Future versions will maintain backward compatibility at `/api/v1/`.

---

## Support & Documentation

- **Swagger UI:** http://localhost:8000/api/docs
- **OpenAPI Spec:** http://localhost:8000/api/openapi.json
- **Email:** api-support@mediflow.com
- **GitHub Issues:** https://github.com/mediflow/api/issues

---

## License

Proprietary - MediFlow Healthcare Platform

All rights reserved © 2024 MediFlow Inc.
