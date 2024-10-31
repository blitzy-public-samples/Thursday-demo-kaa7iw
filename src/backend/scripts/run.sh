#!/bin/bash

# Human Tasks:
# 1. Ensure Python 3.9+ is installed
# 2. Create and configure virtual environment if not exists
# 3. Set up Google Cloud User Store credentials
# 4. Configure PostgreSQL connection string
# 5. Configure Redis connection parameters
# 6. Review and adjust Gunicorn worker/thread settings for production
# 7. Set up SSL certificates for production deployment

# Requirement: System Overview - Implements the Flask web server handling REST API requests
# Requirement: Deployment Environment - Provides environment-specific application startup
# Requirement: Environment Configuration - Configures and starts Flask application with appropriate settings

# Function to check required environment variables
check_environment() {
    # Check if FLASK_ENV is set
    if [ -z "$FLASK_ENV" ]; then
        echo "Error: FLASK_ENV environment variable is not set"
        return 1
    fi

    # Check if FLASK_APP is set
    if [ -z "$FLASK_APP" ]; then
        echo "Error: FLASK_APP environment variable is not set"
        return 1
    fi

    # Validate FLASK_ENV value
    case "$FLASK_ENV" in
        development|staging|production)
            ;;
        *)
            echo "Error: Invalid FLASK_ENV value. Must be development, staging, or production"
            return 1
            ;;
    esac

    return 0
}

# Function to setup and activate virtual environment
setup_virtualenv() {
    VENV_DIR="venv"
    
    # Check if virtual environment exists
    if [ ! -d "$VENV_DIR" ]; then
        echo "Virtual environment not found. Creating new virtual environment..."
        python3 -m venv "$VENV_DIR"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to create virtual environment"
            return 1
        fi
    fi

    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to activate virtual environment"
        return 1
    fi

    # Verify activation
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Error: Virtual environment activation failed"
        return 1
    fi

    return 0
}

# Function to start the application based on environment
start_application() {
    # Load environment variables from .env and .flaskenv
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
    if [ -f .flaskenv ]; then
        export $(cat .flaskenv | grep -v '^#' | xargs)
    fi

    # Set default values for optional environment variables
    export FLASK_DEBUG=${FLASK_DEBUG:-0}
    export GUNICORN_WORKERS=${GUNICORN_WORKERS:-3}
    export GUNICORN_THREADS=${GUNICORN_THREADS:-2}

    # Start application based on environment
    case "$FLASK_ENV" in
        production)
            echo "Starting production server with Gunicorn..."
            exec gunicorn \
                --bind 0.0.0.0:8000 \
                --workers $GUNICORN_WORKERS \
                --threads $GUNICORN_THREADS \
                --access-logfile - \
                --error-logfile - \
                --log-level info \
                --capture-output \
                --enable-stdio-inheritance \
                wsgi:app
            ;;
        staging)
            echo "Starting staging server with Gunicorn..."
            exec gunicorn \
                --bind 0.0.0.0:8000 \
                --workers 2 \
                --threads 2 \
                --access-logfile - \
                --error-logfile - \
                --log-level debug \
                --reload \
                wsgi:app
            ;;
        development)
            echo "Starting development server..."
            exec flask run --host=0.0.0.0 --port=8000
            ;;
    esac
}

# Main execution flow
main() {
    # Change to the backend directory
    cd "$(dirname "$0")/.." || exit 1

    # Check environment variables
    if ! check_environment; then
        exit 1
    fi

    # Setup virtual environment
    if ! setup_virtualenv; then
        exit 1
    fi

    # Install dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install dependencies"
            exit 1
        fi
    fi

    # Start the application
    start_application
}

# Execute main function
main