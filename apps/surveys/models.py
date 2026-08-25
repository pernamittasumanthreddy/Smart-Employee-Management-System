from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class Survey(models.Model):
    SURVEY_TYPES = [('ENPS', 'eNPS Quarterly Workforce Survey'), ('PULSE', 'Monthly Morale Pulse Check'), ('ONBOARDING', '30-Day Onboarding Feedback'), ('EXIT', 'Confidential Exit Survey'), ('CUSTOM', 'Custom Organizational Survey')]

    title = models.CharField(max_length=200)
    survey_type = models.CharField(max_length=30, choices=SURVEY_TYPES, default='ENPS')
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    is_anonymous = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    target_responses_count = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_survey_type_display()})"


class SurveyQuestion(models.Model):
    QUESTION_TYPES = [('RATING_10', '1-10 Scale (eNPS)'), ('RATING_5', '1-5 Stars (Likert Scale)'), ('TEXT', 'Open-Ended Qualitative Text'), ('CHOICE', 'Multiple Choice Single Selection')]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField(default=1)
    prompt_text = models.CharField(max_length=300, blank=True)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default='RATING_10')
    choices_csv = models.CharField(max_length=255, blank=True, help_text="Comma separated options if Multiple Choice")
    is_required = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __init__(self, *args, **kwargs):
        if 'question_text' in kwargs:
            kwargs['prompt_text'] = kwargs.pop('question_text')
        super().__init__(*args, **kwargs)

    @property
    def question_text(self):
        return self.prompt_text

    @question_text.setter
    def question_text(self, val):
        self.prompt_text = val

    def __str__(self):
        return f"Q{self.order}: {self.prompt_text}"


class SurveySubmission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='submissions')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, help_text="Null if 100% anonymous")
    submitted_at = models.DateTimeField(auto_now_add=True)
    enps_score = models.IntegerField(null=True, blank=True, help_text="0-10 rating")
    qualitative_feedback = models.TextField(blank=True)
    sentiment_label = models.CharField(max_length=30, choices=[('POSITIVE', 'Promoter / High Satisfaction'), ('PASSIVE', 'Passive / Neutral'), ('DETRACTOR', 'Detractor / At-Risk')], default='POSITIVE')

    def __str__(self):
        return f"Submission #{self.id} for {self.survey.title} ({self.sentiment_label})"


class SurveyAnswer(models.Model):
    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    rating_value = models.IntegerField(null=True, blank=True)
    text_answer = models.TextField(blank=True)

    def __str__(self):
        return f"Answer to {self.question} ({self.rating_value})"
