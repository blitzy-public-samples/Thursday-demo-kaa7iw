#!/bin/bash

# Human Tasks:
# 1. Ensure PostgreSQL is installed and running locally
# 2. Ensure Redis is installed and running locally
# 3. Configure Google OAuth credentials in .env file
# 4. Review and adjust environment variables in .env for your environment
# 5. Make sure you have Python 3.9+ installed on your system
# 6. Ensure pip and virtualenv are installed globally

# Requirement: Environment Configuration - Sets up required environment configuration for all application components
# Requirement: Database Setup - Initializes PostgreSQL database and performs initial migrations
# Requirement: Development Environment - Configures development environment with required dependencies and settings

# Set error handling
set -e
set -o pipefail

# Global variables
PYTHON_MIN_VERSION="3.9.0"
VENV_DIR="./venv"
REQUIREMENTS_FILE="./requirements.txt"
BACKEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function: Verifies that the correct version of Python is installed
check_python_version() {
    log_info "Checking Python version..."
    
    # Get Python version
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
    
    # Compare versions
    python3 -c "from packaging import version; exit(0 if version.parse('$PYTHON_VERSION') >= version.parse('$PYTHON_MIN_VERSION') else 1)" || {
        log_error "Python version $PYTHON_MIN_VERSION or higher is required. Found version $PYTHON_VERSION"
        exit 1
    }
    
    log_info "Python version $PYTHON_VERSION detected - OK"
}

# Function: Creates and activates Python virtual environment
setup_virtual_environment() {
    log_info "Setting up virtual environment..."
    
    # Check if virtualenv is installed
    if ! command -v virtualenv &> /dev/null; then
        log_error "virtualenv is not installed. Please install it using: pip install virtualenv"
        exit 1
    }
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        virtualenv -p python3 "$VENV_DIR"
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    log_info "Virtual environment activated"
}

# Function: Installs required Python packages from requirements.txt
install_dependencies() {
    log_info "Installing dependencies..."
    
    # Upgrade pip to latest version
    pip install --upgrade pip
    
    # Install packages from requirements.txt
    pip install -r "$REQUIREMENTS_FILE"
    
    # Verify installation success
    pip check || {
        log_error "Dependency installation failed"
        exit 1
    }
    
    log_info "Dependencies installed successfully"
}

# Function: Sets up environment configuration files
setup_environment() {
    log_info "Setting up environment configuration..."
    
    # Copy .env.example to .env if not exists
    if [ ! -f "$BACKEND_DIR/.env" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        log_warn "Created .env file from example. Please update with your configuration."
    else
        log_info ".env file already exists"
    fi
    
    # Copy .flaskenv if not exists
    if [ ! -f "$BACKEND_DIR/.flaskenv" ]; then
        cp "$BACKEND_DIR/.flaskenv" "$BACKEND_DIR/.flaskenv"
        log_info "Created .flaskenv file"
    else
        log_info ".flaskenv file already exists"
    fi
}

# Function: Initializes database and runs migrations
initialize_database() {
    log_info "Initializing database..."
    
    # Source the .env file to get database configuration
    if [ -f "$BACKEND_DIR/.env" ]; then
        source "$BACKEND_DIR/.env"
    else
        log_error ".env file not found. Database initialization failed."
        exit 1
    fi
    
    # Check database connection
    python3 -c "
import psycopg2
from urllib.parse import urlparse
url = urlparse('$DATABASE_URL')
try:
    conn = psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    conn.close()
except Exception as e:
    exit(1)
" || {
        log_error "Database connection failed. Please check your DATABASE_URL in .env"
        exit 1
    }
    
    # Run database migrations
    export FLASK_APP=wsgi.py
    flask db upgrade
    
    log_info "Database initialized successfully"
}

# Main setup process
main() {
    log_info "Starting backend setup..."
    
    # Change to backend directory
    cd "$BACKEND_DIR"
    
    # Run setup steps
    check_python_version
    setup_virtual_environment
    install_dependencies
    setup_environment
    initialize_database
    
    log_info "Backend setup completed successfully!"
    log_info "You can now start the development server using: flask run"
}

# Execute main function
main