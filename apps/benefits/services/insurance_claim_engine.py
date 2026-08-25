"""
Corporate Group Health & Term Insurance Claim Adjudication Engine:
Computes cashless hospital authorization, room rent capping, co-pay deductions,
maternity cover sub-limits, and corporate buffer approval workflows.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional


@dataclass
class InsuranceClaimAdjudication:
    claim_id: str
    employee_id: int
    patient_name: str
    total_hospital_bill: Decimal
    admissible_amount: Decimal
    room_rent_deduction: Decimal
    co_pay_deduction: Decimal
    non_medical_expenses_deduction: Decimal
    corporate_buffer_applied: Decimal
    final_settled_amount: Decimal
    claim_status: str # APPROVED, REJECTED, QUERY_RAISED, SETTLED
    settlement_notes: List[str]


class InsuranceClaimEngine:
    """
    Automated insurance claim settlement and sub-limit validator.
    """

    ROOM_RENT_CAPPING_PERCENT = Decimal('0.01') # 1% of Sum Insured per day
    CO_PAY_RATE = Decimal('0.10') # 10% co-pay for parents

    @classmethod
    def adjudicate_claim(
        cls,
        claim_id: str,
        emp_id: int,
        patient_name: str,
        is_parent: bool,
        sum_insured: Decimal,
        hospital_bill: Decimal,
        room_rent_per_day: Decimal,
        hospitalization_days: int,
        non_medical_charges: Decimal,
        corporate_buffer_available: Decimal = Decimal('50000.00')
    ) -> InsuranceClaimAdjudication:
        notes = []

        # 1. Non-medical deductions (Gloves, admin charges, PPE, consumables)
        admissible_before_limits = max(Decimal('0.00'), hospital_bill - non_medical_charges)
        if non_medical_charges > 0:
            notes.append(f"Deducted non-medical consumables of Rs. {non_medical_charges}.")

        # 2. Room rent capping limit check
        daily_limit = sum_insured * cls.ROOM_RENT_CAPPING_PERCENT
        allowed_room_rent = daily_limit * Decimal(str(hospitalization_days))
        actual_room_rent = room_rent_per_day * Decimal(str(hospitalization_days))

        room_rent_deduction = Decimal('0.00')
        if actual_room_rent > allowed_room_rent:
            # Proportionate deduction penalty
            room_rent_deduction = actual_room_rent - allowed_room_rent
            notes.append(f"Room rent exceeded policy daily limit (Limit: Rs. {daily_limit}/day, Actual: Rs. {room_rent_per_day}/day). Proportionate deduction: Rs. {room_rent_deduction}.")

        admissible_after_room = max(Decimal('0.00'), admissible_before_limits - room_rent_deduction)

        # 3. Co-pay calculation
        co_pay_amount = Decimal('0.00')
        if is_parent:
            co_pay_amount = (admissible_after_room * cls.CO_PAY_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            notes.append(f"10% Parental co-pay applied: Rs. {co_pay_amount}.")

        final_payable = max(Decimal('0.00'), admissible_after_room - co_pay_amount)

        # 4. Corporate buffer check if bill exceeds sum insured
        buffer_used = Decimal('0.00')
        if final_payable > sum_insured:
            excess = final_payable - sum_insured
            if corporate_buffer_available >= excess:
                buffer_used = excess
                notes.append(f"Corporate Executive Buffer of Rs. {buffer_used} applied for excess hospitalization.")
            else:
                final_payable = sum_insured
                notes.append(f"Claim capped at policy Sum Insured limit of Rs. {sum_insured}.")

        return InsuranceClaimAdjudication(
            claim_id=claim_id,
            employee_id=emp_id,
            patient_name=patient_name,
            total_hospital_bill=hospital_bill,
            admissible_amount=admissible_before_limits,
            room_rent_deduction=room_rent_deduction,
            co_pay_deduction=co_pay_amount,
            non_medical_expenses_deduction=non_medical_charges,
            corporate_buffer_applied=buffer_used,
            final_settled_amount=final_payable,
            claim_status='APPROVED',
            settlement_notes=notes
        )
