"""
Monitoring package initialization module exposing health check and metrics collection functionality.

Human Tasks:
1. Verify database connection settings in environment variables
2. Confirm Redis connection parameters in configuration
3. Review health check thresholds with operations team
4. Set up monitoring alerts based on health check results
5. Verify Prometheus endpoint security settings with the security team
6. Confirm metric collection intervals with the operations team
7. Review alert thresholds with the SRE team
8. Ensure metric retention policies align with compliance requirements
"""

# Internal imports
from .health import (  # type: ignore
    HealthStatus,
    HealthCheck,
    get_system_health
)
from .metrics import (  # type: ignore
    MetricsCollector,
    get_metrics_collector,
    export_metrics
)

# Requirement: 7.1 High-Level Architecture/Core Components - Core monitoring system component
# Export all required monitoring components
__all__ = [
    'HealthStatus',
    'HealthCheck',
    'get_system_health',
    'MetricsCollector',
    'get_metrics_collector',
    'export_metrics'
]

# Requirement: 11.5.2 Pipeline Stages - Performance metrics and health monitoring
# Initialize metrics collector singleton on module import
metrics_collector = get_metrics_collector()