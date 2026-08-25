from apps.insights.models import InsightCategory, InsightSeverity
from apps.projects.models import Project, ProjectStatus
from apps.skills.models import EmployeeSkill, SkillProficiency


class SkillAnalyzer:
    """
    Evaluates project skill demands against employee competencies to detect
    critical staffing gaps and department skill shortages.
    """

    PROFICIENCY_SCORES = {
        SkillProficiency.BEGINNER: 1,
        SkillProficiency.INTERMEDIATE: 2,
        SkillProficiency.ADVANCED: 3,
        SkillProficiency.EXPERT: 4,
    }

    @classmethod
    def analyze_project_skill_gaps(cls):
        active_projects = Project.objects.filter(status=ProjectStatus.ACTIVE).prefetch_related('required_skills__skill', 'members__skills__skill')
        insights = []

        for project in active_projects:
            reqs = project.required_skills.all()
            if not reqs.exists():
                continue

            members = project.members.all()
            for req in reqs:
                target_score = cls.PROFICIENCY_SCORES.get(req.min_proficiency, 2)
                matching_members = []

                for m in members:
                    emp_skill = m.skills.filter(skill=req.skill).first()
                    if emp_skill:
                        emp_score = cls.PROFICIENCY_SCORES.get(emp_skill.proficiency_level, 1)
                        if emp_score >= target_score:
                            matching_members.append(m)

                if len(matching_members) == 0:
                    # Project has an unfulfilled skill requirement among assigned members!
                    # Find other company employees who possess this skill
                    available_experts = EmployeeSkill.objects.filter(
                        skill=req.skill,
                        proficiency_level__in=[SkillProficiency.ADVANCED, SkillProficiency.EXPERT],
                        employee__employment_status='ACTIVE'
                    ).exclude(employee__in=members).select_related('employee__department')[:3]

                    rec_candidates = ", ".join([f"{ae.employee.full_name} ({ae.get_proficiency_level_display()})" for ae in available_experts])

                    insights.append({
                        'category': InsightCategory.SKILL,
                        'severity': InsightSeverity.HIGH,
                        'employee': None,
                        'department': project.manager.department if project.manager else None,
                        'title': f"Critical Skill Gap: Project '{project.name}' lacks '{req.skill.name}'",
                        'what_detected': f"No assigned member on active project '{project.name}' meets the required proficiency ({req.get_min_proficiency_display()}) for '{req.skill.name}'.",
                        'why_detected': f"0 of {members.count()} project team members meet required competency level ({target_score}/4).",
                        'supporting_data': {
                            'project_code': project.code,
                            'required_skill': req.skill.name,
                            'min_proficiency': req.get_min_proficiency_display(),
                            'available_internal_candidates': [ae.employee.full_name for ae in available_experts]
                        },
                        'recommendation': f"Assign skilled internal staff ({rec_candidates if rec_candidates else 'External hiring/upskilling needed'}) or enroll a current team member in relevant training.",
                        'confidence_score': 0.96
                    })

        return insights
