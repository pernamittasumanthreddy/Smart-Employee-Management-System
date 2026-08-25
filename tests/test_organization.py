import pytest
from decimal import Decimal
from apps.organization.models import Department, Team, Designation

@pytest.mark.django_db
def test_department_and_team():
    dept = Department.objects.create(name='Technology', code='TECH', budget=Decimal('50000.00'))
    team = Team.objects.create(name='Dev Team', code='DEV', department=dept)
    assert team.department == dept
    assert 'Technology' in str(dept)
