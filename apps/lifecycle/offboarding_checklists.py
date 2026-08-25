from typing import List, Dict, Any

class OffboardingChecklistManager:
    '''
    Multi-Departmental clearance checklist generator for employee exit workflows.
    '''

    DEPARTMENT_TASKS = {
        'IT': ['MacBook / Hardware Return', 'VPN & SSO Account Revocation', 'Access Card Deactivation'],
        'FINANCE': ['Travel Advance Settlement', 'Corporate Credit Card Closure', 'Final Settlement (FnF)'],
        'ADMIN': ['Library Books Return', 'Locker Key Handover', 'Parking Permit Surrender'],
        'HR': ['Exit Interview Questionnaire', 'Experience Certificate Generation', 'Gratuity / PF Transfer Guidance'],
    }

    @classmethod
    def generate_clearance_matrix(cls) -> Dict[str, List[str]]:
        return cls.DEPARTMENT_TASKS
