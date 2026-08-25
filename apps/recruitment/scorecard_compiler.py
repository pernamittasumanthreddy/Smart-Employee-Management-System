from decimal import Decimal
from typing import List, Dict, Any

class InterviewScorecardCompiler:
    '''
    Aggregates multi-round interview ratings with weighted domain competencies:
    - Core Technical Architecture (40%)
    - Problem Solving & Algorithmic Design (25%)
    - Communication & Leadership Impact (20%)
    - Cultural Alignment & Core Values (15%)
    '''

    WEIGHTS = {
        'technical': Decimal('0.40'),
        'problem_solving': Decimal('0.25'),
        'communication': Decimal('0.20'),
        'culture': Decimal('0.15'),
    }

    @classmethod
    def compute_composite_rating(cls, tech: int, ps: int, comm: int, cult: int) -> Dict[str, Any]:
        composite = (
            (Decimal(str(tech)) * cls.WEIGHTS['technical']) +
            (Decimal(str(ps)) * cls.WEIGHTS['problem_solving']) +
            (Decimal(str(comm)) * cls.WEIGHTS['communication']) +
            (Decimal(str(cult)) * cls.WEIGHTS['culture'])
        ).quantize(Decimal('0.01'))

        hiring_verdict = "REJECT"
        if composite >= Decimal('4.50'):
            hiring_verdict = "STRONG_HIRE"
        elif composite >= Decimal('3.75'):
            hiring_verdict = "HIRE"
        elif composite >= Decimal('3.00'):
            hiring_verdict = "LEAN_HIRE"

        return {
            'composite_rating': float(composite),
            'max_possible': 5.0,
            'hiring_verdict': hiring_verdict,
            'is_above_bar': composite >= Decimal('3.75'),
        }
