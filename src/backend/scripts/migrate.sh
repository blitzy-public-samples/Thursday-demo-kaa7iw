#!/bin/bash

# Human Tasks:
# 1. Verify PostgreSQL connection string format in environment variables
# 2. Ensure database user has sufficient privileges for migrations
# 3. Review logging configuration for migration operations
# 4. Confirm database backup before running migrations
# 5. Set up proper environment variables in .env file
# 6. Ensure PYTHONPATH includes the project root directory

# Set strict error handling
set -euo pipefail

# Script directory for relative path resolution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Required environment variables
# Requirement: Data Access Layer - PostgreSQL database interactions
required_vars=("FLASK_ENV" "DATABASE_URL")

# Function to check required environment variables
# Requirement: Data Management - Database schema management and migrations
check_environment() {
    local exit_code=0
    
    # Load environment variables from .env if it exists
    if [[ -f "${PROJECT_ROOT}/.env" ]]; then
        source "${PROJECT_ROOT}/.env"
    fi
    
    # Check if required variables are set
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            echo "Error: Required environment variable $var is not set"
            exit_code=1
        fi
    done
    
    # Validate FLASK_ENV value
    if [[ -n "${FLASK_ENV:-}" ]]; then
        case "$FLASK_ENV" in
            development|production|testing)
                ;;
            *)
                echo "Error: FLASK_ENV must be one of: development, production, testing"
                exit_code=1
                ;;
        esac
    fi
    
    return $exit_code
}

# Function to run database migrations
# Requirement: Data Management - Database schema management and migrations
run_migrations() {
    local mode="$1"
    local exit_code=0
    
    # Set PYTHONPATH to include project root
    export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"
    
    echo "Running migrations in $mode mode..."
    
    case "$mode" in
        offline)
            # Generate SQL migration script
            if ! alembic upgrade head --sql > migration.sql; then
                echo "Error: Failed to generate migration SQL"
                exit_code=1
            else
                echo "Migration SQL script generated successfully: migration.sql"
            fi
            ;;
        online)
            # Execute migrations directly
            if ! alembic upgrade head; then
                echo "Error: Failed to execute online migration"
                exit_code=1
            else
                echo "Online migration completed successfully"
            fi
            ;;
        *)
            echo "Error: Invalid migration mode. Use 'online' or 'offline'"
            exit_code=1
            ;;
    esac
    
    return $exit_code
}

# Main script execution
main() {
    local exit_code=0
    
    # Verify environment
    if ! check_environment; then
        echo "Environment check failed"
        return 1
    fi
    
    # Parse command line arguments
    local mode="online"
    if [[ $# -gt 0 ]]; then
        mode="$1"
    fi
    
    # Change to project root directory
    cd "${PROJECT_ROOT}"
    
    # Run migrations with specified mode
    if ! run_migrations "$mode"; then
        echo "Migration failed"
        exit_code=1
    fi
    
    return $exit_code
}

# Execute main function with all arguments
main "$@"