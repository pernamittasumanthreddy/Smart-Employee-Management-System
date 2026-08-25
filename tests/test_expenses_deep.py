import pytest
from decimal import Decimal
from django.utils import timezone
from apps.expenses.models import ExpenseClaim, ExpenseCategory
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestExpensesDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="exp.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-EXP-DEEP-01",
            first_name="Vikram",
            last_name="Batra",
            email="vikram.exp@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.cat, _ = ExpenseCategory.objects.get_or_create(name="Business Travel & Client Meals")

    def test_expense_submission_and_approval(self):
        exp = ExpenseClaim.objects.create(
            employee=self.emp,
            category=self.cat,
            amount=Decimal('4500.00'),
            expense_date=timezone.now().date(),
            description="Client Dinner Workshop in Bengaluru",
            status="APPROVED"
        )
        assert exp.amount == Decimal('4500.00')
        assert exp.status == "APPROVED"
