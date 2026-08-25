"""
Candidate Resume Keyword & Experience Parsing Engine:
Extracts tech stacks, years of experience, qualification degrees,
contact credentials, and computes job-match relevance scores.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass
class CandidateResumeProfile:
    candidate_name: str
    email: str
    phone: str
    total_experience_years: float
    detected_skills: List[str]
    matched_job_skills: List[str]
    missing_job_skills: List[str]
    skill_match_percentage: float
    education_degrees: List[str]
    is_shortlisted: bool


class ResumeParsingEngine:
    """
    Rule-based resume keyword extractor and skill matching calculator.
    """

    KNOWN_SKILLS = {
        'python', 'django', 'fastapi', 'flask', 'javascript', 'typescript',
        'react', 'next.js', 'vue', 'node.js', 'postgresql', 'mysql', 'redis',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'git',
        'rest api', 'graphql', 'html5', 'css3', 'bootstrap', 'tailwind',
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'celery'
    }

    DEGREE_PATTERNS = [
        r'(b\.?tech|b\.?e|m\.?tech|m\.?e|bca|mca|b\.?sc|m\.?sc|mba|bba|ph\.?d)'
    ]

    @classmethod
    def parse_resume_text(cls, text: str, required_skills: List[str]) -> CandidateResumeProfile:
        text_lower = text.lower()

        # Extract Email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0) if email_match else 'unknown@candidate.com'

        # Extract Phone
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        phone = phone_match.group(0) if phone_match else 'N/A'

        # Extract Experience Years (e.g. "5 years of experience" or "7+ yrs")
        exp_match = re.search(r'(\d+(\.\d+)?)\+?\s*(years?|yrs?)\s*(of)?\s*(experience|exp)', text_lower)
        exp_years = float(exp_match.group(1)) if exp_match else 2.0

        # Extract Skills
        detected = []
        for skill in cls.KNOWN_SKILLS:
            if skill in text_lower:
                detected.append(skill.title())

        # Match against required skills
        matched = []
        missing = []
        for req in required_skills:
            if req.lower() in text_lower:
                matched.append(req)
            else:
                missing.append(req)

        match_rate = (len(matched) / len(required_skills) * 100.0) if required_skills else 100.0
        shortlisted = match_rate >= 60.0 and exp_years >= 1.0

        # Degrees
        degrees = []
        for pat in cls.DEGREE_PATTERNS:
            found = re.findall(pat, text_lower, re.IGNORECASE)
            degrees.extend([d.upper() for d in found])

        return CandidateResumeProfile(
            candidate_name='Extracted Applicant',
            email=email,
            phone=phone,
            total_experience_years=exp_years,
            detected_skills=detected,
            matched_job_skills=matched,
            missing_job_skills=missing,
            skill_match_percentage=round(match_rate, 1),
            education_degrees=list(set(degrees)) or ['B.TECH'],
            is_shortlisted=shortlisted
        )
