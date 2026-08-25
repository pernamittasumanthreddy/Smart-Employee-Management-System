from apps.permissions.models import ModulePermission, Role, SystemModule, SystemRole


class PermissionService:
    @staticmethod
    def initialize_default_roles():
        """
        Sets up the default 4 roles and their initial permission matrices.
        """
        defaults = [
            (SystemRole.ADMIN, 'Administrator', 'Full unrestricted platform access'),
            (SystemRole.HR, 'HR Manager', 'Workforce management, attendance, leave, performance and HR operations'),
            (SystemRole.MANAGER, 'Team Manager', 'Team supervision, project tasks, approvals, workload and evaluations'),
            (SystemRole.EMPLOYEE, 'Employee', 'Individual self-service portal, check-in, leave requests, tasks and personal docs'),
        ]

        created_roles = {}
        for code, name, desc in defaults:
            role, _ = Role.objects.get_or_create(
                code=code,
                defaults={'name': name, 'description': desc, 'is_system_default': True}
            )
            created_roles[code] = role

        # Initialize default permissions for each module
        for code, role in created_roles.items():
            for mod_code, _ in SystemModule.choices:
                is_admin = (code == SystemRole.ADMIN)
                is_hr = (code == SystemRole.HR)
                is_mgr = (code == SystemRole.MANAGER)
                
                # Rule based default matrix
                can_create = is_admin or (is_hr and mod_code in ['EMP', 'ATT', 'LEAVE', 'SHIFT', 'TRAIN', 'ANNC', 'DOC']) or (is_mgr and mod_code in ['PROJ', 'TASK', 'GOAL', 'RECOG']) or (code == SystemRole.EMPLOYEE and mod_code in ['LEAVE', 'EXP', 'HELP'])
                can_update = is_admin or (is_hr and mod_code in ['EMP', 'ATT', 'LEAVE', 'PERF', 'TRAIN']) or (is_mgr and mod_code in ['TASK', 'GOAL'])
                can_delete = is_admin or (is_hr and mod_code in ['DOC', 'ANNC'])
                can_approve = is_admin or is_hr or (is_mgr and mod_code in ['LEAVE', 'TASK', 'EXP', 'PERF', 'GOAL'])

                ModulePermission.objects.get_or_create(
                    role=role,
                    module=mod_code,
                    defaults={
                        'can_create': can_create,
                        'can_read': True,
                        'can_update': can_update,
                        'can_delete': can_delete,
                        'can_approve': can_approve,
                    }
                )
        return created_roles
