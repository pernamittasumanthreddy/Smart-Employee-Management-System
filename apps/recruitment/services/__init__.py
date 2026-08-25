from decimal import Decimal
from django.db.models import Count, Avg
from apps.recruitment.models import JobRequisition, JobApplication, Candidate, InterviewSchedule, OfferLetter

class RecruitmentPipelineService:
    @staticmethod
    def get_pipeline_overview():
        total_open = JobRequisition.objects.filter(status='APPROVED').count()
        total_candidates = Candidate.objects.count()
        total_active_apps = JobApplication.objects.exclude(stage__in=['REJECTED', 'WITHDRAWN', 'HIRED']).count()
        total_offers = OfferLetter.objects.filter(status__in=['SENT', 'ACCEPTED']).count()
        
        stages_breakdown = JobApplication.objects.values('stage').annotate(count=Count('id')).order_by('stage')
        
        return {
            'total_open_positions': total_open,
            'total_candidates': total_candidates,
            'active_applications': total_active_apps,
            'offers_extended': total_offers,
            'stages_breakdown': list(stages_breakdown),
        }

    @staticmethod
    def advance_candidate_stage(application, target_stage, recruiter_user=None):
        application.stage = target_stage
        application.save()
        return application
