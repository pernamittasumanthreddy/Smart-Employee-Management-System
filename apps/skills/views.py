from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.employees.models import Employee
from apps.organization.models import Department
from apps.permissions.decorators import manager_or_above_required
from apps.skills.forms import EmployeeSkillForm
from apps.skills.models import (
    EmployeeSkill,
    Skill,
    SkillCategory,
)


@login_required
def skill_catalog_view(request):
    categories = SkillCategory.objects.all().prefetch_related('skills__employee_skills')
    return render(request, 'skills/catalog.html', {'categories': categories})

@login_required
def my_skills_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    my_skills = EmployeeSkill.objects.filter(employee=employee).select_related('skill__category')
    form = EmployeeSkillForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        skill_obj = form.save(commit=False)
        skill_obj.employee = employee
        skill_obj.save()
        messages.success(request, f"Skill '{skill_obj.skill.name}' added to your profile.")
        return redirect('skills:my_skills')

    return render(request, 'skills/my_skills.html', {
        'my_skills': my_skills,
        'form': form,
    })

@login_required
def skill_matrix_view(request):
    """
    Renders the workforce Skill Matrix Heatmap cross-referencing employees vs core competencies.
    """
    dept_id = request.GET.get('department')
    employees = Employee.objects.filter(employment_status='ACTIVE').select_related('department', 'designation')
    if dept_id:
        employees = employees.filter(department_id=dept_id)

    skills = Skill.objects.all().select_related('category')[:15]
    departments = Department.objects.filter(is_active=True)

    # Build matrix map: {employee_id: {skill_id: proficiency_level}}
    emp_skills = EmployeeSkill.objects.filter(employee__in=employees).values('employee_id', 'skill_id', 'proficiency_level')
    matrix_map = {}
    for item in emp_skills:
        matrix_map.setdefault(item['employee_id'], {})[item['skill_id']] = item['proficiency_level']

    matrix_rows = []
    for emp in employees:
        row_skills = []
        for s in skills:
            prof = matrix_map.get(emp.id, {}).get(s.id, None)
            row_skills.append({
                'skill': s,
                'proficiency': prof
            })
        matrix_rows.append({
            'employee': emp,
            'skills': row_skills
        })

    return render(request, 'skills/matrix.html', {
        'matrix_rows': matrix_rows,
        'skills': skills,
        'departments': departments,
        'selected_dept': dept_id,
    })

@login_required
@manager_or_above_required
def skill_verification_action(request, emp_skill_id):
    emp_skill = get_object_or_404(EmployeeSkill, id=emp_skill_id)
    current_emp = getattr(request.user, 'employee_profile', None)
    emp_skill.is_verified = True
    emp_skill.verified_by = current_emp
    emp_skill.save()
    messages.success(request, f"Skill verified for {emp_skill.employee.full_name}.")
    return redirect('skills:matrix')
