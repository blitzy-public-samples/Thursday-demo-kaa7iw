# Code Generation Web Application

A comprehensive RESTful backend service built with Python and Flask for automated codebase generation from requirement specifications.

## Human Tasks
- [ ] Configure Google Cloud User Store credentials in .env file
- [ ] Set up PostgreSQL database and update connection string
- [ ] Configure Redis instance and update connection details
- [ ] Set up monitoring credentials for Prometheus/Grafana
- [ ] Review and update rate limiting configurations
- [ ] Configure backup retention policies
- [ ] Set up SSL certificates for production deployment

## Introduction

The Code Generation Web Application is a robust backend service that automates the process of generating codebase from requirement specifications. Built with a layered architecture, it provides secure, scalable, and maintainable API endpoints for managing projects, specifications, and code generation.

### System Architecture

- API Layer: RESTful endpoints for HTTP request/response handling
- Authentication Layer: Google Cloud User Store integration
- Business Logic Layer: Core project and specification management
- Data Access Layer: PostgreSQL database operations
- Code Generation Layer: Automated codebase generation

## Technology Stack

### Core Technologies
- Python 3.9+
- Flask 2.0+
- PostgreSQL 14+
- Redis 6+
- Google Cloud User Store

### Additional Components
- Docker & Kubernetes for containerization
- Prometheus & Grafana for monitoring
- ELK Stack for logging
- NGINX for load balancing

## Prerequisites

Ensure you have the following installed:
- Python 3.9 or higher
- Docker and Docker Compose
- PostgreSQL 14+
- Redis 6+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd code-generation-webapp
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r src/backend/requirements.txt
```

4. Set up environment variables:
```bash
cp src/backend/.env.example src/backend/.env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
cd src/backend
./scripts/migrate.sh
```

## Configuration

### Environment Variables
```ini
# Application
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=<your-secret-key>

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Google Cloud
GOOGLE_CLIENT_ID=<your-client-id>
GOOGLE_CLIENT_SECRET=<your-client-secret>

# Security
JWT_SECRET_KEY=<your-jwt-secret>
JWT_ACCESS_TOKEN_EXPIRES=3600
```

## Development

### Running Locally
```bash
cd src/backend
./scripts/run.sh
```

### Development Guidelines
- Follow PEP 8 style guide
- Write unit tests for new features
- Update API documentation for endpoint changes
- Use type hints and docstrings
- Commit messages should follow conventional commits

### Testing
```bash
pytest src/backend/tests
```

## API Documentation

### Authentication
- POST /api/v1/auth/login - Login with Google
- POST /api/v1/auth/logout - Logout user
- POST /api/v1/auth/refresh - Refresh JWT token

### Projects
- GET /api/v1/projects - List user's projects
- POST /api/v1/projects - Create new project
- GET /api/v1/projects/{id} - Get project details
- PUT /api/v1/projects/{id} - Update project
- DELETE /api/v1/projects/{id} - Delete project

### Specifications
- GET /api/v1/projects/{id}/specs - List specifications
- POST /api/v1/projects/{id}/specs - Create specification
- GET /api/v1/specs/{id} - Get specification details
- PUT /api/v1/specs/{id} - Update specification
- DELETE /api/v1/specs/{id} - Delete specification

## Deployment

### Docker Deployment
```bash
cd src/backend
docker-compose up -d
```

### Kubernetes Deployment
```bash
kubectl apply -k infrastructure/kubernetes/overlays/prod
```

## Monitoring

### Health Checks
- /health/live - Liveness probe
- /health/ready - Readiness probe
- /metrics - Prometheus metrics

### Logging
- Application logs: /var/log/app/application.log
- Access logs: /var/log/app/access.log
- Error logs: /var/log/app/error.log

## Security

### Authentication Flow
1. Client authenticates with Google
2. Backend validates Google token
3. JWT token issued for subsequent requests
4. Token refresh available for extended sessions

### Security Measures
- TLS encryption for all endpoints
- JWT-based authentication
- Rate limiting per IP
- SQL injection protection
- XSS prevention headers
- CORS configuration
- Request size limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Pull Request Guidelines
- Include unit tests
- Update documentation
- Follow code style guidelines
- Add meaningful commit messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.