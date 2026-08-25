"""
Unit Tests for Resume Keyword Extractor and Match Scorer.
"""

import pytest
from apps.recruitment.services.resume_parser import ResumeParsingEngine


class TestResumeParsingEngine:
    def test_resume_skill_and_exp_extraction(self):
        text = """
        Rohit Verma - Lead Software Engineer
        Email: rohit.verma@example.com | Phone: (987) 654-3210
        Summary: 6+ years of experience developing web applications using Python, Django,
        PostgreSQL, Docker, React, and AWS cloud infrastructure. Holds a B.Tech in Computer Science.
        """
        required = ['Python', 'Django', 'PostgreSQL', 'AWS']
        profile = ResumeParsingEngine.parse_resume_text(text, required)
        assert profile.email == 'rohit.verma@example.com'
        assert profile.total_experience_years == 6.0
        assert profile.skill_match_percentage == 100.0
        assert profile.is_shortlisted
