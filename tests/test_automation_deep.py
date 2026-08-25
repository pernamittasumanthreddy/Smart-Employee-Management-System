import pytest
from apps.automation.models import AutomationRule, AutomationExecutionLog
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestAutomationDeepSuite:
    def setup_method(self):
        self.rule = AutomationRule.objects.create(
            name="Auto-Notify Manager on Leave Request Submission",
            trigger_event="LEAVE_SUBMITTED",
            condition_expression="days >= 3",
            action_type="SEND_NOTIFICATION",
            action_payload="Send high priority notification to reporting manager",
            is_active=True
        )

    def test_rule_execution_log(self):
        log = AutomationExecutionLog.objects.create(
            rule=self.rule,
            triggered_by_entity="LeaveRequest#991",
            status="SUCCESS",
            details="Triggered manager approval notification successfully."
        )
        assert log.rule == self.rule
        assert log.status == "SUCCESS"
        assert self.rule.is_active is True
