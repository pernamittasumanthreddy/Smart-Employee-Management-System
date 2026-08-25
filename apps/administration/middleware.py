from apps.administration.models import AuditAction, AuditLog


class AuditLoggingMiddleware:
    """
    Middleware that captures and logs user actions across the platform for audit and compliance.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log mutating operations (POST, PUT, DELETE, PATCH) by authenticated users
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            path = request.path
            # Filter out internal admin/login polling if needed
            if not path.startswith('/static/') and not path.startswith('/media/'):
                ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
                if ip and ',' in ip:
                    ip = ip.split(',')[0].strip()

                module_name = 'SYSTEM'
                if '/employees/' in path:
                    module_name = 'EMPLOYEE_MANAGEMENT'
                elif '/attendance/' in path:
                    module_name = 'ATTENDANCE_MANAGEMENT'
                elif '/leave/' in path:
                    module_name = 'LEAVE_MANAGEMENT'
                elif '/projects/' in path:
                    module_name = 'PROJECT_MANAGEMENT'
                elif '/tasks/' in path:
                    module_name = 'TASK_MANAGEMENT'
                elif '/performance/' in path:
                    module_name = 'PERFORMANCE_MANAGEMENT'
                elif '/expenses/' in path:
                    module_name = 'EXPENSE_MANAGEMENT'
                elif '/assets/' in path:
                    module_name = 'ASSET_MANAGEMENT'
                elif '/helpdesk/' in path:
                    module_name = 'HELPDESK_SUPPORT'
                elif '/documents/' in path:
                    module_name = 'DOCUMENT_MANAGEMENT'
                elif '/auth/' in path:
                    module_name = 'AUTHENTICATION'

                action = AuditAction.UPDATE
                if 'create' in path or 'add' in path or 'punch' in path or 'claim' in path:
                    action = AuditAction.CREATE
                elif 'delete' in path or 'remove' in path:
                    action = AuditAction.DELETE
                elif 'approve' in path:
                    action = AuditAction.APPROVE
                elif 'reject' in path:
                    action = AuditAction.REJECT

                try:
                    AuditLog.objects.create(
                        user=request.user,
                        username=request.user.username,
                        action=action,
                        module=module_name,
                        ip_address=ip,
                        description=f"HTTP {request.method} request to {path} (Status {response.status_code})"
                    )
                except Exception:
                    pass

        return response
