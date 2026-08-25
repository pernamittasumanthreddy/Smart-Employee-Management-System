"""
Unit Tests for Workplace Feedback Sentiment Analyzer.
"""

import pytest
from apps.insights.services.sentiment_analyzer import WorkplaceSentimentAnalyzer


class TestWorkplaceSentimentAnalyzer:
    def test_positive_feedback_analysis(self):
        text = "The leadership team is very supportive and collaborative. Great growth environment!"
        res = WorkplaceSentimentAnalyzer.analyze_feedback_text(text)
        assert res['sentiment'] == 'POSITIVE'
        assert res['score'] > 0.3
        assert 'supportive' in res['positive_hits']

    def test_negative_burnout_feedback(self):
        text = "Severe micromanagement and toxic deadlines. Everyone is exhausted and overworked."
        res = WorkplaceSentimentAnalyzer.analyze_feedback_text(text)
        assert res['sentiment'] == 'NEGATIVE'
        assert res['score'] < -0.3
        assert 'toxic' in res['negative_hits']

    def test_negated_sentiment(self):
        text = "The working culture is not supportive and there is no transparent leadership."
        res = WorkplaceSentimentAnalyzer.analyze_feedback_text(text)
        assert res['sentiment'] == 'NEGATIVE'
