"""
Smart Employee Management System — Reporting Engine State Transition Workflow Processor
Report generation runs, data exports, and audit requests.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowStateTransition:
    entity_id: int
    from_state: str
    to_state: str
    actor_id: int
    timestamp: datetime
    is_valid: bool
    transition_notes: str


class ReportsWorkflowProcessor:
    """
    State machine and transition validator for Reporting Engine.
    """

    ALLOWED_TRANSITIONS = {
        'DRAFT': ['PENDING_REVIEW', 'SUBMITTED', 'CANCELLED'],
        'PENDING_REVIEW': ['APPROVED', 'REJECTED', 'QUERY_RAISED'],
        'QUERY_RAISED': ['PENDING_REVIEW', 'CANCELLED'],
        'APPROVED': ['IN_PROGRESS', 'SETTLED', 'COMPLETED', 'ARCHIVED'],
        'REJECTED': ['DRAFT', 'ARCHIVED'],
        'COMPLETED': ['ARCHIVED'],
        'CANCELLED': ['ARCHIVED'],
    }

    @classmethod
    def process_transition(
        cls,
        entity_id: int,
        current_state: str,
        target_state: str,
        actor_id: int,
        notes: str = ''
    ) -> WorkflowStateTransition:
        allowed = cls.ALLOWED_TRANSITIONS.get(current_state, [])
        is_valid = target_state in allowed

        transition_msg = f"Transition from {current_state} to {target_state} by user {actor_id}."
        if not is_valid:
            transition_msg = f"Invalid transition: {current_state} cannot move to {target_state}."

        return WorkflowStateTransition(
            entity_id=entity_id,
            from_state=current_state,
            to_state=target_state if is_valid else current_state,
            actor_id=actor_id,
            timestamp=datetime.now(),
            is_valid=is_valid,
            transition_notes=notes or transition_msg
        )
