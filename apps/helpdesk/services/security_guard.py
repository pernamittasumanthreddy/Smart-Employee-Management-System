"""
Smart Enterprise Management System — IT & HR Service Desk Helpdesk Security Guard & Access Enforcement
SLA breach timers, priority routing, and multi-tier escalations.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SecurityAuthorizationResult:
    is_authorized: bool
    access_level: str # FULL_CONTROL, READ_WRITE, READ_ONLY, DENIED
    reason: str
    required_permissions: List[str]
    missing_permissions: List[str]


class HelpdeskSecurityGuard:
    """
    Granular permission gatekeeper and authorization barrier for IT & HR Service Desk Helpdesk.
    """

    PERMISSION_HIERARCHY = {
        'ADMIN': ['*'],
        'HR': ['view', 'create', 'update', 'export'],
        'MANAGER': ['view', 'create', 'approve'],
        'EMPLOYEE': ['view_self', 'create_self'],
        'GUEST': ['view_public']
    }

    @classmethod
    def authorize_action(
        cls,
        user_id: int,
        user_role: str,
        requested_action: str,
        resource_owner_id: Optional[int] = None
    ) -> SecurityAuthorizationResult:
        role_caps = cls.PERMISSION_HIERARCHY.get(user_role.upper(), ['view_public'])

        # Admin has root override
        if '*' in role_caps or 'ADMIN' in user_role.upper():
            return SecurityAuthorizationResult(
                is_authorized=True,
                access_level='FULL_CONTROL',
                reason='Administrative superuser grant.',
                required_permissions=[requested_action],
                missing_permissions=[]
            )

        # Self-service actions
        is_self = resource_owner_id is not None and user_id == resource_owner_id
        if is_self and f"{requested_action}_self" in role_caps:
            return SecurityAuthorizationResult(
                is_authorized=True,
                access_level='READ_WRITE',
                reason='Self-service resource authorization.',
                required_permissions=[f"{requested_action}_self"],
                missing_permissions=[]
            )

        if requested_action in role_caps:
            return SecurityAuthorizationResult(
                is_authorized=True,
                access_level='READ_WRITE',
                reason='Role capabilities matched.',
                required_permissions=[requested_action],
                missing_permissions=[]
            )

        return SecurityAuthorizationResult(
            is_authorized=False,
            access_level='DENIED',
            reason=f"Role '{user_role}' lacks permission '{requested_action}' on helpdesk.",
            required_permissions=[requested_action],
            missing_permissions=[requested_action]
        )
