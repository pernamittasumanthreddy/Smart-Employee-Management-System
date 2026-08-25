import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.expenses.models import ExpenseCategory, ExpenseClaim, ExpenseStatus

@pytest.mark.django_db
def test_expenses():
    user = User.objects.create_user(username='expuser', email='exp@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-EXP-01', first_name='Exp', last_name='User', email='exp@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = ExpenseCategory.objects.create(name='Travel')
    claim = ExpenseClaim.objects.create(employee=emp, category=cat, claim_number='CLM-001', title='Hotel stay', amount=Decimal('200.00'), expense_date=date(2026, 5, 1), description='Lodging')
    assert claim.status == ExpenseStatus.PENDING
