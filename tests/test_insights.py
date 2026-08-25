import pytest
from apps.insights.insight_service import SmartInsightService
from apps.insights.models import SmartInsight

@pytest.mark.django_db
def test_insights_generation():
    count = SmartInsightService.run_full_system_analysis()
    assert isinstance(count, int)
