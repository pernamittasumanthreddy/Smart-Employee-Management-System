import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# RECRUITMENT TEMPLATES
# ==============================================================================

write_file("templates/recruitment/dashboard.html", """{% extends 'base.html' %}
{% block title %}Recruitment & ATS — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-person-plus-fill text-primary"></i> Recruitment & Talent Acquisition (ATS)</h1>
        <p class="ems-page-subheading">Job requisitions, candidate pipeline kanban, interview scheduling & offer management</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{% url 'recruitment:pipeline' %}" class="btn btn-primary"><i class="bi bi-kanban me-1"></i>Hiring Pipeline</a>
        <a href="{% url 'recruitment:requisition_create' %}" class="btn btn-outline-primary"><i class="bi bi-plus-lg me-1"></i>Create Requisition</a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div><div class="text-muted small">Open Requisitions</div><h3 class="fw-bold mb-0 text-primary">{{ overview.total_open_positions }}</h3></div>
                <div class="p-3 bg-primary-subtle text-primary rounded-3"><i class="bi bi-briefcase-fill fs-3"></i></div>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div><div class="text-muted small">Candidate Pool</div><h3 class="fw-bold mb-0 text-success">{{ overview.total_candidates }}</h3></div>
                <div class="p-3 bg-success-subtle text-success rounded-3"><i class="bi bi-people-fill fs-3"></i></div>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div><div class="text-muted small">Active in Pipeline</div><h3 class="fw-bold mb-0 text-warning">{{ overview.active_applications }}</h3></div>
                <div class="p-3 bg-warning-subtle text-warning rounded-3"><i class="bi bi-funnel-fill fs-3"></i></div>
            </div>
        </div>
    </div>
    <div class="col-12 col-md-3">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div><div class="text-muted small">Offers Extended</div><h3 class="fw-bold mb-0 text-info">{{ overview.offers_extended }}</h3></div>
                <div class="p-3 bg-info-subtle text-info rounded-3"><i class="bi bi-envelope-paper-heart-fill fs-3"></i></div>
            </div>
        </div>
    </div>
</div>

<div class="row g-3">
    <div class="col-12 col-lg-8">
        <div class="ems-card">
            <div class="ems-card-header d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0">Open Job Requisitions</h5>
                <a href="{% url 'recruitment:requisition_list' %}" class="btn btn-sm btn-outline-primary">View All</a>
            </div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Position Title</th><th>Code</th><th>Department</th><th>Headcount</th><th>Priority</th><th>Action</th></tr></thead>
                <tbody>{% for r in open_requisitions %}
                    <tr>
                        <td><strong>{{ r.title }}</strong></td>
                        <td><span class="badge bg-light text-dark border">{{ r.requisition_code }}</span></td>
                        <td>{{ r.department.name }}</td>
                        <td><span class="badge bg-primary">{{ r.headcount }} Open</span></td>
                        <td><span class="badge bg-danger">{{ r.get_priority_display }}</span></td>
                        <td><a href="{% url 'recruitment:pipeline' %}" class="btn btn-sm btn-outline-secondary">Pipeline</a></td>
                    </tr>
                {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No open requisitions.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
    <div class="col-12 col-lg-4">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Upcoming Interviews</h5></div>
            <div class="ems-card-body p-3">
                <div class="list-group list-group-flush">
                    {% for iv in upcoming_interviews %}
                        <div class="list-group-item px-0">
                            <div class="fw-semibold">{{ iv.application.candidate.full_name }}</div>
                            <div class="text-muted small">{{ iv.round_name }}</div>
                            <div class="badge bg-primary-subtle text-primary mt-1">{{ iv.scheduled_start|date:"M d, H:i" }}</div>
                        </div>
                    {% empty %}<p class="text-muted small">No interviews scheduled today.</p>{% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/recruitment/requisition_list.html", """{% extends 'base.html' %}
{% block title %}Job Requisitions — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-briefcase-fill text-primary"></i> Job Requisitions & Vacancies</h1>
        <p class="ems-page-subheading">Enterprise workforce hiring approvals and job requisitions</p>
    </div>
    <div><a href="{% url 'recruitment:requisition_create' %}" class="btn btn-primary"><i class="bi bi-plus-lg me-1"></i>New Requisition</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Job Title</th><th>Code</th><th>Department</th><th>Headcount</th><th>Experience</th><th>Budget Range</th><th>Status</th></tr></thead>
    <tbody>{% for r in requisitions %}
        <tr>
            <td><strong>{{ r.title }}</strong></td>
            <td><span class="badge bg-light text-dark border">{{ r.requisition_code }}</span></td>
            <td>{{ r.department.name }}</td>
            <td>{{ r.headcount }}</td>
            <td>{{ r.min_experience_years }} - {{ r.max_experience_years }} yrs</td>
            <td>₹{{ r.budget_min|floatformat:0 }} - ₹{{ r.budget_max|floatformat:0 }}</td>
            <td><span class="badge bg-success">{{ r.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center py-4 text-muted">No requisitions created.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/recruitment/requisition_form.html", """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-md-6"><label class="form-label small fw-semibold">Job Title *</label>{{ form.title }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Requisition Code *</label>{{ form.requisition_code }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Department *</label>{{ form.department }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Designation</label>{{ form.designation }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Headcount *</label>{{ form.headcount }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Min Experience (Yrs)</label>{{ form.min_experience_years }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Max Experience (Yrs)</label>{{ form.max_experience_years }}</div>
        <div class="col-md-4"><label class="form-label small fw-semibold">Priority</label>{{ form.priority }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Budget Min (₹)</label>{{ form.budget_min }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Budget Max (₹)</label>{{ form.budget_max }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Employment Type</label>{{ form.employment_type }}</div>
        <div class="col-md-6"><label class="form-label small fw-semibold">Target Hire Date</label>{{ form.target_hire_date }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Required Skills</label>{{ form.required_skills }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Job Description</label>{{ form.job_description }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Business Justification</label>{{ form.justification }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
        <a href="{% url 'recruitment:requisition_list' %}" class="btn btn-outline-secondary">Cancel</a>
        <button type="submit" class="btn btn-primary px-4">Create Requisition</button>
    </div>
</form></div></div>
{% endblock %}
""")

write_file("templates/recruitment/pipeline_kanban.html", """{% extends 'base.html' %}
{% block title %}Hiring Pipeline Kanban — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-kanban text-primary"></i> Candidate Pipeline Kanban Board</h1>
        <p class="ems-page-subheading">Track candidates across recruitment stages from application to offer acceptance</p>
    </div>
</div>

<div class="row g-3 overflow-auto flex-nowrap pb-3">
    {% for stage_name, apps in pipeline_by_stage.items %}
        <div class="col-12 col-md-4 col-lg-3" style="min-width: 280px;">
            <div class="card bg-light border-0 shadow-sm rounded-3 h-100">
                <div class="card-header bg-white border-0 fw-bold d-flex justify-content-between align-items-center py-3">
                    <span class="small text-uppercase">{{ stage_name }}</span>
                    <span class="badge bg-primary rounded-pill">{{ apps|length }}</span>
                </div>
                <div class="card-body p-2 d-flex flex-column gap-2">
                    {% for app in apps %}
                        <div class="card border shadow-sm p-3 bg-white rounded-3">
                            <div class="fw-bold text-dark">{{ app.candidate.full_name }}</div>
                            <div class="text-muted small">{{ app.job_requisition.title }}</div>
                            <div class="d-flex justify-content-between align-items-center mt-2 small">
                                <span class="badge bg-success-subtle text-success border">Match: {{ app.match_score_percentage }}%</span>
                                <a href="{% url 'recruitment:candidate_detail' app.candidate.id %}" class="btn btn-sm btn-outline-secondary py-0">Profile</a>
                            </div>
                        </div>
                    {% empty %}
                        <div class="text-center text-muted small py-4">No candidates</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    {% endfor %}
</div>
{% endblock %}
""")

write_file("templates/recruitment/candidate_list.html", """{% extends 'base.html' %}
{% block title %}Candidates Pool — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-people-fill text-primary"></i> Candidate Talent Pool</h1>
        <p class="ems-page-subheading">Search and evaluate active applicants and candidate profiles</p>
    </div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Candidate Name</th><th>Email</th><th>Phone</th><th>Current Company</th><th>Experience</th><th>Current Location</th><th>Action</th></tr></thead>
    <tbody>{% for c in candidates %}
        <tr>
            <td><strong>{{ c.full_name }}</strong></td>
            <td>{{ c.email }}</td>
            <td>{{ c.phone }}</td>
            <td>{{ c.current_company|default:"Not Disclosed" }}</td>
            <td>{{ c.total_experience_years }} yrs</td>
            <td>{{ c.current_location }}</td>
            <td><a href="{% url 'recruitment:candidate_detail' c.id %}" class="btn btn-sm btn-outline-primary">View 360</a></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center py-4 text-muted">No candidates found.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/recruitment/candidate_detail.html", """{% extends 'base.html' %}
{% block title %}{{ candidate.full_name }} — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-person-badge-fill text-primary"></i> {{ candidate.full_name }}</h1>
        <p class="ems-page-subheading">{{ candidate.current_designation|default:"Professional Candidate" }} at {{ candidate.current_company|default:"Industry" }}</p>
    </div>
    <a href="{% url 'recruitment:candidate_list' %}" class="btn btn-outline-secondary"><i class="bi bi-arrow-left me-1"></i>Back</a>
</div>

<div class="row g-3">
    <div class="col-md-4">
        <div class="ems-card p-4">
            <h5 class="fw-bold mb-3">Contact Information</h5>
            <div><strong>Email:</strong> {{ candidate.email }}</div>
            <div><strong>Phone:</strong> {{ candidate.phone }}</div>
            <div><strong>Location:</strong> {{ candidate.current_location }}</div>
            <div><strong>Notice Period:</strong> {{ candidate.notice_period_days }} Days</div>
            <div class="mt-3"><strong>Current CTC:</strong> ₹{{ candidate.current_ctc|floatformat:0 }}</div>
            <div><strong>Expected CTC:</strong> ₹{{ candidate.expected_ctc|floatformat:0 }}</div>
        </div>
    </div>
    <div class="col-md-8">
        <div class="ems-card p-4">
            <h5 class="fw-bold mb-3">Application History</h5>
            {% for app in applications %}
                <div class="border rounded-3 p-3 mb-2 bg-light">
                    <div class="d-flex justify-content-between align-items-center">
                        <strong class="text-primary">{{ app.job_requisition.title }}</strong>
                        <span class="badge bg-primary">{{ app.get_stage_display }}</span>
                    </div>
                    <div class="text-muted small mt-1">Applied: {{ app.applied_at|date:"M d, Y" }} | Source: {{ app.get_source_display }}</div>
                    <div class="mt-2 small"><strong>AI Match Score:</strong> {{ app.match_score_percentage }}%</div>
                </div>
            {% empty %}<p class="text-muted">No applications recorded.</p>{% endfor %}
        </div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/recruitment/offer_list.html", """{% extends 'base.html' %}
{% block title %}Offer Letters — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-envelope-paper-heart-fill text-success"></i> Extended Offer Letters</h1>
        <p class="ems-page-subheading">Track formal candidate offers, CTC agreements, and digital signatures</p>
    </div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Offer Code</th><th>Candidate</th><th>Department</th><th>Offered Annual CTC</th><th>Target Joining</th><th>Status</th></tr></thead>
    <tbody>{% for o in offers %}
        <tr>
            <td><span class="badge bg-light text-dark border">{{ o.offer_code }}</span></td>
            <td><strong>{{ o.application.candidate.full_name }}</strong></td>
            <td>{{ o.department.name }}</td>
            <td class="fw-bold text-success">₹{{ o.offered_ctc_annual|floatformat:2 }}</td>
            <td>{{ o.joining_date }}</td>
            <td><span class="badge bg-success">{{ o.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No offers recorded.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

# ==============================================================================
# LIFECYCLE & ONBOARDING TEMPLATES
# ==============================================================================

write_file("templates/lifecycle/dashboard.html", """{% extends 'base.html' %}
{% block title %}Employee Lifecycle — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-arrows-fullscreen text-info"></i> Employee Lifecycle & Exit Clearances</h1>
        <p class="ems-page-subheading">New hire onboarding journeys, probation regularizations, resignations & department clearance checklists</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{% url 'lifecycle:onboarding_list' %}" class="btn btn-outline-primary"><i class="bi bi-person-check me-1"></i>Onboarding Hub</a>
        <a href="{% url 'lifecycle:resignation_list' %}" class="btn btn-outline-danger"><i class="bi bi-box-arrow-right me-1"></i>Resignations & Clearances</a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-md-4"><div class="ems-card p-3"><div class="text-muted small">Active Onboardings</div><h3 class="fw-bold text-primary mb-0">{{ onboardings.count }} In Progress</h3></div></div>
    <div class="col-md-4"><div class="ems-card p-3"><div class="text-muted small">Pending Probations</div><h3 class="fw-bold text-warning mb-0">{{ pending_probations.count }} Due</h3></div></div>
    <div class="col-md-4"><div class="ems-card p-3"><div class="text-muted small">Exit Clearances</div><h3 class="fw-bold text-danger mb-0">{{ resignations.count }} Active</h3></div></div>
</div>

<div class="row g-3">
    <div class="col-12 col-lg-6">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Recent Onboarding Workflows</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>New Hire</th><th>Joining Date</th><th>Progress</th><th>Action</th></tr></thead>
                <tbody>{% for ob in onboardings %}
                    <tr>
                        <td><strong>{{ ob.employee.full_name }}</strong></td>
                        <td>{{ ob.joining_date }}</td>
                        <td><div class="progress" style="height: 12px;"><div class="progress-bar bg-success" style="width: {{ ob.progress_percentage }}%;">{{ ob.progress_percentage }}%</div></div></td>
                        <td><a href="{% url 'lifecycle:onboarding_detail' ob.id %}" class="btn btn-sm btn-outline-primary">Checklist</a></td>
                    </tr>
                {% empty %}<tr><td colspan="4" class="text-center py-4 text-muted">No onboardings active.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
    <div class="col-12 col-lg-6">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Resignation & Clearance Pipeline</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Employee</th><th>Notice Date</th><th>Status</th><th>Action</th></tr></thead>
                <tbody>{% for r in resignations %}
                    <tr>
                        <td><strong>{{ r.employee.full_name }}</strong></td>
                        <td>{{ r.resignation_date }}</td>
                        <td><span class="badge bg-warning text-dark">{{ r.get_status_display }}</span></td>
                        <td><a href="{% url 'lifecycle:resignation_detail' r.id %}" class="btn btn-sm btn-outline-danger">Clearances</a></td>
                    </tr>
                {% empty %}<tr><td colspan="4" class="text-center py-4 text-muted">No resignations active.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/lifecycle/onboarding_list.html", """{% extends 'base.html' %}
{% block title %}Onboardings — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-person-check-fill text-primary"></i> New Hire Onboardings</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Mentor</th><th>Joining Date</th><th>IT Assets</th><th>HR Orientation</th><th>Action</th></tr></thead>
    <tbody>{% for ob in onboardings %}
        <tr>
            <td><strong>{{ ob.employee.full_name }}</strong></td>
            <td>{{ ob.mentor_buddy.full_name|default:"Assigned" }}</td>
            <td>{{ ob.joining_date }}</td>
            <td><span class="badge {% if ob.it_assets_assigned %}bg-success{% else %}bg-secondary{% endif %}">{% if ob.it_assets_assigned %}Issued{% else %}Pending{% endif %}</span></td>
            <td><span class="badge {% if ob.hr_orientation_completed %}bg-success{% else %}bg-secondary{% endif %}">{% if ob.hr_orientation_completed %}Completed{% else %}Pending{% endif %}</span></td>
            <td><a href="{% url 'lifecycle:onboarding_detail' ob.id %}" class="btn btn-sm btn-outline-primary">Tasks</a></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No active onboardings.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/lifecycle/onboarding_detail.html", """{% extends 'base.html' %}
{% block title %}Onboarding {{ workflow.employee.full_name }} — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-check2-circle text-success"></i> Onboarding: {{ workflow.employee.full_name }}</h1>
        <p class="ems-page-subheading">Joining Date: {{ workflow.joining_date }} | Mentor: {{ workflow.mentor_buddy.full_name|default:"Assigned Mentor" }}</p>
    </div>
    <a href="{% url 'lifecycle:onboarding_list' %}" class="btn btn-outline-secondary"><i class="bi bi-arrow-left me-1"></i>Back</a>
</div>

<div class="ems-card p-4">
    <h5 class="fw-bold mb-3">Onboarding Milestones Checklist</h5>
    <div class="row g-3">
        <div class="col-md-6"><div class="p-3 border rounded-3 d-flex justify-content-between align-items-center"><span>Welcome Email Dispatched</span><span class="badge bg-success">Done</span></div></div>
        <div class="col-md-6"><div class="p-3 border rounded-3 d-flex justify-content-between align-items-center"><span>Laptop & IT Hardware Allocated</span><span class="badge bg-success">Done</span></div></div>
        <div class="col-md-6"><div class="p-3 border rounded-3 d-flex justify-content-between align-items-center"><span>HR Orientation & Benefits Briefing</span><span class="badge bg-success">Done</span></div></div>
        <div class="col-md-6"><div class="p-3 border rounded-3 d-flex justify-content-between align-items-center"><span>Security Access Card & Badge Issued</span><span class="badge bg-success">Done</span></div></div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/lifecycle/resignation_list.html", """{% extends 'base.html' %}
{% block title %}Resignations — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-box-arrow-right text-danger"></i> Resignation & Offboarding Tracker</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Resignation Date</th><th>Proposed Exit</th><th>Reason Category</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>{% for r in resignations %}
        <tr>
            <td><strong>{{ r.employee.full_name }}</strong></td>
            <td>{{ r.resignation_date }}</td>
            <td>{{ r.proposed_last_working_day }}</td>
            <td>{{ r.get_reason_category_display }}</td>
            <td><span class="badge bg-danger">{{ r.get_status_display }}</span></td>
            <td><a href="{% url 'lifecycle:resignation_detail' r.id %}" class="btn btn-sm btn-outline-danger">Clearances</a></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No resignations.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/lifecycle/resignation_detail.html", """{% extends 'base.html' %}
{% block title %}Exit Clearances {{ resignation.employee.full_name }} — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-shield-x text-danger"></i> Exit Clearances: {{ resignation.employee.full_name }}</h1>
        <p class="ems-page-subheading">Notice Date: {{ resignation.resignation_date }} | Status: {{ resignation.get_status_display }}</p>
    </div>
    <a href="{% url 'lifecycle:resignation_list' %}" class="btn btn-outline-secondary"><i class="bi bi-arrow-left me-1"></i>Back</a>
</div>

<div class="ems-card p-4">
    <h5 class="fw-bold mb-3">Multi-Department Exit Clearance Sign-offs</h5>
    <div class="table-responsive">
        <table class="ems-table">
            <thead><tr><th>Department</th><th>Status</th><th>Pending Items / Assets</th><th>Cleared By</th></tr></thead>
            <tbody>{% for cl in clearances %}
                <tr>
                    <td><strong>{{ cl.get_department_name_display }}</strong></td>
                    <td><span class="badge {% if cl.is_cleared %}bg-success{% else %}bg-warning text-dark{% endif %}">{% if cl.is_cleared %}Cleared{% else %}Pending Return{% endif %}</span></td>
                    <td>{{ cl.pending_items|default:"None" }}</td>
                    <td>{{ cl.cleared_by.first_name|default:"Department Lead" }}</td>
                </tr>
            {% empty %}<tr><td colspan="4" class="text-center py-3 text-muted">All department clearances initialized.</td></tr>{% endfor %}</tbody>
        </table>
    </div>
</div>
{% endblock %}
""")

write_file("templates/lifecycle/experience_certificate.html", """{% extends 'base.html' %}
{% block title %}Experience Certificate — Smart EMS{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <a href="{% url 'lifecycle:dashboard' %}" class="btn btn-outline-secondary"><i class="bi bi-arrow-left me-1"></i>Back</a>
    <button onclick="window.print()" class="btn btn-primary"><i class="bi bi-printer me-1"></i>Print Certificate</button>
</div>

<div class="card border shadow-sm p-5 bg-white rounded-4" style="max-width: 800px; margin: 0 auto;">
    <div class="text-center border-bottom pb-4 mb-4">
        <h2 class="fw-bold text-primary mb-1">BHARAT ENTERPRISE SOLUTIONS</h2>
        <p class="text-muted small mb-0">Corporate Headquarters | Human Resources & Workforce Division</p>
    </div>

    <div class="text-center my-4">
        <h4 class="fw-bold text-uppercase text-dark text-decoration-underline">EXPERIENCE & RELIEVING CERTIFICATE</h4>
        <div class="text-muted small mt-1">Certificate Ref No: {{ cert.certificate_number }}</div>
    </div>

    <div class="lead fs-6 lh-lg my-4 text-dark">
        <p>This is to certify that <strong>{{ cert.employee.full_name }}</strong> (Employee ID: <strong>{{ cert.employee.employee_id }}</strong>) was employed with Bharat Enterprise Solutions from <strong>{{ cert.joining_date }}</strong> to <strong>{{ cert.relieving_date }}</strong>.</p>
        <p>During their tenure, they served in the capacity of <strong>{{ cert.last_designation }}</strong>. Their conduct and performance throughout their service were found to be <strong>{{ cert.conduct_remarks }}</strong>.</p>
        <p>We thank them for their valuable contributions and wish them the very best in all their future professional endeavors.</p>
    </div>

    <div class="d-flex justify-content-between align-items-end mt-5 pt-5">
        <div>
            <div>Date of Issue: {{ cert.issued_date }}</div>
            <div>Place: Bengaluru, India</div>
        </div>
        <div class="text-end">
            <div class="fw-bold text-primary">{{ cert.authorized_signatory_name }}</div>
            <div class="text-muted small">Authorized Signatory, Human Resources</div>
        </div>
    </div>
</div>
{% endblock %}
""")

# ==============================================================================
# COMPLIANCE TEMPLATES
# ==============================================================================

write_file("templates/compliance/dashboard.html", """{% extends 'base.html' %}
{% block title %}Compliance & Legal — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-shield-lock-fill text-danger"></i> Statutory & Labor Law Compliance</h1>
        <p class="ems-page-subheading">Labor law registers (Form A, B, C, D), statutory audits, POSH committee & corporate policy adherence</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{% url 'compliance:register_list' %}" class="btn btn-outline-primary"><i class="bi bi-file-earmark-spreadsheet me-1"></i>Statutory Registers</a>
        <a href="{% url 'compliance:posh_portal' %}" class="btn btn-outline-danger"><i class="bi bi-shield-heart me-1"></i>POSH Committee</a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Statutory Registers</div><h3 class="fw-bold text-success mb-0">100% Up to Date</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Audit Compliance Score</div><h3 class="fw-bold text-primary mb-0">98% Grade A</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Policy Acknowledgments</div><h3 class="fw-bold text-info mb-0">{{ total_acks }} Signed</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">POSH IC Members</div><h3 class="fw-bold text-danger mb-0">{{ posh_members.count }} Active</h3></div></div>
</div>

<div class="row g-3">
    <div class="col-12 col-lg-7">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Mandatory Statutory Registers (Labor Bureau)</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Register Name</th><th>Period</th><th>Verification Officer</th><th>Status</th></tr></thead>
                <tbody>{% for r in registers %}
                    <tr>
                        <td><strong>{{ r.title }}</strong></td>
                        <td>{{ r.period_year }}/{{ r.period_month }}</td>
                        <td>{{ r.verified_by_officer }}</td>
                        <td><span class="badge bg-success">Certified & Signed</span></td>
                    </tr>
                {% empty %}<tr><td colspan="4" class="text-center py-4 text-muted">No statutory registers.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
    <div class="col-12 col-lg-5">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Statutory Audits History</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Audit</th><th>Score</th><th>Status</th></tr></thead>
                <tbody>{% for a in audits %}
                    <tr>
                        <td><strong>{{ a.title }}</strong><div class="text-muted small">{{ a.auditor_agency }}</div></td>
                        <td class="fw-bold text-success">{{ a.score_percentage }}%</td>
                        <td><span class="badge bg-success">{{ a.get_status_display }}</span></td>
                    </tr>
                {% empty %}<tr><td colspan="3" class="text-center py-4 text-muted">No audits recorded.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/compliance/register_list.html", """{% extends 'base.html' %}
{% block title %}Statutory Registers — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-file-earmark-ruled text-primary"></i> Statutory Labor Registers</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Register Title</th><th>Type</th><th>Period</th><th>Verified By</th><th>Status</th></tr></thead>
    <tbody>{% for r in registers %}
        <tr>
            <td><strong>{{ r.title }}</strong></td>
            <td><span class="badge bg-light text-dark border">{{ r.get_register_type_display }}</span></td>
            <td>{{ r.period_year }}/{{ r.period_month }}</td>
            <td>{{ r.verified_by_officer }}</td>
            <td><span class="badge bg-success">Compliant & Archived</span></td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center py-4 text-muted">No registers.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/compliance/audit_list.html", """{% extends 'base.html' %}
{% block title %}Compliance Audits — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-clipboard2-check text-primary"></i> External & Internal Audits</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Audit Title</th><th>Date</th><th>Agency</th><th>Lead Auditor</th><th>Compliance Score</th><th>Status</th></tr></thead>
    <tbody>{% for a in audits %}
        <tr>
            <td><strong>{{ a.title }}</strong></td>
            <td>{{ a.audit_date }}</td>
            <td>{{ a.auditor_agency }}</td>
            <td>{{ a.lead_auditor }}</td>
            <td class="fw-bold text-success">{{ a.score_percentage }}%</td>
            <td><span class="badge bg-success">{{ a.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No audits.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/compliance/posh_portal.html", """{% extends 'base.html' %}
{% block title %}POSH Committee — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-shield-heart-fill text-danger"></i> POSH Internal Committee Portal</h1>
        <p class="ems-page-subheading">Prevention of Sexual Harassment (POSH Act) governance & confidential redressal</p>
    </div>
</div>
<div class="ems-card p-4">
    <h5 class="fw-bold mb-3">Internal Committee (IC) Members</h5>
    <div class="row g-3">
        {% for m in posh_members %}
            <div class="col-md-6">
                <div class="p-3 border rounded-3 bg-light">
                    <div class="fw-bold text-primary fs-6">{{ m.employee.full_name }}</div>
                    <div class="badge bg-danger-subtle text-danger border mt-1">{{ m.get_role_title_display }}</div>
                    <div class="mt-2 small"><strong>Email:</strong> {{ m.contact_email }}</div>
                    <div class="small"><strong>Phone:</strong> {{ m.contact_phone }}</div>
                </div>
            </div>
        {% empty %}<p class="text-muted">No members configured.</p>{% endfor %}
    </div>
</div>
{% endblock %}
""")

# ==============================================================================
# BENEFITS TEMPLATES
# ==============================================================================

write_file("templates/benefits/dashboard.html", """{% extends 'base.html' %}
{% block title %}Corporate Benefits & Insurance — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-heart-pulse-fill text-danger"></i> Corporate Benefits & Health Insurance</h1>
        <p class="ems-page-subheading">Group mediclaim floater policies, dependent enrollments, claims & flexible benefit allowances</p>
    </div>
    <a href="{% url 'benefits:claims_list' %}" class="btn btn-primary"><i class="bi bi-receipt me-1"></i>Track Claims</a>
</div>

<div class="row g-3 mb-4">
    <div class="col-md-4"><div class="ems-card p-3"><div class="text-muted small">Corporate Policies</div><h3 class="fw-bold text-primary mb-0">{{ policies.count }} Active</h3></div></div>
    <div class="col-md-4"><div class="ems-card p-3"><div class="text-muted small">Cashless Network Hospitals</div><h3 class="fw-bold text-success mb-0">12,000+ Nationwide</h3></div></div>
    <div class="col-md-4"><div class="ems-card p-3"><div class="text-muted small">TPA Support</div><h3 class="fw-bold text-dark mb-0">1800-425-9449</h3></div></div>
</div>

<div class="ems-card">
    <div class="ems-card-header"><h5 class="fw-bold mb-0">Active Group Insurance Policies</h5></div>
    <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
        <thead><tr><th>Policy Name</th><th>Policy No</th><th>Provider</th><th>Sum Insured</th><th>TPA Administrator</th><th>Status</th></tr></thead>
        <tbody>{% for p in policies %}
            <tr>
                <td><strong>{{ p.name }}</strong></td>
                <td><span class="badge bg-light text-dark border">{{ p.policy_number }}</span></td>
                <td>{{ p.provider_name }}</td>
                <td class="fw-bold text-success">₹{{ p.sum_insured|floatformat:0 }}</td>
                <td>{{ p.tpa_name }}</td>
                <td><span class="badge bg-success">Active</span></td>
            </tr>
        {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No policies active.</td></tr>{% endfor %}</tbody>
    </table></div></div>
</div>
{% endblock %}
""")

write_file("templates/benefits/policy_list.html", """{% extends 'base.html' %}
{% block title %}Insurance Policies — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-shield-plus text-primary"></i> Company Insurance Policies</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Policy Name</th><th>Policy Number</th><th>Type</th><th>Provider</th><th>Sum Insured</th></tr></thead>
    <tbody>{% for p in policies %}
        <tr>
            <td><strong>{{ p.name }}</strong></td>
            <td>{{ p.policy_number }}</td>
            <td>{{ p.get_policy_type_display }}</td>
            <td>{{ p.provider_name }}</td>
            <td class="fw-bold text-success">₹{{ p.sum_insured|floatformat:0 }}</td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center py-4 text-muted">No policies.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/benefits/claims_list.html", """{% extends 'base.html' %}
{% block title %}Insurance Claims — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-receipt-cutoff text-primary"></i> Health Insurance Claims Tracker</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Claim ID</th><th>Employee / Patient</th><th>Hospital</th><th>Claimed Amount</th><th>Approved Amount</th><th>Status</th></tr></thead>
    <tbody>{% for c in claims %}
        <tr>
            <td><span class="badge bg-light text-dark border">{{ c.claim_id }}</span></td>
            <td><strong>{{ c.enrollment.employee.full_name }}</strong> ({{ c.patient_name }})</td>
            <td>{{ c.hospital_name }}</td>
            <td>₹{{ c.claimed_amount|floatformat:2 }}</td>
            <td class="fw-bold text-success">₹{{ c.approved_amount|floatformat:2 }}</td>
            <td><span class="badge bg-success">{{ c.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No claims filed.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

# ==============================================================================
# TIMESHEETS TEMPLATES
# ==============================================================================

write_file("templates/timesheets/dashboard.html", """{% extends 'base.html' %}
{% block title %}Timesheets & Billing — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-clock-history text-warning"></i> Client Project Timesheets & Billing</h1>
        <p class="ems-page-subheading">Weekly billable hours tracking, project rate cards & manager sign-off workflows</p>
    </div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Week Starting</th><th>Week Ending</th><th>Billable Hours</th><th>Non-Billable</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>{% for t in timesheets %}
        <tr>
            <td><strong>{{ t.employee.full_name }}</strong></td>
            <td>{{ t.week_start_date }}</td>
            <td>{{ t.week_end_date }}</td>
            <td class="fw-bold text-success">{{ t.total_billable_hours }} hrs</td>
            <td>{{ t.total_non_billable_hours }} hrs</td>
            <td><span class="badge {% if t.status == 'APPROVED' %}bg-success{% else %}bg-warning text-dark{% endif %}">{{ t.get_status_display }}</span></td>
            <td><a href="{% url 'timesheets:timesheet_detail' t.id %}" class="btn btn-sm btn-outline-primary">Details</a></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center py-4 text-muted">No timesheets submitted.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/timesheets/timesheet_detail.html", """{% extends 'base.html' %}
{% block title %}Timesheet Details — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-calendar3 text-primary"></i> Timesheet: {{ timesheet.employee.full_name }}</h1>
        <p class="ems-page-subheading">{{ timesheet.week_start_date }} to {{ timesheet.week_end_date }} | Status: {{ timesheet.get_status_display }}</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{% url 'timesheets:dashboard' %}" class="btn btn-outline-secondary"><i class="bi bi-arrow-left me-1"></i>Back</a>
        {% if timesheet.status != 'APPROVED' %}
            <a href="{% url 'timesheets:timesheet_approval' timesheet.id %}" class="btn btn-success"><i class="bi bi-check-lg me-1"></i>Approve Timesheet</a>
        {% endif %}
    </div>
</div>

<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Date</th><th>Project</th><th>Hours Logged</th><th>Billable?</th><th>Task Description</th></tr></thead>
    <tbody>{% for e in entries %}
        <tr>
            <td>{{ e.entry_date }}</td>
            <td><strong>{{ e.project.name }}</strong></td>
            <td class="fw-bold">{{ e.hours_logged }} hrs</td>
            <td>{% if e.is_billable %}<span class="badge bg-success">Yes</span>{% else %}<span class="badge bg-secondary">No</span>{% endif %}</td>
            <td>{{ e.task_description }}</td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center py-4 text-muted">No individual log entries.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

# ==============================================================================
# SURVEYS TEMPLATES
# ==============================================================================

write_file("templates/surveys/dashboard.html", """{% extends 'base.html' %}
{% block title %}Employee Surveys & eNPS — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-chat-heart-fill text-danger"></i> Employee Net Promoter Score & Surveys</h1>
        <p class="ems-page-subheading">Anonymous workforce sentiment analytics, quarterly eNPS & pulse feedback</p>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Workforce eNPS Index</div><h2 class="fw-bold text-success mb-0">+{{ enps_index }}</h2><div class="small text-muted">World-class benchmark</div></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Total Responses</div><h3 class="fw-bold text-dark mb-0">{{ total_submissions }} Staff</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Promoters (9-10)</div><h3 class="fw-bold text-success mb-0">{{ promoters_count }}</h3></div></div>
    <div class="col-md-3"><div class="ems-card p-3"><div class="text-muted small">Detractors (0-6)</div><h3 class="fw-bold text-danger mb-0">{{ detractors_count }}</h3></div></div>
</div>

<div class="ems-card">
    <div class="ems-card-header"><h5 class="fw-bold mb-0">Active Organization Surveys</h5></div>
    <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
        <thead><tr><th>Survey Title</th><th>Type</th><th>Start Date</th><th>End Date</th><th>Anonymous?</th><th>Action</th></tr></thead>
        <tbody>{% for s in surveys %}
            <tr>
                <td><strong>{{ s.title }}</strong></td>
                <td><span class="badge bg-primary">{{ s.get_survey_type_display }}</span></td>
                <td>{{ s.start_date }}</td>
                <td>{{ s.end_date }}</td>
                <td><span class="badge bg-success">100% Anonymous</span></td>
                <td><a href="{% url 'surveys:survey_detail' s.id %}" class="btn btn-sm btn-outline-primary">Participate</a></td>
            </tr>
        {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No surveys active.</td></tr>{% endfor %}</tbody>
    </table></div></div>
</div>
{% endblock %}
""")

write_file("templates/surveys/survey_detail.html", """{% extends 'base.html' %}
{% block title %}{{ survey.title }} — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-ui-checks text-primary"></i> {{ survey.title }}</h1>
        <p class="ems-page-subheading">{{ survey.description }}</p>
    </div>
    <a href="{% url 'surveys:dashboard' %}" class="btn btn-outline-secondary"><i class="bi bi-arrow-left me-1"></i>Back</a>
</div>

<div class="ems-card p-4">
    <h5 class="fw-bold mb-3">Survey Questionnaire</h5>
    {% for q in questions %}
        <div class="p-3 border rounded-3 mb-3 bg-light">
            <div class="fw-bold text-dark">{{ forloop.counter }}. {{ q.prompt_text }}</div>
            <div class="text-muted small mt-1">Scale: {{ q.get_question_type_display }}</div>
        </div>
    {% empty %}<p class="text-muted">No questions configured.</p>{% endfor %}
</div>
{% endblock %}
""")

# ==============================================================================
# WORKPLACE TEMPLATES
# ==============================================================================

write_file("templates/workplace/dashboard.html", """{% extends 'base.html' %}
{% block title %}Smart Workplace & Desks — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-building-gear text-primary"></i> Smart Workplace & Travel Management</h1>
        <p class="ems-page-subheading">Hot-desking reservations, meeting room calendars, visitor passes & corporate travel authorizations</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{% url 'workplace:desk_booking' %}" class="btn btn-primary"><i class="bi bi-laptop me-1"></i>Book Desk</a>
        <a href="{% url 'workplace:travel_list' %}" class="btn btn-outline-primary"><i class="bi bi-airplane me-1"></i>Travel Requests</a>
    </div>
</div>

<div class="row g-3">
    <div class="col-12 col-lg-6">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Meeting Rooms & Pods</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Room Name</th><th>Floor</th><th>Seats</th><th>VC Equipped</th></tr></thead>
                <tbody>{% for r in meeting_rooms %}
                    <tr>
                        <td><strong>{{ r.name }}</strong></td>
                        <td>{{ r.floor }}</td>
                        <td>{{ r.capacity_seats }} Seats</td>
                        <td><span class="badge bg-success">Zoom / Meet Enabled</span></td>
                    </tr>
                {% empty %}<tr><td colspan="4" class="text-center py-4 text-muted">No rooms configured.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
    <div class="col-12 col-lg-6">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Corporate Travel Authorizations</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Traveler</th><th>Destination</th><th>Departure</th><th>Status</th></tr></thead>
                <tbody>{% for t in travel_requests %}
                    <tr>
                        <td><strong>{{ t.employee.full_name }}</strong></td>
                        <td>{{ t.destination_city }}</td>
                        <td>{{ t.departure_date }}</td>
                        <td><span class="badge bg-success">{{ t.get_status_display }}</span></td>
                    </tr>
                {% empty %}<tr><td colspan="4" class="text-center py-4 text-muted">No travel requests.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/workplace/travel_list.html", """{% extends 'base.html' %}
{% block title %}Corporate Travel — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-airplane-fill text-primary"></i> Business Travel Requests</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Purpose</th><th>Origin</th><th>Destination</th><th>Dates</th><th>Estimated Budget</th><th>Status</th></tr></thead>
    <tbody>{% for t in travels %}
        <tr>
            <td><strong>{{ t.employee.full_name }}</strong></td>
            <td>{{ t.purpose }}</td>
            <td>{{ t.origin_city }}</td>
            <td>{{ t.destination_city }}</td>
            <td>{{ t.departure_date }} to {{ t.return_date }}</td>
            <td class="fw-bold">₹{{ t.estimated_total_cost|floatformat:0 }}</td>
            <td><span class="badge bg-success">{{ t.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center py-4 text-muted">No travels.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

write_file("templates/workplace/desk_booking.html", """{% extends 'base.html' %}
{% block title %}Desk Reservations — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-laptop text-primary"></i> Hot-Desking & Workstation Reservations</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Desk No</th><th>Employee</th><th>Building / Floor</th><th>Date</th><th>Slot</th><th>Status</th></tr></thead>
    <tbody>{% for b in bookings %}
        <tr>
            <td><strong>{{ b.desk_number }}</strong></td>
            <td>{{ b.employee.full_name }}</td>
            <td>{{ b.building }} - {{ b.floor }}</td>
            <td>{{ b.booking_date }}</td>
            <td>{{ b.get_time_slot_display }}</td>
            <td><span class="badge bg-success">Checked In</span></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center py-4 text-muted">No bookings.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}
""")

# ==============================================================================
# API & AUTOMATION TEMPLATES
# ==============================================================================

write_file("templates/api/documentation.html", """{% extends 'base.html' %}
{% block title %}Developer REST API Docs — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-code-slash text-primary"></i> Developer REST API & Webhooks Suite</h1>
        <p class="ems-page-subheading">Integrate external biometric gates, ERPs, mobile clients & microservices via JSON REST APIs</p>
    </div>
</div>

<div class="row g-3">
    <div class="col-12 col-lg-8">
        <div class="ems-card p-4">
            <h5 class="fw-bold mb-3">Available Core API Endpoints</h5>
            <div class="d-flex flex-column gap-3">
                {% for ep in endpoints %}
                    <div class="p-3 border rounded-3 bg-light">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <span class="badge {% if ep.method == 'GET' %}bg-success{% else %}bg-primary{% endif %} px-2 py-1">{{ ep.method }}</span>
                            <code class="fw-bold text-dark fs-6">{{ ep.path }}</code>
                        </div>
                        <p class="text-muted small mb-0">{{ ep.desc }}</p>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="col-12 col-lg-4">
        <div class="ems-card p-4">
            <h5 class="fw-bold mb-3">Your API Keys</h5>
            {% for k in api_keys %}
                <div class="border rounded-3 p-2 mb-2 bg-light">
                    <div class="fw-semibold small">{{ k.name }}</div>
                    <code class="small text-break">{{ k.key }}</code>
                </div>
            {% empty %}<p class="text-muted small">No custom API keys registered for this session.</p>{% endfor %}
        </div>
    </div>
</div>
{% endblock %}
""")

write_file("templates/automation/dashboard.html", """{% extends 'base.html' %}
{% block title %}Smart Automation Engine — Smart EMS{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-cpu-fill text-warning"></i> Event-Driven Workflow Automation Engine</h1>
        <p class="ems-page-subheading">Build event-condition-action triggers across employee milestones, leave approvals & alerts</p>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-md-6"><div class="ems-card p-3"><div class="text-muted small">Active Automation Rules</div><h3 class="fw-bold text-primary mb-0">{{ active_count }} Rules</h3></div></div>
    <div class="col-md-6"><div class="ems-card p-3"><div class="text-muted small">Total Triggered Actions</div><h3 class="fw-bold text-success mb-0">{{ total_runs }} Dispatches</h3></div></div>
</div>

<div class="row g-3">
    <div class="col-12 col-lg-7">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Active Automation Rules</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Rule Name</th><th>Trigger Event</th><th>Action</th><th>Runs</th><th>Action</th></tr></thead>
                <tbody>{% for r in rules %}
                    <tr>
                        <td><strong>{{ r.name }}</strong></td>
                        <td><span class="badge bg-light text-dark border">{{ r.get_trigger_event_display }}</span></td>
                        <td><span class="badge bg-primary-subtle text-primary">{{ r.get_action_type_display }}</span></td>
                        <td>{{ r.total_executions }}</td>
                        <td><a href="{% url 'automation:trigger_rule' r.id %}" class="btn btn-sm btn-outline-success">Simulate</a></td>
                    </tr>
                {% empty %}<tr><td colspan="5" class="text-center py-4 text-muted">No rules.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
    <div class="col-12 col-lg-5">
        <div class="ems-card">
            <div class="ems-card-header"><h5 class="fw-bold mb-0">Recent Execution Logs</h5></div>
            <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
                <thead><tr><th>Rule</th><th>Time</th><th>Status</th></tr></thead>
                <tbody>{% for l in logs %}
                    <tr>
                        <td><strong>{{ l.rule.name }}</strong></td>
                        <td class="small text-muted">{{ l.executed_at|date:"M d, H:i" }}</td>
                        <td><span class="badge bg-success">{{ l.status }}</span></td>
                    </tr>
                {% empty %}<tr><td colspan="3" class="text-center py-4 text-muted">No executions.</td></tr>{% endfor %}</tbody>
            </table></div></div>
        </div>
    </div>
</div>
{% endblock %}
""")

print("Finished all enterprise module templates generation.")
