import pytest
from django.utils import timezone
from apps.skills.models import Skill, EmployeeSkill, SkillCategory
from apps.employees.skill_matrix_service import SkillMatrixAnalyticsService
from apps.employees.models import Employee
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.mark.django_db
class TestSkillsDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="skill.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-SKILL-DEEP-01",
            first_name="Aditi",
            last_name="Rao",
            email="aditi.skill@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.cat, _ = SkillCategory.objects.get_or_create(name="Cloud & DevOps Architecture")
        self.skill = Skill.objects.create(name="Terraform Enterprise", category=self.cat)

    def test_employee_skill_rating(self):
        emp_s = EmployeeSkill.objects.create(
            employee=self.emp,
            skill=self.skill,
            proficiency_level=5,
            years_of_experience=4,
            is_verified=True
        )
        assert emp_s.proficiency_level == 5
        assert emp_s.is_verified is True
