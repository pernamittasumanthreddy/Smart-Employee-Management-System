"""
Smart Employee Management System — Reporting Engine Audit Trail Ledger
Report generation runs, data exports, and audit requests.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class AuditLedgerEntry:
    entry_id: str
    module_name: str
    action_type: str # CREATE, UPDATE, DELETE, VIEW, EXPORT, APPROVE
    actor_user_id: int
    ip_address: str
    timestamp: datetime
    old_values: Dict[str, Any]
    new_values: Dict[str, Any]
    integrity_checksum: str


class ReportsAuditLogger:
    """
    Immutable audit trail recorder for Reporting Engine.
    """

    @classmethod
    def record_audit_event(
        cls,
        action: str,
        actor_id: int,
        ip: str,
        old_val: Dict[str, Any],
        new_val: Dict[str, Any]
    ) -> AuditLedgerEntry:
        import hashlib
        import uuid

        eid = str(uuid.uuid4())[:8].upper()
        now = datetime.now()
        raw_hash_data = f"{eid}|reports|{action}|{actor_id}|{now.isoformat()}"
        checksum = hashlib.sha256(raw_hash_data.encode('utf-8')).hexdigest()

        return AuditLedgerEntry(
            entry_id=f"AUD-REP-{eid}",
            module_name="reports",
            action_type=action,
            actor_user_id=actor_id,
            ip_address=ip or '127.0.0.1',
            timestamp=now,
            old_values=old_val,
            new_values=new_val,
            integrity_checksum=checksum
        )
