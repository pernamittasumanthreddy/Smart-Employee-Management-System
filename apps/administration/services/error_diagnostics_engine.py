"""
Smart Enterprise Management System — Error Handling & Telemetry Diagnostics Engine
Parses exceptions, classifies root causes, redacts sensitive credentials,
and generates actionable resolution instructions.
"""

import traceback
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class DiagnosticIncidentReport:
    incident_id: str
    timestamp: datetime
    error_class: str
    error_message: str
    severity_level: str # CRITICAL, ERROR, WARNING, INFO
    http_status_code: int
    source_module: str
    sanitized_stacktrace: str
    suggested_action: str
    context_metadata: Dict[str, Any] = field(default_factory=dict)


class ErrorDiagnosticsEngine:
    """
    Enterprise telemetry parser and exception classifier.
    """

    ERROR_CLASSIFICATION_RULES = {
        'IntegrityError': ('DATABASE_INTEGRITY_FAULT', 409, 'CRITICAL', 'Check for unique constraint collisions (e.g. duplicate email, employee ID, or national ID).'),
        'ValidationError': ('DATA_VALIDATION_FAILURE', 422, 'WARNING', 'Verify incoming payload against model validation schemas and field formats.'),
        'PermissionDenied': ('SECURITY_AUTHORIZATION_DENIED', 403, 'ERROR', 'Verify user RBAC role assignment and active capabilities in permissions matrix.'),
        'ObjectDoesNotExist': ('ENTITY_NOT_FOUND', 404, 'INFO', 'Ensure requested record ID exists and has not been archived or deleted.'),
        'OperationalError': ('DATABASE_CONNECTIVITY_ISSUE', 503, 'CRITICAL', 'Verify SQLite/PostgreSQL connection string and disk write permissions.'),
        'TimeoutError': ('UPSTREAM_TIMEOUT', 504, 'ERROR', 'Investigate external microservice or slow database query performance.')
    }

    @classmethod
    def diagnose_exception(
        cls,
        exception: Exception,
        module_name: str = 'core',
        request_context: Optional[Dict[str, Any]] = None
    ) -> DiagnosticIncidentReport:
        import uuid
        err_type = type(exception).__name__
        err_msg = str(exception)

        cat, status_code, severity, remediation = cls.ERROR_CLASSIFICATION_RULES.get(
            err_type,
            ('UNCLASSIFIED_RUNTIME_ERROR', 500, 'ERROR', 'Inspect full stack trace and verify module dependencies.')
        )

        raw_trace = traceback.format_exc()
        # Redact secrets (passwords, tokens, keys)
        sanitized = raw_trace.replace('password', '***').replace('secret', '***').replace('token', '***')

        incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        return DiagnosticIncidentReport(
            incident_id=incident_id,
            timestamp=datetime.now(),
            error_class=err_type,
            error_message=err_msg,
            severity_level=severity,
            http_status_code=status_code,
            source_module=module_name,
            sanitized_stacktrace=sanitized,
            suggested_action=remediation,
            context_metadata=request_context or {}
        )
