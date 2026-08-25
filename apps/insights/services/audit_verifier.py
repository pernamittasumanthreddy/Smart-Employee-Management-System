"""
Smart Enterprise Management System — Smart AI & Workforce ML Analytics Audit Trail Integrity Verifier
Attrition predictive models, flight risk scoring, and sentiment pulse.
"""

import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class AuditVerificationSummary:
    module_name: str
    total_events_checked: int
    is_chain_unbroken: bool
    tampered_event_indices: List[int]
    verification_hash: str
    verified_at: datetime


class InsightsAuditVerifier:
    """
    Cryptographic audit ledger hash-chain validator for Smart AI & Workforce ML Analytics.
    """

    @classmethod
    def verify_event_chain(
        cls,
        audit_events: List[Dict[str, Any]],
        expected_root_hash: Optional[str] = None
    ) -> AuditVerificationSummary:
        """
        Verifies SHA-256 integrity linking across consecutive audit ledger entries.
        """
        tampered = []
        prev_hash = "GENESIS"

        for idx, event in enumerate(audit_events):
            event_id = str(event.get('id', idx))
            action = str(event.get('action', 'UNKNOWN'))
            payload_str = f"{prev_hash}|{event_id}|{action}|insights"
            calculated_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()

            stored_hash = event.get('checksum')
            if stored_hash and stored_hash != calculated_hash:
                tampered.append(idx)

            prev_hash = calculated_hash

        is_valid = len(tampered) == 0

        return AuditVerificationSummary(
            module_name="insights",
            total_events_checked=len(audit_events),
            is_chain_unbroken=is_valid,
            tampered_event_indices=tampered,
            verification_hash=prev_hash,
            verified_at=datetime.now()
        )
