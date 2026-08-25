from decimal import Decimal
from typing import List, Dict, Any
from django.db.models import Count, Avg
from apps.employees.models import Employee
from apps.skills.models import Skill, EmployeeSkill

class SkillMatrixAnalyticsService:
    '''
    Analyzes organizational competency distributions, skill gaps across departments,
    critical single points of failure (SPOFs), and training recommendation paths.
    '''

    @staticmethod
    def compute_department_skill_gap(department_id: int) -> Dict[str, Any]:
        employees = Employee.objects.filter(department_id=department_id)
        total_emp = employees.count()
        if total_emp == 0:
            return {'total_employees': 0, 'skill_coverage': {}, 'critical_gaps': []}

        skills = Skill.objects.all()
        coverage_data = {}
        critical_gaps = []

        for skill in skills:
            emp_with_skill = EmployeeSkill.objects.filter(employee__in=employees, skill=skill)
            count = emp_with_skill.count()
            avg_rating = emp_with_skill.aggregate(avg=Avg('proficiency_level'))['avg'] or 0.0
            
            coverage_pct = round((count / total_emp) * 100.0, 1)
            coverage_data[skill.name] = {
                'headcount': count,
                'coverage_percentage': coverage_pct,
                'avg_proficiency': round(float(avg_rating), 1),
            }

            if count <= 1 and total_emp >= 5:
                critical_gaps.append({
                    'skill_name': skill.name,
                    'current_certified_staff': count,
                    'risk_level': 'HIGH_SINGLE_POINT_OF_FAILURE',
                })

        return {
            'total_employees': total_emp,
            'skill_coverage': coverage_data,
            'critical_gaps': critical_gaps,
        }

    @staticmethod
    def identify_mentorship_pairs() -> List[Dict[str, Any]]:
        pairs = []
        skills = Skill.objects.all()[:10]
        for skill in skills:
            experts = EmployeeSkill.objects.filter(skill=skill, proficiency_level__gte=4).select_related('employee')
            learners = EmployeeSkill.objects.filter(skill=skill, proficiency_level__lte=2).select_related('employee')
            
            if experts.exists() and learners.exists():
                pairs.append({
                    'skill_name': skill.name,
                    'mentor': experts.first().employee.full_name,
                    'mentee': learners.first().employee.full_name,
                    'target_level': 4,
                })
        return pairs
