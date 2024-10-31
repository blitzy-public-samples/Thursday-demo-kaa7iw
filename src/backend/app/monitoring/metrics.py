"""
System metrics collection and monitoring functionality for the Flask backend application.

Human Tasks:
1. Verify Prometheus endpoint security settings with the security team
2. Confirm metric collection intervals with the operations team
3. Review alert thresholds with the SRE team
4. Ensure metric retention policies align with compliance requirements
"""

# External imports
from prometheus_client import Counter, Histogram, Gauge, generate_latest  # version: 0.14+
from typing import Optional  # version: 3.9+
from flask import Response  # version: 2.0+

# Internal imports
from ..utils.constants import SYS001, SYS002

# Singleton instance
_metrics_collector: Optional['MetricsCollector'] = None

class MetricsCollector:
    """
    Singleton class responsible for collecting and managing system metrics using Prometheus client.
    
    Requirement: 7.1 High-Level Architecture/Core Components - Core monitoring system component
    for collecting and tracking system metrics
    """
    
    def __init__(self) -> None:
        """
        Initializes Prometheus metrics collectors.
        
        Requirement: 11.5.2 Pipeline Stages - Performance metrics collection and monitoring
        """
        # Request count metric
        self.request_count_total = Counter(
            'request_count_total',
            'Total number of HTTP requests',
            ['endpoint', 'method']
        )
        
        # Request latency metric
        self.request_latency_seconds = Histogram(
            'request_latency_seconds',
            'Request latency in seconds',
            ['endpoint'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
        )
        
        # Active users metric
        self.active_users = Gauge(
            'active_users',
            'Number of currently active users'
        )
        
        # Error count metric
        self.error_count_total = Counter(
            'error_count_total',
            'Total number of errors',
            ['error_code']
        )
        
        # Database connections metric
        self.database_connections = Gauge(
            'database_connections',
            'Number of active database connections'
        )
        
        # Cache hit ratio metric
        self.cache_hit_ratio = Gauge(
            'cache_hit_ratio',
            'Cache hit ratio percentage'
        )

    def increment_request_count(self, endpoint: str, method: str) -> None:
        """
        Increments the total request counter.
        
        Args:
            endpoint: The API endpoint being accessed
            method: The HTTP method used
            
        Requirement: 7.1 High-Level Architecture/Core Components/LOG - System-wide metrics collection
        """
        try:
            self.request_count_total.labels(endpoint=endpoint, method=method).inc()
        except Exception:
            self.increment_error_count(SYS001)

    def observe_request_latency(self, endpoint: str, duration: float) -> None:
        """
        Records request latency in the histogram.
        
        Args:
            endpoint: The API endpoint being measured
            duration: Request duration in seconds
            
        Requirement: 11.5.2 Pipeline Stages - Performance metrics collection
        """
        try:
            self.request_latency_seconds.labels(endpoint=endpoint).observe(duration)
        except Exception:
            self.increment_error_count(SYS001)

    def set_active_users(self, count: int) -> None:
        """
        Updates the active users gauge.
        
        Args:
            count: Current number of active users
            
        Requirement: 7.1 High-Level Architecture/Core Components - System metrics
        """
        try:
            self.active_users.set(count)
        except Exception:
            self.increment_error_count(SYS001)

    def increment_error_count(self, error_code: str) -> None:
        """
        Increments the error counter.
        
        Args:
            error_code: The error code to increment
            
        Requirement: 7.1 High-Level Architecture/Core Components/LOG - Error tracking
        """
        try:
            self.error_count_total.labels(error_code=error_code).inc()
        except Exception:
            # Last resort error handling to avoid recursion
            pass

def get_metrics_collector() -> MetricsCollector:
    """
    Singleton accessor for MetricsCollector instance.
    
    Returns:
        MetricsCollector: Singleton instance of MetricsCollector
        
    Requirement: 7.1 High-Level Architecture/Core Components - Metrics collection
    """
    global _metrics_collector
    if _metrics_collector is None:
        try:
            _metrics_collector = MetricsCollector()
        except Exception:
            # Handle initialization error
            if _metrics_collector is None:
                raise RuntimeError("Failed to initialize metrics collector")
    return _metrics_collector

def export_metrics() -> Response:
    """
    Exports collected metrics in Prometheus format.
    
    Returns:
        Response: Flask response containing metrics in Prometheus format
        
    Requirement: 11.5.2 Pipeline Stages - Metrics collection with health checks
    """
    try:
        metrics_data = generate_latest()
        return Response(metrics_data, mimetype='text/plain; version=0.0.4')
    except Exception:
        # Log metric export failure
        get_metrics_collector().increment_error_count(SYS002)
        return Response("Metric export failed", status=500)