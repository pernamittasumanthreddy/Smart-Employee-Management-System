from typing import Dict, List, Any

class AutomationTriggerRegistry:
    '''
    Central event trigger registry mapping business domain events to executable action pipelines.
    '''

    REGISTERED_TRIGGERS = [
        ('EMPLOYEE_ONBOARDED', 'Triggered when a new employee joins the organization'),
        ('LEAVE_APPROVED', 'Triggered when a manager approves a leave request'),
        ('PAYROLL_DISBURSED', 'Triggered when monthly payslips are finalized and bank files exported'),
        ('EXPENSE_SUBMITTED', 'Triggered when an expense claim exceeds threshold approval limit'),
        ('TICKET_ESCALATED', 'Triggered when support ticket breaches priority SLA deadline'),
        ('SURVEY_PUBLISHED', 'Triggered when a quarterly eNPS survey is launched'),
    ]

    @classmethod
    def list_triggers(cls) -> List[Dict[str, str]]:
        return [{'event': code, 'description': desc} for code, desc in cls.REGISTERED_TRIGGERS]
