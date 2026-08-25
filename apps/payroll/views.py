from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.http import HttpResponse
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, Payslip, TaxDeclaration
from apps.payroll.forms import SalaryStructureForm, PayrollRunForm, TaxDeclarationForm
from apps.payroll.services import PayrollCalculationService

@login_required
def payroll_dashboard(request):
    runs = PayrollRun.objects.all()[:6]
    structures = SalaryStructure.objects.filter(is_active=True)
    total_annual_payroll = structures.aggregate(total=Sum('annual_ctc'))['total'] or 0
    recent_payslips = Payslip.objects.select_related('employee', 'payroll_run')[:10]
    
    # User's personal latest payslip
    user_payslip = None
    if hasattr(request.user, 'employee_profile'):
        user_payslip = Payslip.objects.filter(employee=request.user.employee_profile).order_by('-payroll_run__payroll_year', '-payroll_run__payroll_month').first()

    context = {
        'runs': runs,
        'structures': structures,
        'total_annual_payroll': total_annual_payroll,
        'recent_payslips': recent_payslips,
        'user_payslip': user_payslip,
    }
    return render(request, 'payroll/dashboard.html', context)

@login_required
def salary_structure_list(request):
    structures = SalaryStructure.objects.all()
    return render(request, 'payroll/structure_list.html', {'structures': structures})

@login_required
def salary_structure_create(request):
    if request.method == 'POST':
        form = SalaryStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary structure configured successfully.")
            return redirect('payroll:structure_list')
    else:
        form = SalaryStructureForm()
    return render(request, 'payroll/structure_form.html', {'form': form, 'title': 'Create Salary Structure'})

@login_required
def payroll_run_list(request):
    runs = PayrollRun.objects.all()
    return render(request, 'payroll/run_list.html', {'runs': runs})

@login_required
def payroll_run_detail(request, pk):
    run = get_object_or_404(PayrollRun, pk=pk)
    payslips = run.payslips.select_related('employee__user', 'employee__department').all()
    return render(request, 'payroll/run_detail.html', {'run': run, 'payslips': payslips})

@login_required
def payroll_run_process(request, pk):
    run = get_object_or_404(PayrollRun, pk=pk)
    PayrollCalculationService.execute_payroll_run(run, request.user)
    messages.success(request, f"Payroll for {run.title} calculated and disbursed successfully!")
    return redirect('payroll:run_detail', pk=run.pk)

@login_required
def my_payslips(request):
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, "Employee profile not found.")
        return redirect('payroll:dashboard')
    payslips = Payslip.objects.filter(employee=request.user.employee_profile).select_related('payroll_run')
    return render(request, 'payroll/my_payslips.html', {'payslips': payslips})

@login_required
def payslip_detail(request, pk):
    payslip = get_object_or_404(Payslip.objects.select_related('employee', 'payroll_run', 'salary_structure'), pk=pk)
    return render(request, 'payroll/payslip_view.html', {'payslip': payslip})

@login_required
def tax_declaration_portal(request):
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, "Employee profile required.")
        return redirect('payroll:dashboard')
    dec, created = TaxDeclaration.objects.get_or_create(
        employee=request.user.employee_profile,
        financial_year="2026-2027"
    )
    if request.method == 'POST':
        form = TaxDeclarationForm(request.POST, instance=dec)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 'SUBMITTED'
            obj.save()
            messages.success(request, "Tax exemptions declaration submitted successfully for verification.")
            return redirect('payroll:tax_declaration')
    else:
        form = TaxDeclarationForm(instance=dec)
    return render(request, 'payroll/tax_declaration.html', {'form': form, 'declaration': dec})
