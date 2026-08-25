import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# PAYROLL TEMPLATES
# ==============================================================================

write_file("templates/payroll/dashboard.html", """{% extends 'base.html' %}
{% block title %}Payroll & Compensation — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-cash-stack text-success"></i> Enterprise Payroll & Compensation</h1>
        <p class="ems-page-subheading">Salary structures, tax deductions, PF/ESI statutory compliance & monthly disbursements</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{% url 'payroll:my_payslips' %}" class="btn btn-outline-primary"><i class="bi bi-file-earmark-text me-1"></i>My Payslips</a>
        <a href="{% url 'payroll:tax_declaration' %}" class="btn btn-outline-secondary"><i class="bi bi-calculator me-1"></i>Tax Declarations</a>
        <a href="{% url 'payroll:run_list' %}" class="btn btn-primary"><i class="bi bi-play-circle me-1"></i>Payroll Runs</a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="text-muted small">Total Annual CTC</div>
                    <h3 class="fw-bold mb-0 text-dark">₹{{ total_annual_payroll|floatformat:0 }}</h3>
                </div>
                <div class="p-3 bg-success-subtle text-success rounded-3"><i class="bi bi-bank fs-3"></i></div>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="text-muted small">Salary Structures</div>
                    <h3 class="fw-bold mb-0 text-dark">{{ structures.count }} Active</h3>
                </div>
                <div class="p-3 bg-primary-subtle text-primary rounded-3"><i class="bi bi-diagram-3-fill fs-3"></i></div>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="text-muted small">Completed Runs</div>
                    <h3 class="fw-bold mb-0 text-dark">{{ runs.count }} Cycles</h3>
                </div>
                <div class="p-3 bg-warning-subtle text-warning rounded-3"><i class="bi bi-clock-history fs-3"></i></div>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="text-muted small">Compliance Status</div>
                    <h3 class="fw-bold mb-0 text-success">100% PF/ESI</h3>
                </div>
                <div class="p-3 bg-info-subtle text-info rounded-3"><i class="bi bi-shield-check fs-3"></i></div>
            </div>
        </div>
    </div>
</div>

<div class="row g-3">
    <div class="col-12 col-lg-8">
        <div class="ems-card">
            <div class="ems-card-header d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0">Recent Payroll Disbursement Runs</h5>
                <a href="{% url 'payroll:run_list' %}" class="btn btn-sm btn-outline-primary">View All</a>
            </div>
            <div class="ems-card-body p-0">
                <div class="table-responsive">
                    <table class="ems-table">
                        <thead><tr><th>Cycle Title</th><th>Period</th><th>Employees</th><th>Disbursed Total</th><th>Status</th><th>Action</th></tr></thead>
                        <tbody>{% for r in runs %}
                            <tr>
                                <td><strong>{{ r.title }}</strong></td>
                                <td>{{ r.start_date }} to {{ r.end_date }}</td>
                                <td><span class="badge bg-light text-dark border">{{ r.total_employees }} Staff</span></td>
                                <td class="fw-bold text-success">₹{{ r.total_net_pay|floatformat:2 }}</td>
                                <td><span class="badge bg-success">{{ r.get_status_display }}</span></td>
                                <td><a href="{% url 'payroll:run_detail' r.id %}" class="btn btn-sm btn-outline-secondary">Details</a></td>
                            </tr>
                        {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No payroll runs found.</td></tr>{% endfor %}</tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <div class="col-12 col-lg-4">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Salary Structures & Grades</h5></div>
            <div class="ems-card-body p-3">
                <div class="list-group list-group-flush">
                    {% for s in structures %}
                        <div class="list-group-item px-0 d-flex justify-content-between align-items-center">
                            <div>
                                <div class="fw-semibold">{{ s.name }}</div>
                                <div class="text-muted small">Code: {{ s.code }}</div>
                            </div>
                            <span class="badge bg-primary-subtle text-primary border">₹{{ s.annual_ctc|floatformat:0 }}/yr</span>
                        </div>
                    {% empty %}<p class="text-muted small">No structures.</p>{% endfor %}
                </div>
                <div class="mt-3 text-center">
                    <a href="{% url 'payroll:structure_list' %}" class="btn btn-sm btn-outline-primary w-100">Manage Salary Bands</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/payroll/structure_list.html", """{% extends 'base.html' %}
{% block title %}Salary Structures — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-diagram-3-fill text-primary"></i> Salary Structures & Compensation Bands</h1>
        <p class="ems-page-subheading">Define grade-wise CTC allocations, Basic, HRA, DA, PF & ESI formulas</p>
    </div>
    <div><a href="{% url 'payroll:structure_create' %}" class="btn btn-primary"><i class="bi bi-plus-lg me-1"></i>Add Structure</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Structure Name</th><th>Code</th><th>Annual CTC</th><th>Monthly Basic</th><th>Monthly HRA</th><th>PF Deduct %</th><th>Net Est / Mo</th><th>Status</th></tr></thead>
    <tbody>{% for s in structures %}
        <tr>
            <td><strong>{{ s.name }}</strong></td>
            <td><span class="badge bg-light text-dark border">{{ s.code }}</span></td>
            <td class="fw-bold">₹{{ s.annual_ctc|floatformat:2 }}</td>
            <td>₹{{ s.monthly_basic|floatformat:2 }}</td>
            <td>₹{{ s.monthly_hra|floatformat:2 }}</td>
            <td>{{ s.pf_employee_rate }}%</td>
            <td class="text-success fw-bold">₹{{ s.monthly_net_pay|floatformat:2 }}</td>
            <td><span class="badge bg-success">Active</span></td>
        </tr>
    {% empty %}<tr><td colspan="8" class="text-center py-4 text-muted">No structures configured.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/payroll/structure_form.html", """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1><p class="ems-page-subheading">Configure grade-level compensation breakdown</p></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-md-6"><label class="form-label small fw-semibold">Structure Name *</label>{{ form.name }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Code *</label>{{ form.code }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Annual CTC (₹) *</label>{{ form.annual_ctc }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Currency</label>{{ form.currency }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Basic % of CTC</label>{{ form.basic_percentage }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">HRA % of Basic</label>{{ form.hra_percentage }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">DA % of Basic</label>{{ form.da_percentage }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Special Allowance / Mo</label>{{ form.special_allowance }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Conveyance / Mo</label>{{ form.conveyance_allowance }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Medical / Mo</label>{{ form.medical_allowance }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">PF Employee Rate %</label>{{ form.pf_employee_rate }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">PF Employer Rate %</label>{{ form.pf_employer_rate }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Professional Tax / Mo</label>{{ form.professional_tax }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
        <a href="{% url 'payroll:structure_list' %}" class="btn btn-outline-secondary">Cancel</a>
        <button type="submit" class="btn btn-primary px-4">Save Structure</button>
    </div>
</form></div></div>
{% endblock %}
""")

write_file("templates/payroll/run_list.html", """{% extends 'base.html' %}
{% block title %}Payroll Runs — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-cash-coin text-success"></i> Monthly Payroll Runs & Cycles</h1>
        <p class="ems-page-subheading">Generate, calculate, review, and disburse monthly workforce wages</p>
    </div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Run Title</th><th>Month / Year</th><th>Start Date</th><th>End Date</th><th>Employees</th><th>Gross Total</th><th>Net Disbursed</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>{% for r in runs %}
        <tr>
            <td><strong>{{ r.title }}</strong></td>
            <td>{{ r.payroll_month }}/{{ r.payroll_year }}</td>
            <td>{{ r.start_date }}</td>
            <td>{{ r.end_date }}</td>
            <td><span class="badge bg-light text-dark border">{{ r.total_employees }}</span></td>
            <td>₹{{ r.total_gross_pay|floatformat:2 }}</td>
            <td class="fw-bold text-success">₹{{ r.total_net_pay|floatformat:2 }}</td>
            <td><span class="badge bg-success">{{ r.get_status_display }}</span></td>
            <td><a href="{% url 'payroll:run_detail' r.id %}" class="btn btn-sm btn-outline-primary">View / Process</a></td>
        </tr>
    {% empty %}<tr><td colspan="9" class="text-center py-4 text-muted">No payroll runs found.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/payroll/run_detail.html", """{% extends 'base.html' %}
{% block title %}{{ run.title }} — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-wallet2 text-success"></i> {{ run.title }}</h1>
        <p class="ems-page-subheading">Period: {{ run.start_date }} to {{ run.end_date }} | Disbursed on: {{ run.payment_date }}</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{% url 'payroll:run_process' run.id %}" class="btn btn-success" onclick="return confirm('Recalculate and approve all employee payslips for this cycle?')"><i class="bi bi-gear-wide-connected me-1"></i>Recalculate & Disburse</a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Total Employees</div><h3 class="fw-bold text-dark mb-0">{{ run.total_employees }}</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Gross Pay</div><h3 class="fw-bold text-dark mb-0">₹{{ run.total_gross_pay|floatformat:2 }}</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Total Deductions</div><h3 class="fw-bold text-danger mb-0">₹{{ run.total_deductions|floatformat:2 }}</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Net Disbursed</div><h3 class="fw-bold text-success mb-0">₹{{ run.total_net_pay|floatformat:2 }}</h3></div></div>
</div>

<div class="ems-card"><div class="ems-card-header"><h5 class="fw-bold mb-0">Individual Employee Payslips ({{ payslips.count }})</h5></div>
<div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Department</th><th>Working Days</th><th>Gross Earnings</th><th>PF + Tax Deductions</th><th>Net Salary</th><th>Action</th></tr></thead>
    <tbody>{% for p in payslips %}
        <tr>
            <td><strong>{{ p.employee.full_name }}</strong><div class="text-muted small">{{ p.employee.employee_id }}</div></td>
            <td>{{ p.employee.department.name|default:"General" }}</td>
            <td>{{ p.days_present }}/{{ p.total_working_days }}</td>
            <td>₹{{ p.gross_earnings|floatformat:2 }}</td>
            <td class="text-danger">₹{{ p.total_deductions|floatformat:2 }}</td>
            <td class="fw-bold text-success">₹{{ p.net_salary|floatformat:2 }}</td>
            <td><a href="{% url 'payroll:payslip_detail' p.id %}" class="btn btn-sm btn-outline-secondary"><i class="bi bi-eye"></i> View Slip</a></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center py-4 text-muted">No payslips calculated yet.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/payroll/my_payslips.html", """{% extends 'base.html' %}
{% block title %}My Payslips — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-receipt-cutoff text-primary"></i> My Monthly Payslips</h1>
        <p class="ems-page-subheading">View, download, and verify your official monthly salary receipts</p>
    </div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Month / Year</th><th>Pay Cycle</th><th>Gross Pay</th><th>Total Deductions</th><th>Net Pay Deposited</th><th>Action</th></tr></thead>
    <tbody>{% for p in payslips %}
        <tr>
            <td><strong>{{ p.payroll_run.payroll_month }}/{{ p.payroll_run.payroll_year }}</strong></td>
            <td>{{ p.payroll_run.title }}</td>
            <td>₹{{ p.gross_earnings|floatformat:2 }}</td>
            <td class="text-danger">₹{{ p.total_deductions|floatformat:2 }}</td>
            <td class="fw-bold text-success">₹{{ p.net_salary|floatformat:2 }}</td>
            <td><a href="{% url 'payroll:payslip_detail' p.id %}" class="btn btn-sm btn-primary"><i class="bi bi-printer me-1"></i>View Slip</a></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No payslips generated for your profile yet.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/payroll/payslip_view.html", """{% extends 'base.html' %}
{% block title %}Payslip {{ payslip.employee.full_name }} — Smart EMS{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <a href="{% url 'payroll:my_payslips' %}" class="btn btn-outline-secondary"><i class="bi bi-arrow-left me-1"></i>Back to Payslips</a>
    <button onclick="window.print()" class="btn btn-primary"><i class="bi bi-printer me-1"></i>Print Payslip</button>
</div>

<div class="card border shadow-sm p-4 bg-white rounded-4" style="max-width: 850px; margin: 0 auto;">
    <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-3">
        <div>
            <h3 class="fw-bold text-primary mb-0">BHARAT ENTERPRISE SOLUTIONS</h3>
            <p class="text-muted small mb-0">Workforce & Human Resources Platform | Confidential Payslip</p>
        </div>
        <div class="text-end">
            <span class="badge bg-success-subtle text-success border fs-6">CONFIRMED & PAID</span>
            <div class="text-muted small mt-1">Period: {{ payslip.payroll_run.title }}</div>
        </div>
    </div>

    <div class="row g-3 mb-4 small">
        <div class="col-6">
            <div><strong>Employee Name:</strong> {{ payslip.employee.full_name }}</div>
            <div><strong>Employee ID:</strong> {{ payslip.employee.employee_id }}</div>
            <div><strong>Designation:</strong> {{ payslip.employee.designation.title|default:"Staff" }}</div>
            <div><strong>Department:</strong> {{ payslip.employee.department.name|default:"Corporate" }}</div>
        </div>
        <div class="col-6">
            <div><strong>Bank Name:</strong> State Bank of India</div>
            <div><strong>Account No:</strong> ************1012</div>
            <div><strong>Payment Mode:</strong> {{ payslip.payment_mode }}</div>
            <div><strong>Working Days:</strong> {{ payslip.days_present }} / {{ payslip.total_working_days }}</div>
        </div>
    </div>

    <div class="row g-3 mb-4">
        <div class="col-6">
            <div class="border rounded-3 p-3 bg-light">
                <h6 class="fw-bold text-success border-bottom pb-2 mb-2">EARNINGS</h6>
                <div class="d-flex justify-content-between py-1"><span>Basic Pay</span><span>₹{{ payslip.basic_pay|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>House Rent Allowance (HRA)</span><span>₹{{ payslip.hra|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>Dearness Allowance (DA)</span><span>₹{{ payslip.da|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>Special Allowance</span><span>₹{{ payslip.special_allowance|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>Conveyance Allowance</span><span>₹{{ payslip.conveyance_allowance|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>Medical Allowance</span><span>₹{{ payslip.medical_allowance|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1 border-top fw-bold"><span>Gross Earnings</span><span class="text-success">₹{{ payslip.gross_earnings|floatformat:2 }}</span></div>
            </div>
        </div>
        <div class="col-6">
            <div class="border rounded-3 p-3 bg-light">
                <h6 class="fw-bold text-danger border-bottom pb-2 mb-2">DEDUCTIONS</h6>
                <div class="d-flex justify-content-between py-1"><span>Provident Fund (PF)</span><span>₹{{ payslip.pf_employee|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>Professional Tax (PT)</span><span>₹{{ payslip.professional_tax|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>Income Tax (TDS)</span><span>₹{{ payslip.income_tax_tds|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1"><span>Loss of Pay (LOP)</span><span>₹{{ payslip.lop_deduction|floatformat:2 }}</span></div>
                <div class="d-flex justify-content-between py-1 border-top fw-bold"><span>Total Deductions</span><span class="text-danger">₹{{ payslip.total_deductions|floatformat:2 }}</span></div>
            </div>
        </div>
    </div>

    <div class="p-3 bg-success-subtle border border-success rounded-3 text-center mb-3">
        <div class="text-muted small">NET SALARY PAYABLE (CREDITED TO ACCOUNT)</div>
        <h2 class="fw-bold text-success mb-0">₹{{ payslip.net_salary|floatformat:2 }}</h2>
    </div>

    <div class="text-center text-muted small mt-4">
        This is a computer-generated official payslip issued under Bharat Enterprise Solutions Smart EMS.
    </div>
</div>
{% endblock %}
""")

write_file("templates/payroll/tax_declaration.html", """{% extends 'base.html' %}
{% block title %}Tax Exemptions Declaration — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-calculator text-primary"></i> Income Tax Exemptions & Declarations</h1>
        <p class="ems-page-subheading">Financial Year {{ declaration.financial_year }} | Tax Regime: {{ declaration.get_regime_display }}</p>
    </div>
</div>

<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-md-6"><label class="form-label small fw-semibold">Financial Year</label>{{ form.financial_year }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Tax Regime</label>{{ form.regime }}</div>
        
        <h6 class="fw-bold text-primary mt-4 border-bottom pb-2">Section 80C Deductions (Max Limit ₹1,50,000)</h6>
        <div class="col-md-3"><label class="form-label small fw-semibold">Life Insurance (LIC)</label>{{ form.section_80c_lic }}</div>
        <div class="col-md-3"><label class="form-label small fw-semibold">Public PF (PPF)</label>{{ form.section_80c_ppf }}</div>
        <div class="col-md-3"><label class="form-label small fw-semibold">ELSS Mutual Funds</label>{{ form.section_80c_elss }}</div>
        <div class="col-md-3"><label class="form-label small fw-semibold">Children Tuition Fees</label>{{ form.section_80c_tuition }}</div>

        <h6 class="fw-bold text-primary mt-4 border-bottom pb-2">Section 80D & Home Loan (Section 24)</h6>
        <div class="col-md-4"><label class="form-label small fw-semibold">Mediclaim (Self & Family)</label>{{ form.section_80d_self }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Mediclaim (Senior Parents)</label>{{ form.section_80d_parents }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Home Loan Interest</label>{{ form.home_loan_interest }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">House Rent Paid (Annual)</label>{{ form.house_rent_paid_annual }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">NPS 80CCD(1B) Contribution</label>{{ form.nps_additional }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
        <button type="submit" class="btn btn-primary px-4">Submit Tax Declaration</button>
    </div>
</form></div></div>
{% endblock %}
""")

print("Finished Payroll templates generation.")
