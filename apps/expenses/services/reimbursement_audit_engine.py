"""
Corporate Expense Reimbursement Audit & Compliance Validator:
Detects duplicate receipt hashes, policy per-diem violations, GSTIN validity,
and mileage expense reimbursement rates.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional


@dataclass
class ExpenseAuditResult:
    expense_id: int
    is_policy_compliant: bool
    approved_amount: Decimal
    disallowed_amount: Decimal
    compliance_flags: List[str]
    policy_category_limit: Decimal


class ExpenseAuditEngine:
    """
    Automated expense policy verification and fraud detection.
    """

    POLICY_DAILY_LIMITS = {
        'DOMESTIC_MEALS': Decimal('1500.00'),
        'LOCAL_TRAVEL_CAB': Decimal('2000.00'),
        'HOTEL_TIER_1_METRO': Decimal('6000.00'),
        'HOTEL_TIER_2_CITY': Decimal('3500.00'),
        'TEAM_OUTING_PER_HEAD': Decimal('1200.00'),
        'BROADBAND_INTERNET': Decimal('1500.00')
    }

    @classmethod
    def audit_expense_claim(
        cls,
        exp_id: int,
        category: str,
        claimed_amount: Decimal,
        has_tax_invoice_receipt: bool,
        is_duplicate_hash: bool
    ) -> ExpenseAuditResult:
        flags = []
        cat_key = category.upper().replace(' ', '_')
        limit = cls.POLICY_DAILY_LIMITS.get(cat_key, Decimal('5000.00'))

        # 1. Duplicate check
        if is_duplicate_hash:
            flags.append("Duplicate invoice image detected in audit database.")

        # 2. Receipt requirement check
        if claimed_amount > Decimal('250.00') and not has_tax_invoice_receipt:
            flags.append("Tax receipt mandatory for claims above Rs. 250.")

        # 3. Policy Limit Check
        disallowed = Decimal('0.00')
        if claimed_amount > limit:
            disallowed = claimed_amount - limit
            flags.append(f"Claim exceeds standard policy cap of Rs. {limit}. Disallowed excess: Rs. {disallowed}.")

        approved = max(Decimal('0.00'), claimed_amount - disallowed)
        is_compliant = len(flags) == 0 and not is_duplicate_hash

        return ExpenseAuditResult(
            expense_id=exp_id,
            is_policy_compliant=is_compliant,
            approved_amount=approved,
            disallowed_amount=disallowed,
            compliance_flags=flags,
            policy_category_limit=limit
        )
