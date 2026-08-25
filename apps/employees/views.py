import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.authentication.models import User
from apps.employees.forms import (
    EmployeeCreateForm,
)
from apps.employees.models import (
    Employee,
    EmploymentStatus,
)
from apps.employees.services import Employee360Service
from apps.organization.models import Department
from apps.permissions.decorators import hr_or_admin_required
from apps.permissions.models import SystemRole


@login_required
def employee_list(request):
    search = request.GET.get('search', '').strip()
    dept_id = request.GET.get('department')
    status = request.GET.get('status')
    emp_type = request.GET.get('type')

    employees = Employee.objects.all().select_related('department', 'designation', 'team', 'reporting_manager')

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(employee_id__icontains=search) |
            Q(email__icontains=search)
        )
    if dept_id:
        employees = employees.filter(department_id=dept_id)
    if status:
        employees = employees.filter(employment_status=status)
    if emp_type:
        employees = employees.filter(employment_type=emp_type)

    departments = Department.objects.filter(is_active=True)
    
    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'departments': departments,
        'selected_dept': dept_id,
        'selected_status': status,
        'selected_type': emp_type,
        'search': search,
    })

@login_required
def employee_360_view(request, employee_id):
    """
    Dedicated Employee 360° View Hub presenting the complete employee profile.
    """
    profile_data = Employee360Service.get_full_360_profile(employee_id)
    if not profile_data:
        messages.error(request, "Employee not found.")
        return redirect('employees:employee_list')

    # Security check: Non-HR/Admin users can view self, direct reports, or department staff if manager
    current_emp = getattr(request.user, 'employee_profile', None)
    is_privileged = request.user.is_superuser or request.user.role in [SystemRole.ADMIN, SystemRole.HR]
    is_self = current_emp and current_emp.id == profile_data['employee'].id
    is_direct_manager = current_emp and profile_data['employee'].reporting_manager_id == current_emp.id
    is_dept_manager = current_emp and request.user.role == SystemRole.MANAGER and current_emp.department_id == profile_data['employee'].department_id

    if not (is_privileged or is_self or is_direct_manager or is_dept_manager):
        messages.error(request, "You are not authorized to view this employee's complete 360° record.")
        return redirect('authentication:dashboard')

    return render(request, 'employees/employee_360.html', profile_data)

@login_required
def employee_self_profile(request):
    current_emp = getattr(request.user, 'employee_profile', None)
    if not current_emp:
        messages.error(request, "No employee record linked to your user account.")
        return redirect('authentication:dashboard')
    return redirect('employees:employee_360', employee_id=current_emp.id)

@login_required
@hr_or_admin_required
def employee_create(request):
    form = EmployeeCreateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        emp = form.save(commit=False)
        # Create a linked user account for this new employee
        username = emp.email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=emp.email,
            password="TemporaryPassword123!",
            first_name=emp.first_name,
            last_name=emp.last_name,
            role=SystemRole.EMPLOYEE
        )
        emp.user = user
        emp.save()
        messages.success(request, f"Employee {emp.full_name} created successfully with username '{username}'.")
        return redirect('employees:employee_360', employee_id=emp.id)

    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Register New Employee'})

@login_required
@hr_or_admin_required
def employee_update(request, employee_id):
    emp = get_object_or_404(Employee, id=employee_id)
    form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=emp)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Employee profile for {emp.full_name} updated successfully.")
        return redirect('employees:employee_360', employee_id=emp.id)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': f'Edit Employee - {emp.full_name}'})

@login_required
def employee_directory(request):
    search = request.GET.get('search', '').strip()
    dept_id = request.GET.get('department')
    employees = Employee.objects.filter(employment_status=EmploymentStatus.ACTIVE).select_related('department', 'designation', 'team')
    
    if search:
        employees = employees.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(designation__title__icontains=search))
    if dept_id:
        employees = employees.filter(department_id=dept_id)

    departments = Department.objects.filter(is_active=True)
    return render(request, 'employees/employee_directory.html', {
        'employees': employees,
        'departments': departments,
        'search': search,
        'selected_dept': dept_id
    })

@login_required
@hr_or_admin_required
def employee_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees_roster.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Full Name', 'Email', 'Phone', 'Department', 'Designation', 'Joining Date', 'Status', 'Type'])

    employees = Employee.objects.all().select_related('department', 'designation')
    for emp in employees:
        writer.writerow([
            emp.employee_id,
            emp.full_name,
            emp.email,
            emp.phone,
            emp.department.name if emp.department else 'N/A',
            emp.designation.title if emp.designation else 'N/A',
            emp.date_of_joining,
            emp.employment_status,
            emp.employment_type
        ])
    return response
