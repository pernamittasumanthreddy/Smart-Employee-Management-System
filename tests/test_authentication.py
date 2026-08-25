import pytest
from django.urls import reverse
from apps.authentication.models import User, LoginHistory
from apps.permissions.models import SystemRole

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username='testuser', email='test@test.com', password='Password@123', role=SystemRole.EMPLOYEE)
    assert user.username == 'testuser'
    assert user.role == SystemRole.EMPLOYEE
    assert user.check_password('Password@123')

@pytest.mark.django_db
def test_login_view(client):
    user = User.objects.create_user(username='testlogin', email='login@test.com', password='Password@123')
    response = client.post(reverse('authentication:login'), {'username': 'testlogin', 'password': 'Password@123'})
    assert response.status_code == 302
