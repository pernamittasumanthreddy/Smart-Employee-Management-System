import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.skills.models import SkillCategory, Skill, EmployeeSkill, SkillProficiency

@pytest.mark.django_db
def test_skills():
    user = User.objects.create_user(username='skuser', email='sk@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-SK-01', first_name='Skill', last_name='User', email='sk@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = SkillCategory.objects.create(name='Programming')
    sk = Skill.objects.create(category=cat, name='Python', code='PY')
    es = EmployeeSkill.objects.create(employee=emp, skill=sk, proficiency_level=SkillProficiency.ADVANCED, years_of_experience=Decimal('4.0'))
    assert es.proficiency_level == SkillProficiency.ADVANCED
