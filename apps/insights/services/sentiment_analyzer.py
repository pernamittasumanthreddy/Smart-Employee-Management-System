"""
Rule-Based Natural Language Sentiment & Workplace Pulse Analyzer:
Evaluates employee feedback, exit interviews, and engagement surveys.
"""

from typing import Dict, List, Tuple


class WorkplaceSentimentAnalyzer:
    """
    Lexicon and rule-based sentiment parser for workplace analytics.
    """

    POSITIVE_WORDS = {
        'excellent', 'great', 'awesome', 'supportive', 'collaborative', 'empowering',
        'transparent', 'growth', 'innovative', 'rewarding', 'balanced', 'fair',
        'proud', 'enjoy', 'motivated', 'productive', 'friendly', 'respectful',
        'promising', 'leadership', 'encouraging', 'inclusive', 'healthy', 'thriving'
    }

    NEGATIVE_WORDS = {
        'burnout', 'toxic', 'stressful', 'micromanagement', 'unfair', 'delayed',
        'overworked', 'disappointed', 'stagnant', 'frustrating', 'politics',
        'poor', 'ignored', 'hostile', 'unsupported', 'chaotic', 'exhausted',
        'underpaid', 'unrealistic', 'favoritism', 'isolated', 'demoralizing'
    }

    INTENSIFIERS = {'very', 'extremely', 'highly', 'deeply', 'absolutely', 'truly'}
    NEGATIONS = {'not', 'never', 'hardly', 'barely', 'scarcely', 'no', 'without'}

    @classmethod
    def analyze_feedback_text(cls, text: str) -> Dict[str, any]:
        if not text or not text.strip():
            return {'score': 0.0, 'sentiment': 'NEUTRAL', 'positive_hits': [], 'negative_hits': []}

        words = [w.strip('.,!?;:"()[]{}').lower() for w in text.split()]
        pos_score = 0.0
        neg_score = 0.0
        pos_hits = []
        neg_hits = []

        is_negated = False
        multiplier = 1.0

        for i, word in enumerate(words):
            if word in cls.NEGATIONS:
                is_negated = True
                continue
            if word in cls.INTENSIFIERS:
                multiplier = 1.6
                continue

            if word in cls.POSITIVE_WORDS:
                if is_negated:
                    neg_score += 1.0 * multiplier
                    neg_hits.append(f"not {word}")
                else:
                    pos_score += 1.0 * multiplier
                    pos_hits.append(word)
                is_negated = False
                multiplier = 1.0
            elif word in cls.NEGATIVE_WORDS:
                if is_negated:
                    pos_score += 0.8 * multiplier
                    pos_hits.append(f"not {word}")
                else:
                    neg_score += 1.0 * multiplier
                    neg_hits.append(word)
                is_negated = False
                multiplier = 1.0

        total_hits = pos_score + neg_score
        if total_hits == 0:
            score = 0.0
            sentiment = 'NEUTRAL'
        else:
            score = (pos_score - neg_score) / (pos_score + neg_score)
            if score >= 0.25:
                sentiment = 'POSITIVE'
            elif score <= -0.25:
                sentiment = 'NEGATIVE'
            else:
                sentiment = 'NEUTRAL'

        return {
            'score': round(score, 2),
            'sentiment': sentiment,
            'positive_score': round(pos_score, 1),
            'negative_score': round(neg_score, 1),
            'positive_hits': list(set(pos_hits)),
            'negative_hits': list(set(neg_hits))
        }
