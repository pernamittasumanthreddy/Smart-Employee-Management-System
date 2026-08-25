from typing import List, Dict, Any
from django.db.models import Count
from apps.recognition.models import Recognition
from apps.employees.models import Employee

class RecognitionGamificationEngine:
    '''
    Computes Kudos leaderboards, peer appreciation badges, core value champions,
    and annual rewards allocation.
    '''

    BADGE_TIERS = {
        'BRONZE_CHAMPION': {'min_kudos': 5, 'badge_title': 'Workplace Contributor (Bronze)'},
        'SILVER_HERO': {'min_kudos': 15, 'badge_title': 'Values Champion (Silver)'},
        'GOLD_LEGEND': {'min_kudos': 30, 'badge_title': 'Enterprise Beacon (Gold)'},
    }

    @classmethod
    def get_top_kudos_leaderboard(cls, limit: int = 10) -> List[Dict[str, Any]]:
        leaders = Recognition.objects.values('receiver__id', 'receiver__user__first_name', 'receiver__user__last_name')\
            .annotate(kudos_count=Count('id'))\
            .order_by('-kudos_count')[:limit]

        results = []
        for rank, row in enumerate(leaders, start=1):
            count = row['kudos_count']
            tier = 'NEWCOMER'
            if count >= 30:
                tier = 'GOLD_LEGEND'
            elif count >= 15:
                tier = 'SILVER_HERO'
            elif count >= 5:
                tier = 'BRONZE_CHAMPION'

            results.append({
                'rank': rank,
                'employee_id': row['receiver__id'],
                'full_name': f"{row['receiver__user__first_name']} {row['receiver__user__last_name']}".strip(),
                'total_kudos_received': count,
                'awarded_badge': cls.BADGE_TIERS.get(tier, {}).get('badge_title', 'Rising Star'),
            })
        return results
