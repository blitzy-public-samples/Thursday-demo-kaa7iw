# Code Generation Web Application Backend

## Human Tasks
- [ ] Configure Google Cloud Project and enable required APIs (User Store, SQL, Redis)
- [ ] Set up PostgreSQL 14+ instance in Cloud SQL
- [ ] Set up Redis 6+ instance in Cloud Memorystore
- [ ] Configure environment variables in .env file
- [ ] Set up monitoring stack (Prometheus/Grafana)
- [ ] Configure SSL certificates for domain
- [ ] Set up backup retention policy in GCP
- [ ] Configure firewall rules for database access

## Overview
The Code Generation Web Application backend is a RESTful service built with Python and Flask, providing the core functionality for managing projects, specifications, and bullet items. The service integrates with Google Cloud User Store for authentication and uses PostgreSQL for data persistence.

## Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Docker 20.10+
- Google Cloud SDK
- kubectl

## Installation

### Local Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd src/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment files
cp .env.example .env
cp .flaskenv.example .flaskenv

# Initialize database
flask db upgrade

# Run development server
flask run
```

### Docker Setup
```bash
# Build container
docker build -f docker/Dockerfile -t codegenapp-backend .

# Run with Docker Compose
docker-compose -f docker/docker-compose.yml up -d
```

## Configuration

### Environment Variables
```ini
# Application
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=<your-secret-key>

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/codegenapp
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=10

# Google Cloud
GOOGLE_CLOUD_PROJECT=<project-id>
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Security
JWT_SECRET_KEY=<jwt-secret-key>
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# Rate Limiting
RATELIMIT_DEFAULT=100/minute
RATELIMIT_STORAGE_URL=redis://localhost:6379/1
```

## Development

### Code Structure
```
src/backend/
├── app/
│   ├── api/            # API endpoints
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── utils/          # Utilities
│   ├── middleware/     # Custom middleware
│   ├── cache/          # Caching logic
│   └── database/       # Database configuration
├── tests/             # Test suite
├── docker/            # Docker configuration
└── scripts/           # Utility scripts
```

### Coding Standards
- Follow PEP 8 style guide
- Use type hints for all function parameters and returns
- Write docstrings for all public modules, functions, classes, and methods
- Maintain test coverage above 80%
- Use black for code formatting
- Use isort for import sorting

### Testing
```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run linting
flake8 app tests
```

## API Documentation

### Authentication
- POST `/api/v1/auth/login` - Login with Google credentials
- POST `/api/v1/auth/logout` - Logout user
- POST `/api/v1/auth/refresh` - Refresh JWT token

### Projects
- GET `/api/v1/projects` - List user's projects
- POST `/api/v1/projects` - Create new project
- GET `/api/v1/projects/{id}` - Get project details
- PUT `/api/v1/projects/{id}` - Update project
- DELETE `/api/v1/projects/{id}` - Delete project

### Specifications
- GET `/api/v1/projects/{id}/specs` - List specifications
- POST `/api/v1/projects/{id}/specs` - Create specification
- GET `/api/v1/specs/{id}` - Get specification
- PUT `/api/v1/specs/{id}` - Update specification
- DELETE `/api/v1/specs/{id}` - Delete specification

### Bullet Items
- GET `/api/v1/specs/{id}/items` - List bullet items
- POST `/api/v1/specs/{id}/items` - Create bullet item
- PUT `/api/v1/items/{id}` - Update bullet item
- DELETE `/api/v1/items/{id}` - Delete bullet item
- PUT `/api/v1/specs/{id}/items/reorder` - Reorder items

## Database

### Schema Overview
- users: User authentication and profile data
- projects: User-owned projects
- specifications: Project specifications
- bullet_items: Ordered specification items

### Migrations
```bash
# Create migration
flask db migrate -m "description"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## Deployment

### Staging Deployment
```bash
# Deploy to staging
kubectl apply -k infrastructure/kubernetes/overlays/staging

# Verify deployment
kubectl get pods -n staging
```

### Production Deployment
```bash
# Deploy to production
kubectl apply -k infrastructure/kubernetes/overlays/prod

# Scale deployment
kubectl scale deployment backend -n prod --replicas=5
```

## Monitoring

### Health Checks
- GET `/health` - Application health status
- GET `/health/db` - Database connection status
- GET `/health/redis` - Redis connection status

### Metrics
- Prometheus metrics available at `/metrics`
- Custom metrics:
  - request_duration_seconds
  - active_users_total
  - database_connections_active
  - cache_hit_ratio

### Logging
- Application logs sent to Cloud Logging
- Structured JSON logging format
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Security

### Authentication
- Google OAuth 2.0 authentication
- JWT tokens for session management
- Refresh token rotation
- Token blacklisting for logout

### Authorization
- Role-based access control
- Resource ownership validation
- Row-level security in database

### Security Headers
- HTTPS enforced
- CORS configuration
- CSP headers
- XSS protection
- CSRF protection

## Troubleshooting

### Common Issues
1. Database Connection Errors
   - Verify database credentials
   - Check network connectivity
   - Validate connection pool settings

2. Authentication Issues
   - Verify Google Cloud credentials
   - Check token expiration
   - Validate client configuration

3. Performance Issues
   - Monitor database query performance
   - Check Redis cache hit ratio
   - Review application logs
   - Analyze metrics dashboard

### Support
For technical support:
1. Check application logs
2. Review monitoring dashboards
3. Contact DevOps team
4. Create GitHub issue

## Last Update
Date: 2024-01-20
Version: 1.0.0

## Version History
- 1.0.0 (2024-01-20): Initial release
- 0.9.0 (2023-12-15): Beta release
- 0.5.0 (2023-11-01): Alpha release

## Contributor Guidelines
1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Add tests for new features
5. Update documentation
6. Submit pull request