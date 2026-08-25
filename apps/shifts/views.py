from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.permissions.decorators import hr_or_admin_required
from apps.shifts.forms import CompanyHolidayForm, ShiftAssignmentForm, WorkShiftForm
from apps.shifts.models import CompanyHoliday, ShiftAssignment, WorkShift


@login_required
def shift_list_view(request):
    shifts = WorkShift.objects.all()
    assignments = ShiftAssignment.objects.filter(is_active=True).select_related('employee', 'shift')[:30]
    return render(request, 'shifts/shift_list.html', {
        'shifts': shifts,
        'assignments': assignments,
    })

@login_required
@hr_or_admin_required
def shift_create_view(request):
    form = WorkShiftForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        shift = form.save()
        messages.success(request, f"Shift '{shift.name}' created.")
        return redirect('shifts:shift_list')
    return render(request, 'shifts/shift_form.html', {'form': form, 'title': 'Create New Shift'})

@login_required
@hr_or_admin_required
def shift_assign_view(request):
    form = ShiftAssignmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        assignment = form.save()
        messages.success(request, f"Shift assigned to {assignment.employee.full_name}.")
        return redirect('shifts:shift_list')
    return render(request, 'shifts/shift_assign_form.html', {'form': form})

@login_required
def holiday_list_view(request):
    holidays = CompanyHoliday.objects.all().order_by('date')
    return render(request, 'shifts/holiday_list.html', {'holidays': holidays})

@login_required
@hr_or_admin_required
def holiday_create_view(request):
    form = CompanyHolidayForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        holiday = form.save()
        messages.success(request, f"Holiday '{holiday.name}' added.")
        return redirect('shifts:holiday_list')
    return render(request, 'shifts/holiday_form.html', {'form': form})
