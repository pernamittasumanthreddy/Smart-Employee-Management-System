from django.contrib import admin
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'survey_type', 'start_date', 'end_date', 'is_anonymous', 'is_active')

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'order', 'prompt_text', 'question_type')

@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'submitted_at', 'enps_score', 'sentiment_label')
