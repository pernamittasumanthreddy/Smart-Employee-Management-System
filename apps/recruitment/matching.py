import re
from decimal import Decimal
from typing import List, Dict, Set, Any

class CandidateMatchingEngine:
    '''
    Algorithmic matching engine that analyzes candidate skill profiles, experience levels,
    location compatibility, notice periods, and compensation expectations against Job Requisition criteria.
    '''

    @staticmethod
    def extract_keywords(text: str) -> Set[str]:
        if not text:
            return set()
        clean = re.sub(r'[^a-zA-Z0-9\s+#]', ' ', text.lower())
        tokens = [t.strip() for t in clean.split() if len(t.strip()) > 1]
        stopwords = {'and', 'the', 'for', 'with', 'in', 'of', 'on', 'at', 'to', 'a', 'is', 'an', 'as', 'by'}
        return {t for t in tokens if t not in stopwords}

    @classmethod
    def calculate_skill_match_score(cls, candidate_skills: str, required_skills: str) -> Decimal:
        cand_set = cls.extract_keywords(candidate_skills)
        req_set = cls.extract_keywords(required_skills)
        
        if not req_set:
            return Decimal('100.00')
        if not cand_set:
            return Decimal('40.00')

        intersection = cand_set.intersection(req_set)
        score = (Decimal(len(intersection)) / Decimal(len(req_set))) * Decimal('100.00')
        return min(Decimal('100.00'), max(Decimal('20.00'), score)).quantize(Decimal('0.01'))

    @classmethod
    def calculate_overall_match_index(cls, candidate, requisition) -> Dict[str, Any]:
        # 1. Skill Score (40% weight)
        skill_score = cls.calculate_skill_match_score(candidate.skills_summary, requisition.required_skills)
        
        # 2. Experience Score (25% weight)
        exp_score = Decimal('100.00')
        if candidate.total_experience_years < requisition.min_experience_years:
            deficit = requisition.min_experience_years - candidate.total_experience_years
            exp_score = max(Decimal('20.00'), Decimal('100.00') - (deficit * Decimal('25.00')))
        elif candidate.total_experience_years > (requisition.max_experience_years + Decimal('3.0')):
            exp_score = Decimal('85.00')

        # 3. Budget / CTC Score (20% weight)
        budget_score = Decimal('100.00')
        if candidate.expected_ctc > requisition.budget_max:
            excess_pct = ((candidate.expected_ctc - requisition.budget_max) / requisition.budget_max) * Decimal('100.00')
            budget_score = max(Decimal('10.00'), Decimal('100.00') - excess_pct)

        # 4. Notice Period Score (15% weight)
        notice_score = Decimal('100.00')
        if candidate.notice_period_days > 60:
            notice_score = Decimal('60.00')
        elif candidate.notice_period_days > 30:
            notice_score = Decimal('80.00')

        # Composite Score
        composite = (
            (skill_score * Decimal('0.40')) +
            (exp_score * Decimal('0.25')) +
            (budget_score * Decimal('0.20')) +
            (notice_score * Decimal('0.15'))
        ).quantize(Decimal('0.01'))

        is_recommended = composite >= Decimal('75.00')

        return {
            'composite_score': composite,
            'skill_score': skill_score,
            'experience_score': exp_score,
            'budget_score': budget_score,
            'notice_score': notice_score,
            'is_recommended': is_recommended,
        }
