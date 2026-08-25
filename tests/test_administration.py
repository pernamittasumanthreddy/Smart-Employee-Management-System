import pytest
from apps.authentication.models import User
from apps.administration.models import AuditLog, AuditAction, BackupConfiguration

@pytest.mark.django_db
def test_audit_logs():
    user = User.objects.create_user(username='admuser', email='adm@test.com', password='Password@123')
    log = AuditLog.objects.create(user=user, username='admuser', action=AuditAction.CREATE, module='EMPLOYEES', description='Created employee')
    assert log.action == AuditAction.CREATE
