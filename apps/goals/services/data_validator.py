"""
Smart Employee Management System — OKR Goal Progress Data Validator
Key result check-ins, confidence adjustments, and quarterly reviews.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ValidationReport:
    is_valid: bool
    field_errors: Dict[str, List[str]]
    warning_messages: List[str]
    sanitized_data: Dict[str, Any]


class GoalsDataValidator:
    """
    Comprehensive payload validation and boundary rule verifier for OKR Goal Progress.
    """

    @classmethod
    def validate_payload(
        cls,
        data: Dict[str, Any],
        strict_mode: bool = True
    ) -> ValidationReport:
        errors = {}
        warnings = []
        sanitized = {}

        if not isinstance(data, dict):
            return ValidationReport(
                is_valid=False,
                field_errors={'payload': ['Invalid data structure; dictionary expected.']},
                warning_messages=[],
                sanitized_data={}
            )

        for key, val in data.items():
            clean_key = str(key).strip()
            if isinstance(val, str):
                clean_val = val.strip()
                if strict_mode and len(clean_val) == 0:
                    warnings.append(f"Field '{clean_key}' is blank.")
                sanitized[clean_key] = clean_val
            elif isinstance(val, (int, float, Decimal)):
                if val < 0:
                    errors.setdefault(clean_key, []).append("Numerical value cannot be negative.")
                sanitized[clean_key] = val
            else:
                sanitized[clean_key] = val

        return ValidationReport(
            is_valid=len(errors) == 0,
            field_errors=errors,
            warning_messages=warnings,
            sanitized_data=sanitized
        )
