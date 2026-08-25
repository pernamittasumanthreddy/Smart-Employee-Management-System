import pytest
from apps.compliance.posh_investigation_service import POSHInvestigationService
from apps.lifecycle.offboarding_checklists import OffboardingChecklistManager
from apps.workplace.desk_allocation_ai import SmartDeskAllocationAI
from apps.api.webhook_signature_validator import WebhookSignatureValidator
from apps.automation.trigger_registry import AutomationTriggerRegistry

@pytest.mark.django_db
def test_posh_and_offboarding_services():
    po = POSHInvestigationService.get_presiding_officer()
    assert 'name' in po
    assert 'email' in po

    metrics = POSHInvestigationService.audit_posh_annual_report_metrics(2026)
    assert metrics['compliance_status'] == '100% STATUTORY COMPLIANT'

    matrix = OffboardingChecklistManager.generate_clearance_matrix()
    assert 'IT' in matrix
    assert 'FINANCE' in matrix

def test_webhook_and_triggers():
    triggers = AutomationTriggerRegistry.list_triggers()
    assert len(triggers) >= 6

    # Test HMAC signature verification
    secret = "test_super_secret_key_123"
    payload = b'{"event":"punch","employee_id":"EMP001"}'
    import hmac, hashlib
    valid_sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    assert WebhookSignatureValidator.verify_signature(payload, secret, valid_sig) is True
    assert WebhookSignatureValidator.verify_signature(payload, secret, "invalid_signature") is False
