# Python standard library imports (version 3.9+)
import logging

# Internal imports
from .handlers import JsonFormatter, CloudLoggingHandler
from .config import configure_logging

# Human tasks:
# 1. Ensure Google Cloud project credentials are properly configured in the environment
# 2. Set up appropriate IAM roles for Cloud Logging access
# 3. Configure logging retention policies in Google Cloud Console
# 4. Set up log-based metrics and alerts if needed

# Initialize module logger
logger = logging.getLogger(__name__)

# Re-export required components
__all__ = [
    'JsonFormatter',
    'CloudLoggingHandler',
    'configure_logging'
]

# Requirement addressed: Logging System
# - Initializes and exports core logging components
# - Provides centralized access to logging functionality
# - Ensures consistent logging configuration across the application

# Requirement addressed: Log Management
# - Exports Cloud Logging integration components
# - Enables centralized log management in cloud infrastructure
# - Facilitates structured logging with JSON formatting