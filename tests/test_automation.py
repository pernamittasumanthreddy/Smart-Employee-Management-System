import pytest
from apps.automation.models import AutomationRule, ExecutionLog

@pytest.mark.django_db
def test_automation_rules():
    rule = AutomationRule.objects.create(
        name="Welcome Onboarding Email Dispatcher",
        trigger_event="EMPLOYEE_JOINED",
        action_type="DISPATCH_EMAIL",
        action_payload="{'template': 'welcome_mail'}",
        is_active=True
    )
    log = ExecutionLog.objects.create(
        rule=rule,
        status='SUCCESS',
        details='Sent welcome email to new hire'
    )
    assert log.status == 'SUCCESS'
    assert rule.execution_logs.count() == 1
