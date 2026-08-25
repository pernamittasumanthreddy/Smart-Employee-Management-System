import pytest
from django.utils import timezone
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission

@pytest.mark.django_db
def test_survey_and_enps():
    survey = Survey.objects.create(
        title="Q3 2026 Workforce eNPS Pulse",
        survey_type="ENPS",
        description="Confidential quarterly survey",
        end_date=timezone.now().date(),
        is_anonymous=True
    )
    q1 = SurveyQuestion.objects.create(
        survey=survey,
        order=1,
        prompt_text="How likely are you to recommend Bharat Enterprise Solutions as a great place to work?",
        question_type="RATING_10"
    )
    sub = SurveySubmission.objects.create(
        survey=survey,
        enps_score=10,
        sentiment_label='POSITIVE'
    )
    assert sub.enps_score == 10
    assert survey.questions.count() == 1
