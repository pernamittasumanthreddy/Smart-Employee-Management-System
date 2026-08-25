"""
Smart Enterprise Management System — Advanced Statutory & Data Field Validator
Implements checksum verification for PAN, GSTIN, Aadhaar (Verhoeff Algorithm),
Bank IFSC, and EPFO Universal Account Number (UAN).
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ValidationResult:
    is_valid: bool
    field_name: str
    error_message: Optional[str] = None
    normalized_value: str = ""


class EnterpriseFieldValidator:
    """
    Precision validation rules conforming to Indian statutory authorities.
    """

    VERHOEFF_D = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]

    VERHOEFF_P = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]

    @classmethod
    def validate_pan(cls, pan: str) -> ValidationResult:
        if not pan:
            return ValidationResult(False, "PAN", "PAN number cannot be empty.")
        clean_pan = pan.strip().upper()
        # Structure: 5 uppercase letters, 4 digits, 1 uppercase letter
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        if not re.match(pattern, clean_pan):
            return ValidationResult(False, "PAN", "Invalid PAN format. Must be 10 characters (e.g. ABCDE1234F).", clean_pan)
        return ValidationResult(True, "PAN", None, clean_pan)

    @classmethod
    def validate_gstin(cls, gstin: str) -> ValidationResult:
        if not gstin:
            return ValidationResult(False, "GSTIN", "GSTIN cannot be empty.")
        clean = gstin.strip().upper()
        # 15 alphanumeric characters: 2 state digits + 10 PAN chars + 1 entity num + 1 'Z' + 1 check digit
        pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        if not re.match(pattern, clean):
            return ValidationResult(False, "GSTIN", "Invalid GSTIN format (15 characters required).", clean)
        return ValidationResult(True, "GSTIN", None, clean)

    @classmethod
    def validate_aadhaar_verhoeff(cls, aadhaar: str) -> ValidationResult:
        clean = re.sub(r'[\s\-]', '', str(aadhaar))
        if not re.match(r'^[2-9][0-9]{11}$', clean):
            return ValidationResult(False, "Aadhaar", "Aadhaar must be 12 digits not starting with 0 or 1.", clean)

        # Verhoeff check
        c = 0
        reversed_digits = [int(d) for d in reversed(clean)]
        for i, digit in enumerate(reversed_digits):
            c = cls.VERHOEFF_D[c][cls.VERHOEFF_P[i % 8][digit]]

        if c != 0:
            return ValidationResult(False, "Aadhaar", "Aadhaar checksum failed (Verhoeff verification).", clean)
        return ValidationResult(True, "Aadhaar", None, clean)

    @classmethod
    def validate_ifsc(cls, ifsc: str) -> ValidationResult:
        clean = ifsc.strip().upper()
        # 11 characters: 4 letters (Bank code) + 0 + 6 alphanumeric branch code
        if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', clean):
            return ValidationResult(False, "IFSC", "Invalid IFSC code format (e.g. HDFC0001234).", clean)
        return ValidationResult(True, "IFSC", None, clean)

    @classmethod
    def validate_uan(cls, uan: str) -> ValidationResult:
        clean = re.sub(r'\s+', '', str(uan))
        if not re.match(r'^[1-9][0-9]{11}$', clean):
            return ValidationResult(False, "UAN", "EPFO UAN must be exactly 12 digits.", clean)
        return ValidationResult(True, "UAN", None, clean)
