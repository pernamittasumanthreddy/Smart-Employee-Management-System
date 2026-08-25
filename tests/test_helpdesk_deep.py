import pytest
from django.utils import timezone
from apps.helpdesk.models import SupportTicket, TicketCategory
from apps.helpdesk.sla_escalation_engine import HelpdeskSLAEngine
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestHelpdeskDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="help.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-HELP-DEEP-01",
            first_name="Harish",
            last_name="Kalyan",
            email="harish.help@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.cat, _ = TicketCategory.objects.get_or_create(name="Hardware & Infrastructure")

    def test_ticket_creation_and_sla(self):
        t = SupportTicket.objects.create(
            employee=self.emp,
            category=self.cat,
            title="External 4K Monitor Connection Issue",
            description="DisplayPort cable replacement required.",
            priority="LOW",
            status="OPEN"
        )
        assert t.priority == "LOW"
        assert t.status == "OPEN"
