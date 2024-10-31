# Python standard library imports (version 3.9+)
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

# Third-party imports
from google.cloud.logging import Client  # google-cloud-logging v3.0+
from google.cloud.logging.handlers.transports.sync import SyncTransport

# Human tasks:
# 1. Ensure Google Cloud project credentials are properly configured in the environment
# 2. Set up appropriate IAM roles for Cloud Logging access
# 3. Configure logging retention policies in Google Cloud Console
# 4. Set up log-based metrics and alerts if needed

class JsonFormatter(logging.Formatter):
    """
    Custom log formatter that outputs log records in JSON format.
    
    Requirement addressed: Logging System
    - Provides structured JSON logging for better parsing and analysis
    - Ensures consistent log format across the application
    """
    
    def __init__(self, datefmt: Optional[str] = None) -> None:
        """
        Initialize the JSON formatter.
        
        Args:
            datefmt: Optional date format string for timestamp formatting
        """
        super().__init__()
        self.datefmt = datefmt

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON string.
        
        Args:
            record: The log record to format
            
        Returns:
            JSON formatted string containing the log data
        """
        # Create base log data dictionary
        log_data: Dict[str, Any] = {
            'timestamp': self.format_timestamp(record),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
            'path': record.pathname,
            'line_number': record.lineno,
            'function': record.funcName,
            'process': record.process,
            'thread': record.thread,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
            
        # Add custom fields from extra or args
        if hasattr(record, 'extra'):
            log_data['extra'] = record.extra
            
        # Add any custom attributes that were passed via LogRecord
        for key, value in record.__dict__.items():
            if key not in logging.LogRecord.__dict__ and key not in log_data:
                log_data[key] = value
                
        return json.dumps(log_data, default=str)
    
    def format_timestamp(self, record: logging.LogRecord) -> str:
        """
        Format the record timestamp according to the specified date format.
        
        Args:
            record: The log record containing the timestamp
            
        Returns:
            Formatted timestamp string
        """
        if self.datefmt:
            return datetime.fromtimestamp(record.created).strftime(self.datefmt)
        return datetime.fromtimestamp(record.created).isoformat()


class CloudLoggingHandler(logging.Handler):
    """
    Custom handler for sending logs to Google Cloud Logging.
    
    Requirement addressed: Log Management
    - Implements centralized logging using Google Cloud Logging
    - Provides structured logging with severity levels
    - Ensures consistent log delivery to cloud infrastructure
    """
    
    # Mapping of logging levels to Google Cloud severity levels
    SEVERITY_MAP = {
        logging.DEBUG: 'DEBUG',
        logging.INFO: 'INFO',
        logging.WARNING: 'WARNING',
        logging.ERROR: 'ERROR',
        logging.CRITICAL: 'CRITICAL'
    }
    
    def __init__(self, project_id: str, log_name: Optional[str] = None) -> None:
        """
        Initialize the Google Cloud Logging handler.
        
        Args:
            project_id: Google Cloud project ID
            log_name: Optional custom log name (defaults to 'python')
        """
        super().__init__()
        
        # Initialize Google Cloud Logging client
        self._client = Client(project=project_id)
        
        # Set up cloud logger instance
        self._logger = self._client.logger(log_name or 'python')
        
        # Set default formatter to JSON
        self.setFormatter(JsonFormatter())
        
    def emit(self, record: logging.LogRecord) -> None:
        """
        Send log record to Google Cloud Logging.
        
        Args:
            record: The log record to send
        """
        try:
            # Format the record using the formatter
            message = self.format(record)
            
            # Parse the message back to dict if it's JSON
            try:
                structured_data = json.loads(message)
            except json.JSONDecodeError:
                structured_data = {'message': message}
            
            # Determine severity level
            severity = self.SEVERITY_MAP.get(record.levelno, 'DEFAULT')
            
            # Create and write the log entry
            self._logger.log_struct(
                structured_data,
                severity=severity,
                source_location={
                    'file': record.pathname,
                    'line': record.lineno,
                    'function': record.funcName
                }
            )
            
        except Exception as e:
            # Fallback to sys.stderr in case of errors
            import sys
            print(f'Error sending log to Google Cloud Logging: {str(e)}',
                  file=sys.stderr)