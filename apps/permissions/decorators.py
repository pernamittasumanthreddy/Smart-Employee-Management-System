from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from apps.permissions.models import SystemRole


def role_required(*allowed_roles):
    """
    Decorator for views that checks if the user has one of the required roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            
            # Superusers always bypass role checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            user_role = getattr(request.user, 'role', None)
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
                
            messages.error(request, "You do not have permission to access this module.")
            return redirect('authentication:dashboard')
        return _wrapped_view
    return decorator

def admin_required(view_func):
    return role_required(SystemRole.ADMIN)(view_func)

def hr_or_admin_required(view_func):
    return role_required(SystemRole.ADMIN, SystemRole.HR)(view_func)

def manager_or_above_required(view_func):
    return role_required(SystemRole.ADMIN, SystemRole.HR, SystemRole.MANAGER)(view_func)
