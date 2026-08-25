import pytest
from apps.permissions.models import Role, ModulePermission, SystemRole, SystemModule
from apps.permissions.services import PermissionService

@pytest.mark.django_db
def test_permission_initialization():
    PermissionService.initialize_default_roles()
    assert Role.objects.filter(code=SystemRole.ADMIN).exists()
    assert Role.objects.filter(code=SystemRole.EMPLOYEE).exists()
    admin_role = Role.objects.get(code=SystemRole.ADMIN)
    assert admin_role.permissions.count() > 0
