from django.utils import timezone

from apps.insights.models import InsightCategory, InsightSeverity
from apps.skills.models import EmployeeSkill, SkillProficiency
from apps.training.models import Course, EnrollmentStatus, TrainingEnrollment


class TrainingAnalyzer:
    """
    Analyzes workforce skill gaps and certification expirations to generate
    targeted upskilling course recommendations.
    """

    @classmethod
    def analyze_training_needs(cls, employee):
        insights = []
        today = timezone.now().date()
        sixty_days = today + timezone.timedelta(days=60)

        # 1. Expiring Certifications
        expiring = TrainingEnrollment.objects.filter(
            employee=employee,
            status=EnrollmentStatus.COMPLETED,
            certificate_expiry_date__isnull=False,
            certificate_expiry_date__lte=sixty_days
        )

        for cert in expiring:
            days_left = (cert.certificate_expiry_date - today).days
            insights.append({
                'category': InsightCategory.TRAINING,
                'severity': InsightSeverity.HIGH if days_left <= 15 else InsightSeverity.MEDIUM,
                'employee': employee,
                'department': employee.department,
                'title': f"Certification Expiring in {max(0, days_left)} Days: {cert.course.title}",
                'what_detected': f"Professional certificate for '{cert.course.title}' expires on {cert.certificate_expiry_date}.",
                'why_detected': "Certificate expiration date is within active renewal window (< 60 days).",
                'supporting_data': {
                    'course_title': cert.course.title,
                    'expiry_date': str(cert.certificate_expiry_date),
                    'days_remaining': days_left
                },
                'recommendation': "Enroll in recertification refresher training to maintain compliance.",
                'confidence_score': 0.99
            })

        # 2. Skill Gap to Course Matching
        beginner_skills = EmployeeSkill.objects.filter(
            employee=employee,
            proficiency_level=SkillProficiency.BEGINNER
        ).select_related('skill__category')

        for emp_skill in beginner_skills:
            matching_course = Course.objects.filter(
                category=emp_skill.skill.category,
                is_active=True
            ).exclude(enrollments__employee=employee).first()

            if matching_course:
                insights.append({
                    'category': InsightCategory.TRAINING,
                    'severity': InsightSeverity.LOW,
                    'employee': employee,
                    'department': employee.department,
                    'title': f"Recommended Upskilling: '{matching_course.title}'",
                    'what_detected': f"Identified opportunity to elevate proficiency in '{emp_skill.skill.name}' from Beginner to Advanced.",
                    'why_detected': f"Employee holds Beginner proficiency in '{emp_skill.skill.name}' and internal academy offers matched course '{matching_course.title}'.",
                    'supporting_data': {
                        'skill_name': emp_skill.skill.name,
                        'current_proficiency': emp_skill.get_proficiency_level_display(),
                        'recommended_course': matching_course.title,
                        'duration_hours': float(matching_course.duration_hours)
                    },
                    'recommendation': f"Enroll {employee.first_name} in '{matching_course.title}' ({matching_course.duration_hours} hrs).",
                    'confidence_score': 0.90
                })

        return insights
