import re
from typing import Dict, Any, List

class WorkforceSentimentAnalyzer:
    '''
    Lexicon and rule-based sentiment classifier for employee pulse feedback,
    open-ended survey responses, and exit interview commentaries.
    '''

    POSITIVE_WORDS = {
        'great', 'excellent', 'supportive', 'transparent', 'growth', 'innovative',
        'proud', 'collaborative', 'empowering', 'trust', 'visionary', 'rewarding'
    }
    NEGATIVE_WORDS = {
        'burnout', 'overworked', 'toxic', 'micromanagement', 'stress', 'delayed',
        'frustrated', 'unclear', 'bias', 'underpaid', 'bureaucracy', 'isolated'
    }

    @classmethod
    def analyze_feedback_text(cls, text: str) -> Dict[str, Any]:
        if not text:
            return {'sentiment': 'NEUTRAL', 'score': 0.0, 'positive_count': 0, 'negative_count': 0}

        words = re.findall(r'\w+', text.lower())
        pos_count = sum(1 for w in words if w in cls.POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in cls.NEGATIVE_WORDS)

        net_score = pos_count - neg_count
        sentiment = 'NEUTRAL'
        if net_score > 0:
            sentiment = 'POSITIVE'
        elif net_score < 0:
            sentiment = 'NEGATIVE'

        return {
            'sentiment': sentiment,
            'net_score': net_score,
            'positive_word_count': pos_count,
            'negative_word_count': neg_count,
            'word_count': len(words),
        }
