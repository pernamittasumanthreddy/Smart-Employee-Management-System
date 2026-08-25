import pytest
from datetime import date
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.helpdesk.models import TicketCategory, SupportTicket, TicketStatus

@pytest.mark.django_db
def test_helpdesk():
    user = User.objects.create_user(username='hduser', email='hd@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-HD-01', first_name='HD', last_name='User', email='hd@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = TicketCategory.objects.create(name='IT')
    tkt = SupportTicket.objects.create(ticket_number='TKT-01', category=cat, creator=emp, subject='Monitor broken', description='No display')
    assert tkt.status == TicketStatus.OPEN
