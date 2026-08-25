"""
Comprehensive Automated Tests for Repository Analyzer, Field Validator, and Error Diagnostics Engine.
"""

import pytest
from apps.administration.services.repository_analyzer import RepositoryStructureAnalyzer
from apps.compliance.services.enterprise_field_validator import EnterpriseFieldValidator
from apps.administration.services.error_diagnostics_engine import ErrorDiagnosticsEngine


class TestRepositoryAndDiagnosticsSuite:
    def test_repository_structure_audit(self):
        """Test repository analyzer across all apps."""
        audit = RepositoryStructureAnalyzer.audit_application_modules()
        assert audit.total_modules == 34
        assert audit.total_source_loc >= 50000
        assert audit.architecture_status == 'EXCELLENT'

    def test_pan_field_validation_valid(self):
        """Test valid individual PAN number."""
        res = EnterpriseFieldValidator.validate_pan('ABCDE1234F')
        assert res.is_valid is True
        assert res.error_message is None

    def test_pan_field_validation_invalid(self):
        """Test invalid PAN format."""
        res = EnterpriseFieldValidator.validate_pan('INVALID_PAN_123')
        assert res.is_valid is False
        assert 'Invalid PAN' in res.error_message

    def test_gstin_validation(self):
        """Test GSTIN validation format."""
        res = EnterpriseFieldValidator.validate_gstin('29ABCDE1234F1Z5')
        assert res.is_valid is True

    def test_ifsc_code_validation(self):
        """Test Bank IFSC code format."""
        res = EnterpriseFieldValidator.validate_ifsc('HDFC0001234')
        assert res.is_valid is True

    def test_uan_validation(self):
        """Test EPFO UAN 12-digit format."""
        res = EnterpriseFieldValidator.validate_uan('101234567890')
        assert res.is_valid is True

    def test_error_diagnostics_engine(self):
        """Test diagnostic report generation from an exception."""
        try:
            raise KeyError("User token expired or invalid.")
        except Exception as ex:
            report = ErrorDiagnosticsEngine.diagnose_exception(ex, module_name='authentication')
            assert report.error_class == 'KeyError'
            assert report.http_status_code == 500
            assert report.source_module == 'authentication'
            assert len(report.incident_id) > 5
