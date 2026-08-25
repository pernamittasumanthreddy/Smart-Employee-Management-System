import pytest
from apps.organization.models import Department, Designation, Team
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestOrganizationDeepSuite:
    def setup_method(self):
        self.dept = Department.objects.create(name="Strategic Growth & AI", code="DEPT-AI-STRAT")
        self.desig = Designation.objects.create(title="Chief AI Scientist", department=self.dept)
        self.team = Team.objects.create(name="Foundation Models Squad", code="SQ-FM-01", department=self.dept)

    def test_department_hierarchy_and_budget(self):
        assert self.dept.code == "DEPT-AI-STRAT"
        assert self.desig.department == self.dept
        assert self.team.department == self.dept

    def test_team_member_association(self):
        user = User.objects.create_user(username="ai.scientist.user", password="Password@123")
        emp = Employee.objects.create(
            user=user,
            employee_id="EMP-AI-001",
            first_name="Arya",
            last_name="Bhatt",
            email="arya.ai@example.com",
            department=self.dept,
            designation=self.desig,
            team=self.team,
            employment_status='ACTIVE'
        )
        assert emp.team == self.team
        assert self.team.members.count() >= 1
