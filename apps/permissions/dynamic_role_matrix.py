from typing import Dict, List, Set

class DynamicRoleMatrixEngine:
    '''
    Enterprise Dynamic RBAC Matrix:
    Maps 34 functional modules across 4 hierarchical personas:
    1. Administrator (Full system read/write/delete/configure/audit)
    2. HR Manager (Workforce, Payroll, Recruitment, Lifecycle, Benefits, Compliance)
    3. Team Manager (Team approvals, Tasks, Projects, Attendance, Timesheets)
    4. Staff Member (Self-service punch, Leaves, Expenses, Profile, Payslips, Surveys)
    '''

    MODULE_PERMISSIONS = {
        'ADMIN': {
            'authentication': {'read', 'write', 'delete', 'admin'},
            'employees': {'read', 'write', 'delete', 'export'},
            'organization': {'read', 'write', 'delete'},
            'permissions': {'read', 'write', 'delete', 'admin'},
            'payroll': {'read', 'write', 'disburse', 'admin'},
            'recruitment': {'read', 'write', 'hire', 'admin'},
            'lifecycle': {'read', 'write', 'clearance', 'admin'},
            'compliance': {'read', 'write', 'audit', 'admin'},
            'benefits': {'read', 'write', 'admin'},
            'timesheets': {'read', 'write', 'approve', 'admin'},
            'surveys': {'read', 'write', 'analytics', 'admin'},
            'workplace': {'read', 'write', 'admin'},
            'api': {'read', 'write', 'admin'},
            'automation': {'read', 'write', 'admin'},
            'insights': {'read', 'admin'},
            'reports': {'read', 'export', 'admin'},
            'administration': {'read', 'write', 'backup', 'admin'},
        },
        'HR_MANAGER': {
            'employees': {'read', 'write', 'export'},
            'organization': {'read', 'write'},
            'payroll': {'read', 'write', 'disburse'},
            'recruitment': {'read', 'write', 'hire'},
            'lifecycle': {'read', 'write', 'clearance'},
            'compliance': {'read', 'write', 'audit'},
            'benefits': {'read', 'write'},
            'attendance': {'read', 'write', 'approve'},
            'leave_management': {'read', 'write', 'approve'},
            'performance': {'read', 'write'},
            'training': {'read', 'write'},
            'surveys': {'read', 'analytics'},
            'reports': {'read', 'export'},
        },
        'TEAM_MANAGER': {
            'employees': {'read_team'},
            'attendance': {'read_team', 'approve'},
            'leave_management': {'read_team', 'approve'},
            'shifts': {'read_team'},
            'workload': {'read_team', 'balance'},
            'projects': {'read', 'write'},
            'tasks': {'read', 'write', 'assign'},
            'goals': {'read_team', 'write'},
            'performance': {'read_team', 'evaluate'},
            'timesheets': {'read_team', 'approve'},
            'expenses': {'read_team', 'approve'},
            'workplace': {'read', 'book'},
        },
        'STAFF_EMPLOYEE': {
            'employees': {'read_self', 'update_self'},
            'attendance': {'punch_in_out', 'read_self'},
            'leave_management': {'apply', 'read_self'},
            'tasks': {'read_assigned', 'update_status'},
            'goals': {'read_self', 'update_progress'},
            'performance': {'self_review'},
            'training': {'enroll', 'read_catalog'},
            'recognition': {'give_kudos', 'read_wall'},
            'expenses': {'submit_claim', 'read_self'},
            'helpdesk': {'raise_ticket', 'read_self'},
            'documents': {'read_self', 'upload'},
            'payroll': {'view_payslips', 'declare_tax'},
            'benefits': {'view_coverage', 'file_claim'},
            'timesheets': {'log_hours', 'submit_week'},
            'surveys': {'submit_feedback'},
            'workplace': {'book_desk', 'request_travel'},
        }
    }

    @classmethod
    def check_permission(cls, role: str, module: str, action: str) -> bool:
        role_key = role.upper()
        if role_key == 'ADMIN':
            return True
        allowed_actions = cls.MODULE_PERMISSIONS.get(role_key, {}).get(module, set())
        return action in allowed_actions
