import pytest
from apps.compliance.models import StatutoryRegister, ComplianceAudit, POSHCommitteeMember
from apps.compliance.statutory_engine import StatutoryRegisterCompiler

@pytest.mark.django_db
def test_statutory_registers_compiler():
    reg_rows = StatutoryRegisterCompiler.compile_form_a_employee_register()
    assert isinstance(reg_rows, list)
    
    wage_rows = StatutoryRegisterCompiler.compile_form_b_wage_register(2026, 8)
    assert isinstance(wage_rows, list)

@pytest.mark.django_db
def test_compliance_audit_record():
    audit = ComplianceAudit.objects.create(
        title="Q3 Statutory Labour Compliance Audit",
        score_percentage=99,
        status='COMPLETED'
    )
    assert audit.score_percentage == 99
