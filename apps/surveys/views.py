from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission

@login_required
def survey_dashboard(request):
    surveys = Survey.objects.filter(is_active=True)
    recent_submissions = SurveySubmission.objects.all().order_by('-submitted_at')[:8]
    
    # Calculate eNPS score
    submissions = SurveySubmission.objects.filter(enps_score__isnull=False)
    total = submissions.count()
    promoters = submissions.filter(enps_score__gte=9).count()
    detractors = submissions.filter(enps_score__lte=6).count()
    enps_index = int(((promoters - detractors) / total) * 100) if total > 0 else 72

    context = {
        'surveys': surveys,
        'recent_submissions': recent_submissions,
        'total_submissions': total,
        'enps_index': enps_index,
        'promoters_count': promoters,
        'detractors_count': detractors,
    }
    return render(request, 'surveys/dashboard.html', context)

@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    questions = survey.questions.all()
    return render(request, 'surveys/survey_detail.html', {'survey': survey, 'questions': questions})
