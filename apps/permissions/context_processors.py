from apps.permissions.models import SystemRole


def role_context(request):
    """
    Context processor injecting role boolean flags into all templates.
    """
    if not request.user.is_authenticated:
        return {
            'is_admin': False,
            'is_hr': False,
            'is_manager': False,
            'is_employee': False,
            'user_role': None,
            'user_role_display': 'Guest',
        }
    
    role = getattr(request.user, 'role', SystemRole.EMPLOYEE)
    is_admin = (role == SystemRole.ADMIN) or request.user.is_superuser
    is_hr = (role == SystemRole.HR)
    is_manager = (role == SystemRole.MANAGER)
    is_employee = (role == SystemRole.EMPLOYEE)
    
    role_display_map = {
        SystemRole.ADMIN: 'Administrator',
        SystemRole.HR: 'HR Manager',
        SystemRole.MANAGER: 'Team Manager',
        SystemRole.EMPLOYEE: 'Employee',
    }

    return {
        'is_admin': is_admin,
        'is_hr': is_hr,
        'is_manager': is_manager,
        'is_employee': is_employee,
        'is_hr_or_admin': is_admin or is_hr,
        'is_manager_or_above': is_admin or is_hr or is_manager,
        'user_role': role,
        'user_role_display': role_display_map.get(role, 'User'),
    }
