from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.organization.forms import (
    DepartmentForm,
    DesignationForm,
    OrganizationProfileForm,
    TeamForm,
)
from apps.organization.models import Department, Designation, OrganizationProfile, Team
from apps.permissions.decorators import admin_required, hr_or_admin_required


@login_required
def department_list(request):
    search = request.GET.get('search', '').strip()
    departments = Department.objects.all().select_related('head_of_department').prefetch_related('teams', 'employees')
    if search:
        departments = departments.filter(Q(name__icontains=search) | Q(code__icontains=search) | Q(location__icontains=search))
    return render(request, 'organization/department_list.html', {
        'departments': departments,
        'search': search,
    })

@login_required
@hr_or_admin_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dept = form.save()
        messages.success(request, f"Department '{dept.name}' created successfully.")
        return redirect('organization:department_list')
    return render(request, 'organization/department_form.html', {'form': form, 'title': 'Add New Department'})

@login_required
@hr_or_admin_required
def department_update(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    form = DepartmentForm(request.POST or None, instance=dept)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Department '{dept.name}' updated successfully.")
        return redirect('organization:department_list')
    return render(request, 'organization/department_form.html', {'form': form, 'title': f'Edit Department - {dept.name}'})

@login_required
def team_list(request):
    search = request.GET.get('search', '').strip()
    dept_id = request.GET.get('department')
    teams = Team.objects.all().select_related('department', 'team_lead').prefetch_related('members')
    
    if search:
        teams = teams.filter(Q(name__icontains=search) | Q(code__icontains=search))
    if dept_id:
        teams = teams.filter(department_id=dept_id)
        
    departments = Department.objects.filter(is_active=True)
    return render(request, 'organization/team_list.html', {
        'teams': teams,
        'departments': departments,
        'selected_dept': dept_id,
        'search': search,
    })

@login_required
@hr_or_admin_required
def team_create(request):
    form = TeamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        team = form.save()
        messages.success(request, f"Team '{team.name}' created successfully.")
        return redirect('organization:team_list')
    return render(request, 'organization/team_form.html', {'form': form, 'title': 'Create New Team'})

@login_required
@hr_or_admin_required
def team_update(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    form = TeamForm(request.POST or None, instance=team)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Team '{team.name}' updated successfully.")
        return redirect('organization:team_list')
    return render(request, 'organization/team_form.html', {'form': form, 'title': f'Edit Team - {team.name}'})

@login_required
def designation_list(request):
    designations = Designation.objects.all().select_related('department')
    return render(request, 'organization/designation_list.html', {'designations': designations})

@login_required
@hr_or_admin_required
def designation_create(request):
    form = DesignationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        desig = form.save()
        messages.success(request, f"Designation '{desig.title}' added successfully.")
        return redirect('organization:designation_list')
    return render(request, 'organization/designation_form.html', {'form': form, 'title': 'Add New Designation'})

@login_required
@hr_or_admin_required
def designation_update(request, desig_id):
    desig = get_object_or_404(Designation, id=desig_id)
    form = DesignationForm(request.POST or None, instance=desig)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Designation '{desig.title}' updated successfully.")
        return redirect('organization:designation_list')
    return render(request, 'organization/designation_form.html', {'form': form, 'title': f'Edit Designation - {desig.title}'})

@login_required
def org_chart_view(request):
    """
    Renders the company structural hierarchy tree showing Departments, Teams, Leads, and Members.
    """
    departments = Department.objects.filter(is_active=True).prefetch_related('teams__members', 'employees')
    return render(request, 'organization/org_chart.html', {'departments': departments})

@login_required
@admin_required
def organization_profile_view(request):
    profile, _ = OrganizationProfile.objects.get_or_create(id=1)
    form = OrganizationProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Company profile information updated.")
        return redirect('organization:profile')
    return render(request, 'organization/org_profile.html', {'form': form, 'profile': profile})
