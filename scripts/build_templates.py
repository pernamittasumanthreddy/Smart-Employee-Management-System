import os

TEMPLATE_FILES = {
    # ----------------------------------------------------
    # Organization Templates
    # ----------------------------------------------------
    "templates/organization/department_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-building text-primary"></i> {{ title }}</h1>
        <p class="ems-page-subheading">Configure department details, operational budget, and leadership</p>
    </div>
</div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Department Name *</label>{{ form.name }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Department Code *</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Head of Department</label>{{ form.head_of_department }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Annual Operating Budget ($)</label>{{ form.budget }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Office Location / Floor</label>{{ form.location }}</div>
        <div class="col-12 col-md-6 form-check mt-4 ms-2">{{ form.is_active }} <label class="form-check-label small fw-semibold">Active Status</label></div>
        <div class="col-12"><label class="form-label small fw-semibold">Department Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
        <a href="{% url 'organization:department_list' %}" class="btn btn-outline-secondary">Cancel</a>
        <button type="submit" class="btn btn-primary px-4">Save Department</button>
    </div>
</form></div></div>
{% endblock %}""",

    "templates/organization/team_list.html": """{% extends 'base.html' %}
{% block title %}Teams — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-people-fill text-primary"></i> Organizational Teams & Squads</h1>
        <p class="ems-page-subheading">Cross-functional and functional workforce team structures</p>
    </div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'organization:team_create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Add Team</a>{% endif %}</div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Team</th><th>Code</th><th>Department</th><th>Team Lead</th><th>Members</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>{% for t in teams %}
        <tr>
            <td><strong>{{ t.name }}</strong></td>
            <td><span class="badge bg-light text-dark border">{{ t.code }}</span></td>
            <td>{{ t.department.name }}</td>
            <td>{{ t.team_lead.full_name|default:"Not Assigned" }}</td>
            <td><span class="badge bg-primary">{{ t.total_members }} Members</span></td>
            <td><span class="ems-badge ems-badge-success">Active</span></td>
            <td>{% if is_hr_or_admin %}<a href="{% url 'organization:team_update' t.id %}" class="btn btn-sm btn-outline-secondary py-0"><i class="bi bi-pencil"></i></a>{% endif %}</td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center text-muted py-4">No teams created.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/organization/team_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Team Name *</label>{{ form.name }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Team Code *</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Parent Department *</label>{{ form.department }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Team Lead</label>{{ form.team_lead }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
        <a href="{% url 'organization:team_list' %}" class="btn btn-outline-secondary">Cancel</a>
        <button type="submit" class="btn btn-primary px-4">Save Team</button>
    </div>
</form></div></div>
{% endblock %}""",

    "templates/organization/designation_list.html": """{% extends 'base.html' %}
{% block title %}Designations — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-award-fill text-primary"></i> Job Titles & Designations</h1></div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'organization:designation_create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Add Designation</a>{% endif %}</div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Designation Title</th><th>Code</th><th>Department</th><th>Grade</th><th>Salary Band</th></tr></thead>
    <tbody>{% for d in designations %}
        <tr>
            <td><strong>{{ d.title }}</strong></td>
            <td><span class="badge bg-light text-dark border">{{ d.code }}</span></td>
            <td>{{ d.department.name }}</td>
            <td><span class="badge bg-secondary">{{ d.grade_level }}</span></td>
            <td>${{ d.min_salary }} - ${{ d.max_salary }}</td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center text-muted py-4">No designations found.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/organization/designation_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Designation Title *</label>{{ form.title }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Code *</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Department *</label>{{ form.department }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Grade Level</label>{{ form.grade_level }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Min Salary ($)</label>{{ form.min_salary }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Max Salary ($)</label>{{ form.max_salary }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
        <a href="{% url 'organization:designation_list' %}" class="btn btn-outline-secondary">Cancel</a>
        <button type="submit" class="btn btn-primary px-4">Save Designation</button>
    </div>
</form></div></div>
{% endblock %}""",

    "templates/organization/org_chart.html": """{% extends 'base.html' %}
{% block title %}Organization Structure Hierarchy — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-diagram-3-fill text-primary"></i> Organizational Hierarchy & Reporting Trees</h1>
        <p class="ems-page-subheading">Visual structural mapping of departments, squads, leads, and staff</p>
    </div>
</div>
<div class="row g-4">
    {% for dept in departments %}
    <div class="col-12 col-lg-6">
        <div class="ems-card h-100">
            <div class="ems-card-header bg-light">
                <div>
                    <h5 class="fw-bold text-dark mb-0">{{ dept.name }}</h5>
                    <span class="small text-muted">Head: {{ dept.head_of_department.full_name|default:"Not Assigned" }}</span>
                </div>
                <span class="badge bg-primary">{{ dept.employees.count }} Staff</span>
            </div>
            <div class="ems-card-body">
                <h6 class="fw-bold small text-uppercase text-secondary mb-2">Teams in Department:</h6>
                <div class="list-group list-group-flush border rounded mb-3">
                    {% for team in dept.teams.all %}
                    <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <strong>{{ team.name }}</strong>
                            <div class="small text-muted">Lead: {{ team.team_lead.full_name|default:"Open Lead" }}</div>
                        </div>
                        <span class="badge bg-light text-dark border">{{ team.members.count }} Members</span>
                    </div>
                    {% empty %}
                    <div class="list-group-item text-muted small">No teams assigned.</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    "templates/organization/org_profile.html": """{% extends 'base.html' %}
{% block title %}Organization Profile — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-building-gear text-primary"></i> Company & Corporate Profile</h1></div>
</div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Company Legal Name</label>{{ form.name }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Tax ID / EIN</label>{{ form.tax_id }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Corporate Email</label>{{ form.email }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Phone</label>{{ form.phone }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Website</label>{{ form.website }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Primary Currency</label>{{ form.currency }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Headquarters Address</label>{{ form.address }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">City</label>{{ form.city }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">State</label>{{ form.state }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Country</label>{{ form.country }}</div>
    </div>
    <div class="d-flex justify-content-end mt-4"><button type="submit" class="btn btn-primary px-4">Update Profile</button></div>
</form></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Permissions Templates
    # ----------------------------------------------------
    "templates/permissions/role_list.html": """{% extends 'base.html' %}
{% block title %}Roles & Permissions — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-shield-lock-fill text-primary"></i> Role-Based Access Control (RBAC)</h1>
        <p class="ems-page-subheading">Fine-grained module permissions across Administrator, HR Manager, Team Manager, and Employee</p>
    </div>
</div>
<div class="row g-4">
    {% for role in roles %}
    <div class="col-12 col-md-6">
        <div class="ems-card h-100">
            <div class="ems-card-header">
                <div>
                    <h5 class="fw-bold mb-0 text-dark">{{ role.name }}</h5>
                    <span class="badge bg-light text-primary border font-monospace">{{ role.code }}</span>
                </div>
                <a href="{% url 'permissions:role_matrix' role.id %}" class="btn btn-sm btn-primary">
                    <i class="bi bi-grid-3x3 me-1"></i>Configure Matrix
                </a>
            </div>
            <div class="ems-card-body">
                <p class="text-muted small mb-3">{{ role.description }}</p>
                <h6 class="fw-bold small text-uppercase text-secondary">Active Module Permissions:</h6>
                <div class="d-flex flex-wrap gap-1">
                    {% for perm in role.permissions.all %}
                        {% if perm.can_read %}
                        <span class="badge bg-light text-dark border small">{{ perm.get_module_display }}</span>
                        {% endif %}
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    "templates/permissions/role_matrix.html": """{% extends 'base.html' %}
{% block title %}Permission Matrix: {{ role.name }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-grid-3x3-gap-fill text-primary"></i> Permission Matrix: {{ role.name }}</h1>
        <p class="ems-page-subheading">Define Create, Read, Update, Delete, and Approval rights per module</p>
    </div>
    <a href="{% url 'permissions:role_list' %}" class="btn btn-outline-secondary btn-sm"><i class="bi bi-arrow-left me-1"></i>Back to Roles</a>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><form method="post">{% csrf_token %}
    <div class="table-responsive"><table class="ems-table">
        <thead>
            <tr>
                <th>Module</th>
                <th class="text-center">Create</th>
                <th class="text-center">Read</th>
                <th class="text-center">Update</th>
                <th class="text-center">Delete</th>
                <th class="text-center">Approve</th>
            </tr>
        </thead>
        <tbody>
            {% for item in matrix_data %}
            <tr>
                <td><strong>{{ item.name }}</strong> ({{ item.code }})</td>
                <td class="text-center"><input type="checkbox" name="create_{{ item.code }}" class="form-check-input" {% if item.can_create %}checked{% endif %}></td>
                <td class="text-center"><input type="checkbox" name="read_{{ item.code }}" class="form-check-input" {% if item.can_read %}checked{% endif %}></td>
                <td class="text-center"><input type="checkbox" name="update_{{ item.code }}" class="form-check-input" {% if item.can_update %}checked{% endif %}></td>
                <td class="text-center"><input type="checkbox" name="delete_{{ item.code }}" class="form-check-input" {% if item.can_delete %}checked{% endif %}></td>
                <td class="text-center"><input type="checkbox" name="approve_{{ item.code }}" class="form-check-input" {% if item.can_approve %}checked{% endif %}></td>
            </tr>
            {% endfor %}
        </tbody>
    </table></div>
    <div class="p-3 bg-light border-top d-flex justify-content-end gap-2">
        <a href="{% url 'permissions:role_list' %}" class="btn btn-outline-secondary">Cancel</a>
        <button type="submit" class="btn btn-primary px-4">Save Matrix Configuration</button>
    </div>
</form></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Attendance Templates
    # ----------------------------------------------------
    "templates/attendance/my_attendance.html": """{% extends 'base.html' %}
{% block title %}My Attendance & Timesheets — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-clock-history text-primary"></i> My Attendance & Timesheet Logs</h1>
        <p class="ems-page-subheading">Track your check-in/out records, working hours, and punctuality score</p>
    </div>
</div>
<div class="row g-3 mb-4">
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Present Days</div><div class="ems-stat-value text-success">{{ present_days }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Late Arrivals</div><div class="ems-stat-value text-warning">{{ late_days }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Unplanned Absences</div><div class="ems-stat-value text-danger">{{ absent_days }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Average Working Hours</div><div class="ems-stat-value text-primary">{{ avg_hours }}h</div></div></div></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Date</th><th>Check In</th><th>Check Out</th><th>Working Hours</th><th>Status</th></tr></thead>
    <tbody>{% for r in records %}
        <tr>
            <td><strong>{{ r.date }}</strong></td>
            <td>{{ r.check_in_time|default:"--" }} {% if r.is_late %}<span class="badge bg-warning text-dark small">Late</span>{% endif %}</td>
            <td>{{ r.check_out_time|default:"--" }} {% if r.is_early_departure %}<span class="badge bg-info text-dark small">Early</span>{% endif %}</td>
            <td>{{ r.total_working_hours }} hrs</td>
            <td><span class="ems-badge {% if r.status == 'PRESENT' %}ems-badge-success{% elif r.status == 'ABSENT' %}ems-badge-danger{% else %}ems-badge-warning{% endif %}">{{ r.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center text-muted py-4">No records found.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/attendance/attendance_roster.html": """{% extends 'base.html' %}
{% block title %}Daily Attendance Roster — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-calendar2-range text-primary"></i> Daily Attendance Roster</h1></div>
</div>
<div class="ems-filter-bar mb-4">
    <form method="get" class="d-flex flex-wrap gap-2 w-100 align-items-center">
        <input type="date" name="date" class="form-control form-control-sm" style="width: auto;" value="{{ target_date|date:'Y-m-d' }}">
        <select name="department" class="form-select form-select-sm" style="width: auto;">
            <option value="">All Departments</option>
            {% for d in departments %}<option value="{{ d.id }}" {% if selected_dept == d.id|stringformat:"i" %}selected{% endif %}>{{ d.name }}</option>{% endfor %}
        </select>
        <button type="submit" class="btn btn-sm btn-primary">Filter Roster</button>
    </form>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Department</th><th>Check In</th><th>Check Out</th><th>Hours</th><th>Status</th></tr></thead>
    <tbody>{% for r in records %}
        <tr>
            <td><strong>{{ r.employee.full_name }}</strong></td>
            <td>{{ r.employee.department.name|default:"--" }}</td>
            <td>{{ r.check_in_time|default:"--" }} {% if r.is_late %}<span class="badge bg-warning text-dark small">Late</span>{% endif %}</td>
            <td>{{ r.check_out_time|default:"--" }}</td>
            <td>{{ r.total_working_hours }} hrs</td>
            <td><span class="ems-badge {% if r.status == 'PRESENT' %}ems-badge-success{% else %}ems-badge-danger{% endif %}">{{ r.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No records for this date.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/attendance/department_summary.html": """{% extends 'base.html' %}
{% block title %}Department Attendance Summary — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-bar-chart-fill text-primary"></i> Department Attendance Rates</h1></div></div>
<div class="row g-4">
    {% for stat in dept_stats %}
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="fw-bold mb-0 text-dark">{{ stat.department.name }}</h6>
                <span class="badge bg-primary">{{ stat.percentage }}% Present</span>
            </div>
            <div class="progress mb-3" style="height: 6px;"><div class="progress-bar bg-primary" style="width: {{ stat.percentage }}%;"></div></div>
            <div class="small text-muted">Total Staff: {{ stat.total }} | Present: {{ stat.present }} | Late: {{ stat.late }}</div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    # ----------------------------------------------------
    # Leave Management Templates
    # ----------------------------------------------------
    "templates/leave_management/my_leaves.html": """{% extends 'base.html' %}
{% block title %}My Leave Portal — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-calendar2-check text-primary"></i> My Leave Portal & Balances</h1></div>
    <a href="{% url 'leave_management:apply_leave' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Apply for Leave</a>
</div>
<div class="row g-3 mb-4">
    {% for bal in balances %}
    <div class="col-12 col-md-4">
        <div class="card p-3 border">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <strong>{{ bal.leave_type.name }}</strong>
                <span class="badge bg-primary fs-6">{{ bal.remaining_days }} Days</span>
            </div>
            <div class="small text-muted">Allocated: {{ bal.total_allocated }} | Used: {{ bal.used_days }} | Pending: {{ bal.pending_days }}</div>
        </div>
    </div>
    {% endfor %}
</div>
<div class="ems-card"><div class="ems-card-header"><h5 class="ems-card-title">Leave History</h5></div>
<div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Leave Type</th><th>Start Date</th><th>End Date</th><th>Days</th><th>Status</th><th>Reviewer Notes</th></tr></thead>
    <tbody>{% for r in requests %}
        <tr>
            <td><strong>{{ r.leave_type.name }}</strong></td>
            <td>{{ r.start_date }}</td>
            <td>{{ r.end_date }}</td>
            <td>{{ r.total_days }}</td>
            <td><span class="ems-badge {% if r.status == 'APPROVED' %}ems-badge-success{% elif r.status == 'REJECTED' %}ems-badge-danger{% else %}ems-badge-warning{% endif %}">{{ r.get_status_display }}</span></td>
            <td>{{ r.rejection_reason|default:"--" }}</td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No leave requests.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/leave_management/apply_leave.html": """{% extends 'base.html' %}
{% block title %}Apply for Leave — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-calendar-plus text-primary"></i> Apply for Leave</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post" enctype="multipart/form-data">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Leave Type *</label>{{ form.leave_type }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Start Date *</label>{{ form.start_date }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">End Date *</label>{{ form.end_date }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Reason for Leave *</label>{{ form.reason }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Supporting Attachment (Optional)</label>{{ form.attachment }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
        <a href="{% url 'leave_management:my_leaves' %}" class="btn btn-outline-secondary">Cancel</a>
        <button type="submit" class="btn btn-primary px-4">Submit Leave Request</button>
    </div>
</form></div></div>
{% endblock %}""",

    "templates/leave_management/approval_list.html": """{% extends 'base.html' %}
{% block title %}Leave Approval Center — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-check2-circle text-primary"></i> Leave Approval Center</h1></div></div>
<div class="ems-card mb-4"><div class="ems-card-header"><h5 class="ems-card-title text-warning"><i class="bi bi-clock-history me-1"></i> Pending Approval Queue</h5></div>
<div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Department</th><th>Leave Type</th><th>Dates</th><th>Days</th><th>Reason</th><th>Actions</th></tr></thead>
    <tbody>{% for r in pending_requests %}
        <tr>
            <td><strong>{{ r.employee.full_name }}</strong></td>
            <td>{{ r.employee.department.name }}</td>
            <td>{{ r.leave_type.name }}</td>
            <td>{{ r.start_date }} to {{ r.end_date }}</td>
            <td>{{ r.total_days }} days</td>
            <td>{{ r.reason|truncatewords:8 }}</td>
            <td>
                <div class="d-flex gap-1">
                    <a href="{% url 'leave_management:approve_leave' r.id %}" class="btn btn-sm btn-success py-0">Approve</a>
                    <form method="post" action="{% url 'leave_management:reject_leave' r.id %}" class="d-inline">{% csrf_token %}
                        <button type="submit" class="btn btn-sm btn-outline-danger py-0">Reject</button>
                    </form>
                </div>
            </td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center text-muted py-4">No pending leave requests in your queue.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/leave_management/calendar.html": """{% extends 'base.html' %}
{% block title %}Leave Calendar — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-calendar3 text-primary"></i> Workforce Leave Calendar</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Leave Type</th><th>Start Date</th><th>End Date</th><th>Duration</th></tr></thead>
    <tbody>{% for l in approved_leaves %}
        <tr>
            <td><strong>{{ l.employee.full_name }}</strong></td>
            <td>{{ l.leave_type.name }}</td>
            <td>{{ l.start_date }}</td>
            <td>{{ l.end_date }}</td>
            <td>{{ l.total_days }} days</td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center text-muted py-4">No scheduled leaves.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Shifts & Holidays Templates
    # ----------------------------------------------------
    "templates/shifts/shift_list.html": """{% extends 'base.html' %}
{% block title %}Shifts & Schedules — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-clock-fill text-primary"></i> Work Shifts & Roster Assignments</h1></div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'shifts:shift_create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Create Shift</a> <a href="{% url 'shifts:shift_assign' %}" class="btn btn-outline-primary btn-sm"><i class="bi bi-person-check me-1"></i>Assign Shift</a>{% endif %}</div>
</div>
<div class="row g-4 mb-4">
    {% for s in shifts %}
    <div class="col-12 col-md-4">
        <div class="ems-card p-3">
            <h5 class="fw-bold mb-1">{{ s.name }}</h5>
            <div class="badge bg-light text-dark border mb-2 font-monospace">{{ s.code }}</div>
            <div class="text-muted small mb-2"><i class="bi bi-clock me-1"></i>{{ s.start_time }} to {{ s.end_time }} (Grace: {{ s.grace_period_minutes }}m)</div>
            <div class="small text-muted">Full Day: {{ s.full_day_hours }}h | Half Day: {{ s.half_day_hours }}h</div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    "templates/shifts/shift_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Shift Name *</label>{{ form.name }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Code *</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Start Time *</label>{{ form.start_time }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">End Time *</label>{{ form.end_time }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Grace Minutes</label>{{ form.grace_period_minutes }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Half Day Hours</label>{{ form.half_day_hours }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Full Day Hours</label>{{ form.full_day_hours }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Save Shift</button></div>
</form></div></div>
{% endblock %}""",

    "templates/shifts/shift_assign_form.html": """{% extends 'base.html' %}
{% block title %}Assign Shift — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Assign Work Shift to Employee</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Employee *</label>{{ form.employee }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Shift *</label>{{ form.shift }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Effective Start Date *</label>{{ form.start_date }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">End Date (Optional)</label>{{ form.end_date }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Save Assignment</button></div>
</form></div></div>
{% endblock %}""",

    "templates/shifts/holiday_list.html": """{% extends 'base.html' %}
{% block title %}Company Holidays — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-calendar-event-fill text-primary"></i> Company Holidays Calendar</h1></div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'shifts:holiday_create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Add Holiday</a>{% endif %}</div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Holiday Name</th><th>Date</th><th>Description</th><th>Department Scope</th></tr></thead>
    <tbody>{% for h in holidays %}
        <tr>
            <td><strong>{{ h.name }}</strong></td>
            <td>{{ h.date }}</td>
            <td>{{ h.description|default:"--" }}</td>
            <td>{{ h.department.name|default:"All Departments" }}</td>
        </tr>
    {% empty %}<tr><td colspan="4" class="text-center text-muted py-4">No holidays configured.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/shifts/holiday_form.html": """{% extends 'base.html' %}
{% block title %}Add Holiday — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Add Company Holiday</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Holiday Name *</label>{{ form.name }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Date *</label>{{ form.date }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Save Holiday</button></div>
</form></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Workload Dashboard
    # ----------------------------------------------------
    "templates/workload/dashboard.html": """{% extends 'base.html' %}
{% block title %}Workload Management — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-pie-chart-fill text-primary"></i> Workforce Workload & Capacity Management</h1>
        <p class="ems-page-subheading">Algorithmic load scoring combining active tasks, priority weights, estimated hours, and deadlines</p>
    </div>
    <div>
        <a href="{% url 'workload:recalculate' %}" class="btn btn-primary btn-sm">
            <i class="bi bi-arrow-repeat me-1"></i>Recalculate All Workloads
        </a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Average Load</div><div class="ems-stat-value text-primary">{{ avg_score }}%</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Overloaded (>85%)</div><div class="ems-stat-value text-danger">{{ overloaded_count }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Balanced / Optimal</div><div class="ems-stat-value text-success">{{ optimal_count }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Underutilized (&lt;35%)</div><div class="ems-stat-value text-info">{{ underutilized_count }}</div></div></div></div>
</div>

<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Department</th><th>Active Tasks</th><th>Allocated Hours</th><th>Overdue</th><th>Workload Score</th><th>Status</th></tr></thead>
    <tbody>{% for m in metrics %}
        <tr>
            <td><strong>{{ m.employee.full_name }}</strong></td>
            <td>{{ m.employee.department.name|default:"--" }}</td>
            <td>{{ m.active_tasks_count }}</td>
            <td>{{ m.estimated_task_hours }} hrs</td>
            <td>{% if m.overdue_tasks_count > 0 %}<span class="badge bg-danger">{{ m.overdue_tasks_count }}</span>{% else %}0{% endif %}</td>
            <td>
                <div class="d-flex align-items-center gap-2">
                    <div class="progress flex-fill" style="height: 6px; width: 80px;">
                        <div class="progress-bar {% if m.workload_score >= 85 %}bg-danger{% elif m.workload_score <= 35 %}bg-info{% else %}bg-primary{% endif %}" style="width: {{ m.workload_score }}%;"></div>
                    </div>
                    <span class="small fw-bold">{{ m.workload_score }}%</span>
                </div>
            </td>
            <td><span class="ems-badge {% if m.utilization_status == 'OVERLOADED' %}ems-badge-danger{% elif m.utilization_status == 'UNDERUTILIZED' %}ems-badge-info{% else %}ems-badge-success{% endif %}">{{ m.get_utilization_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center text-muted py-4">No workload data calculated. Click 'Recalculate All Workloads' above.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Projects & Tasks
    # ----------------------------------------------------
    "templates/projects/project_list.html": """{% extends 'base.html' %}
{% block title %}Project Management — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-kanban-fill text-primary"></i> Projects Directory</h1></div>
    <div>{% if is_manager_or_above %}<a href="{% url 'projects:project_create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>New Project</a>{% endif %}</div>
</div>
<div class="row g-4">
    {% for p in projects %}
    <div class="col-12 col-md-6 col-xl-4">
        <div class="ems-card h-100 p-3">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="badge bg-light text-dark border font-monospace">{{ p.code }}</span>
                <span class="ems-badge ems-badge-success">{{ p.get_status_display }}</span>
            </div>
            <h5 class="fw-bold text-dark mb-1"><a href="{% url 'projects:project_detail' p.id %}" class="text-decoration-none text-dark">{{ p.name }}</a></h5>
            <p class="text-muted small mb-2">{{ p.description|truncatewords:15 }}</p>
            <div class="d-flex justify-content-between align-items-center mb-1 small">
                <span class="text-muted">Progress</span>
                <span class="fw-bold text-primary">{{ p.progress_percentage }}%</span>
            </div>
            <div class="progress mb-3" style="height: 6px;"><div class="progress-bar bg-primary" style="width: {{ p.progress_percentage }}%;"></div></div>
            <div class="border-top pt-2 mt-auto d-flex justify-content-between align-items-center small text-muted">
                <span>Manager: {{ p.manager.full_name|default:"Unassigned" }}</span>
                <a href="{% url 'projects:project_detail' p.id %}" class="btn btn-sm btn-outline-primary py-0">Details</a>
            </div>
        </div>
    </div>
    {% empty %}<div class="col-12 text-center text-muted py-5">No projects created.</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/projects/project_detail.html": """{% extends 'base.html' %}
{% block title %}{{ project.name }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-kanban text-primary"></i> {{ project.name }} ({{ project.code }})</h1>
        <p class="ems-page-subheading">Manager: {{ project.manager.full_name|default:"N/A" }} | Timeline: {{ project.start_date }} to {{ project.end_date|default:"Ongoing" }}</p>
    </div>
</div>
<div class="row g-4">
    <div class="col-12 col-lg-8">
        <div class="ems-card mb-4"><div class="ems-card-header"><h5 class="ems-card-title">Project Tasks ({{ tasks.count }})</h5></div>
        <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
            <thead><tr><th>Code</th><th>Task</th><th>Assignee</th><th>Priority</th><th>Status</th></tr></thead>
            <tbody>{% for t in tasks %}
                <tr>
                    <td><strong>{{ t.code }}</strong></td>
                    <td><a href="{% url 'tasks:task_detail' t.id %}" class="text-decoration-none text-dark">{{ t.title }}</a></td>
                    <td>{{ t.assigned_to.full_name|default:"Unassigned" }}</td>
                    <td><span class="badge bg-secondary">{{ t.get_priority_display }}</span></td>
                    <td><span class="ems-badge ems-badge-success">{{ t.get_status_display }}</span></td>
                </tr>
            {% empty %}<tr><td colspan="5" class="text-center text-muted py-3">No tasks created under this project.</td></tr>{% endfor %}</tbody>
        </table></div></div></div>
    </div>
    <div class="col-12 col-lg-4">
        <div class="ems-card"><div class="ems-card-header"><h5 class="ems-card-title">Project Milestones</h5></div>
        <div class="ems-card-body">
            {% for m in milestones %}
            <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom">
                <div>
                    <div class="fw-bold small">{{ m.title }}</div>
                    <div class="text-muted small">Due: {{ m.due_date }}</div>
                </div>
                <a href="{% url 'projects:toggle_milestone' m.id %}" class="btn btn-sm {% if m.is_completed %}btn-success{% else %}btn-outline-secondary{% endif %} py-0">
                    {% if m.is_completed %}Completed{% else %}Mark Done{% endif %}
                </a>
            </div>
            {% empty %}<p class="text-muted small">No milestones defined.</p>{% endfor %}
            <form method="post" action="{% url 'projects:add_milestone' project.id %}" class="mt-3">{% csrf_token %}
                <div class="mb-2">{{ milestone_form.title }}</div>
                <div class="mb-2">{{ milestone_form.due_date }}</div>
                <button type="submit" class="btn btn-sm btn-primary w-100">Add Milestone</button>
            </form>
        </div></div>
    </div>
</div>
{% endblock %}""",

    "templates/projects/project_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Project Name *</label>{{ form.name }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Project Code *</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Project Manager</label>{{ form.manager }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Project Status</label>{{ form.status }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Start Date *</label>{{ form.start_date }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Target End Date</label>{{ form.end_date }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Project Budget ($)</label>{{ form.budget }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Assigned Team Members</label>{{ form.members }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Project Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Save Project</button></div>
</form></div></div>
{% endblock %}""",

    "templates/tasks/task_list.html": """{% extends 'base.html' %}
{% block title %}Task Management — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-check2-square text-primary"></i> Task Management</h1></div>
    <div>{% if is_manager_or_above %}<a href="{% url 'tasks:task_create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>New Task</a>{% endif %} <a href="{% url 'tasks:my_tasks_kanban' %}" class="btn btn-outline-primary btn-sm"><i class="bi bi-kanban me-1"></i>Kanban</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Code</th><th>Task Title</th><th>Project</th><th>Assignee</th><th>Due Date</th><th>Priority</th><th>Status</th></tr></thead>
    <tbody>{% for t in tasks %}
        <tr>
            <td><strong>{{ t.code }}</strong></td>
            <td><a href="{% url 'tasks:task_detail' t.id %}" class="fw-bold text-decoration-none text-dark">{{ t.title }}</a></td>
            <td>{{ t.project.name }}</td>
            <td>{{ t.assigned_to.full_name|default:"Unassigned" }}</td>
            <td>{{ t.due_date }}</td>
            <td><span class="badge {% if t.priority == 'URGENT' %}bg-danger{% elif t.priority == 'HIGH' %}bg-warning text-dark{% else %}bg-secondary{% endif %}">{{ t.get_priority_display }}</span></td>
            <td><span class="ems-badge {% if t.status == 'COMPLETED' %}ems-badge-success{% else %}ems-badge-warning{% endif %}">{{ t.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center text-muted py-4">No tasks found.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/tasks/kanban.html": """{% extends 'base.html' %}
{% block title %}Task Kanban Board — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-kanban text-primary"></i> Task Kanban Board</h1></div></div>
<div class="row g-3">
    <div class="col-12 col-md-3">
        <div class="p-2 bg-light border rounded"><h6 class="fw-bold p-2 mb-2 border-bottom">To Do ({{ todo_tasks.count }})</h6>
        {% for t in todo_tasks %}
        <div class="ems-card p-2 mb-2 bg-white shadow-sm">
            <div class="small fw-bold">{{ t.title }}</div>
            <div class="text-muted" style="font-size: 0.75rem;">{{ t.project.code }} &bull; Due: {{ t.due_date }}</div>
            <a href="{% url 'tasks:task_detail' t.id %}" class="btn btn-sm btn-link p-0 mt-1" style="font-size: 0.75rem;">View Details</a>
        </div>
        {% endfor %}</div>
    </div>
    <div class="col-12 col-md-3">
        <div class="p-2 bg-light border rounded"><h6 class="fw-bold p-2 mb-2 border-bottom text-primary">In Progress ({{ inprogress_tasks.count }})</h6>
        {% for t in inprogress_tasks %}
        <div class="ems-card p-2 mb-2 bg-white shadow-sm border-primary">
            <div class="small fw-bold">{{ t.title }}</div>
            <div class="text-muted" style="font-size: 0.75rem;">{{ t.project.code }} &bull; Due: {{ t.due_date }}</div>
            <a href="{% url 'tasks:task_detail' t.id %}" class="btn btn-sm btn-link p-0 mt-1" style="font-size: 0.75rem;">View Details</a>
        </div>
        {% endfor %}</div>
    </div>
    <div class="col-12 col-md-3">
        <div class="p-2 bg-light border rounded"><h6 class="fw-bold p-2 mb-2 border-bottom text-warning">In Review ({{ review_tasks.count }})</h6>
        {% for t in review_tasks %}
        <div class="ems-card p-2 mb-2 bg-white shadow-sm">
            <div class="small fw-bold">{{ t.title }}</div>
            <div class="text-muted" style="font-size: 0.75rem;">{{ t.project.code }} &bull; Due: {{ t.due_date }}</div>
            <a href="{% url 'tasks:task_detail' t.id %}" class="btn btn-sm btn-link p-0 mt-1" style="font-size: 0.75rem;">View Details</a>
        </div>
        {% endfor %}</div>
    </div>
    <div class="col-12 col-md-3">
        <div class="p-2 bg-light border rounded"><h6 class="fw-bold p-2 mb-2 border-bottom text-success">Completed ({{ completed_tasks.count }})</h6>
        {% for t in completed_tasks %}
        <div class="ems-card p-2 mb-2 bg-white shadow-sm">
            <div class="small fw-bold text-decoration-line-through text-muted">{{ t.title }}</div>
            <div class="text-muted" style="font-size: 0.75rem;">{{ t.project.code }}</div>
            <a href="{% url 'tasks:task_detail' t.id %}" class="btn btn-sm btn-link p-0 mt-1" style="font-size: 0.75rem;">View Details</a>
        </div>
        {% endfor %}</div>
    </div>
</div>
{% endblock %}""",

    "templates/tasks/task_detail.html": """{% extends 'base.html' %}
{% block title %}{{ task.title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-check2-circle text-primary"></i> [{{ task.code }}] {{ task.title }}</h1>
        <p class="ems-page-subheading">Project: {{ task.project.name }} | Assigned to: {{ task.assigned_to.full_name|default:"Unassigned" }}</p>
    </div>
    <form method="post" action="{% url 'tasks:update_status' task.id %}" class="d-flex gap-2 align-items-center">{% csrf_token %}
        <select name="status" class="form-select form-select-sm" style="width: auto;">
            <option value="TODO" {% if task.status == 'TODO' %}selected{% endif %}>To Do</option>
            <option value="IN_PROGRESS" {% if task.status == 'IN_PROGRESS' %}selected{% endif %}>In Progress</option>
            <option value="REVIEW" {% if task.status == 'REVIEW' %}selected{% endif %}>In Review</option>
            <option value="COMPLETED" {% if task.status == 'COMPLETED' %}selected{% endif %}>Completed</option>
        </select>
        <button type="submit" class="btn btn-sm btn-primary">Update Status</button>
    </form>
</div>
<div class="row g-4">
    <div class="col-12 col-lg-8">
        <div class="ems-card mb-4"><div class="ems-card-header"><h5 class="ems-card-title">Task Description</h5></div>
        <div class="ems-card-body"><p>{{ task.description|default:"No detailed description provided." }}</p></div></div>

        <!-- Comments -->
        <div class="ems-card"><div class="ems-card-header"><h5 class="ems-card-title">Discussion & Updates</h5></div>
        <div class="ems-card-body">
            {% for c in comments %}
            <div class="d-flex gap-2 mb-3 pb-2 border-bottom">
                <div class="ems-user-avatar" style="width: 32px; height: 32px; font-size: 0.8rem;">{{ c.author.initials }}</div>
                <div>
                    <div class="small fw-bold">{{ c.author.full_name }} <span class="text-muted fw-normal">({{ c.created_at }})</span></div>
                    <div class="small text-dark">{{ c.content }}</div>
                </div>
            </div>
            {% endfor %}
            <form method="post" action="{% url 'tasks:add_comment' task.id %}">{% csrf_token %}
                <div class="mb-2">{{ comment_form.content }}</div>
                <button type="submit" class="btn btn-sm btn-primary">Post Comment</button>
            </form>
        </div></div>
    </div>

    <div class="col-12 col-lg-4">
        <div class="ems-card mb-4"><div class="ems-card-header"><h5 class="ems-card-title">Subtasks Checklist</h5></div>
        <div class="ems-card-body">
            {% for s in subtasks %}
            <div class="d-flex justify-content-between align-items-center mb-2 pb-1 border-bottom">
                <span class="small {% if s.is_completed %}text-decoration-line-through text-muted{% endif %}">{{ s.title }}</span>
                <a href="{% url 'tasks:toggle_subtask' s.id %}" class="btn btn-sm btn-outline-secondary py-0">{% if s.is_completed %}Done{% else %}Check{% endif %}</a>
            </div>
            {% endfor %}
            <form method="post" action="{% url 'tasks:add_subtask' task.id %}" class="mt-3">{% csrf_token %}
                <div class="mb-2">{{ subtask_form.title }}</div>
                <button type="submit" class="btn btn-sm btn-outline-primary w-100">Add Subtask</button>
            </form>
        </div></div>
    </div>
</div>
{% endblock %}""",

    "templates/tasks/task_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Task Title *</label>{{ form.title }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Task Code *</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Project *</label>{{ form.project }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Assign To Employee</label>{{ form.assigned_to }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Priority</label>{{ form.priority }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Status</label>{{ form.status }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Start Date</label>{{ form.start_date }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Due Date *</label>{{ form.due_date }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Estimated Hours</label>{{ form.estimated_hours }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Actual Hours</label>{{ form.actual_hours }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Create Task</button></div>
</form></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Skills Management
    # ----------------------------------------------------
    "templates/skills/catalog.html": """{% extends 'base.html' %}
{% block title %}Skill Catalog — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-award-fill text-primary"></i> Company Competency Catalog</h1></div></div>
<div class="row g-4">
    {% for cat in categories %}
    <div class="col-12 col-md-6">
        <div class="ems-card h-100 p-3">
            <h5 class="fw-bold text-primary mb-2">{{ cat.name }}</h5>
            <p class="text-muted small mb-3">{{ cat.description }}</p>
            <div class="d-flex flex-wrap gap-2">
                {% for s in cat.skills.all %}
                <span class="badge bg-light text-dark border p-2">{{ s.name }} ({{ s.code }})</span>
                {% endfor %}
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    "templates/skills/my_skills.html": """{% extends 'base.html' %}
{% block title %}My Skills — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-award text-primary"></i> My Skills & Competency Profile</h1></div></div>
<div class="row g-4">
    <div class="col-12 col-lg-8">
        <div class="ems-card"><div class="ems-card-header"><h5 class="ems-card-title">My Recorded Skills</h5></div>
        <div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
            <thead><tr><th>Skill</th><th>Category</th><th>Proficiency</th><th>Experience</th><th>Verification</th></tr></thead>
            <tbody>{% for s in my_skills %}
                <tr>
                    <td><strong>{{ s.skill.name }}</strong></td>
                    <td>{{ s.skill.category.name }}</td>
                    <td><span class="badge bg-info text-dark">{{ s.get_proficiency_level_display }}</span></td>
                    <td>{{ s.years_of_experience }} yrs</td>
                    <td>{% if s.is_verified %}<span class="badge bg-success">Verified</span>{% else %}<span class="badge bg-secondary">Pending</span>{% endif %}</td>
                </tr>
            {% empty %}<tr><td colspan="5" class="text-center text-muted py-4">No skills recorded.</td></tr>{% endfor %}</tbody>
        </table></div></div></div>
    </div>
    <div class="col-12 col-lg-4">
        <div class="ems-card"><div class="ems-card-header"><h5 class="ems-card-title">Add Skill</h5></div>
        <div class="ems-card-body"><form method="post">{% csrf_token %}
            <div class="mb-3"><label class="form-label small fw-semibold">Skill</label>{{ form.skill }}</div>
            <div class="mb-3"><label class="form-label small fw-semibold">Proficiency</label>{{ form.proficiency_level }}</div>
            <div class="mb-3"><label class="form-label small fw-semibold">Years of Experience</label>{{ form.years_of_experience }}</div>
            <button type="submit" class="btn btn-primary w-100">Add to Profile</button>
        </form></div></div>
    </div>
</div>
{% endblock %}""",

    "templates/skills/matrix.html": """{% extends 'base.html' %}
{% block title %}Skill Matrix Heatmap — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-grid-3x3-gap-fill text-primary"></i> Workforce Skill Matrix Heatmap</h1>
        <p class="ems-page-subheading">Cross-team competency evaluation and proficiency depth</p>
    </div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table table-bordered">
    <thead>
        <tr>
            <th>Employee</th>
            {% for s in skills %}
            <th class="text-center small">{{ s.name }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for row in matrix_rows %}
        <tr>
            <td><strong>{{ row.employee.full_name }}</strong><div class="text-muted" style="font-size: 0.7rem;">{{ row.employee.department.name }}</div></td>
            {% for item in row.skills %}
            <td class="text-center">
                {% if item.proficiency == 'EXPERT' %}<span class="badge bg-success">L4 Expert</span>
                {% elif item.proficiency == 'ADVANCED' %}<span class="badge bg-primary">L3 Adv</span>
                {% elif item.proficiency == 'INTERMEDIATE' %}<span class="badge bg-info text-dark">L2 Mid</span>
                {% elif item.proficiency == 'BEGINNER' %}<span class="badge bg-secondary">L1 Beg</span>
                {% else %}<span class="text-muted">--</span>{% endif %}
            </td>
            {% endfor %}
        </tr>
        {% empty %}<tr><td colspan="15" class="text-center text-muted py-4">No employees in matrix.</td></tr>{% endfor %}
    </tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Goals Management
    # ----------------------------------------------------
    "templates/goals/goal_list.html": """{% extends 'base.html' %}
{% block title %}Goals & OKRs — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-bullseye text-primary"></i> Company & Team OKRs / Goals</h1></div>
    <div>{% if is_manager_or_above %}<a href="{% url 'goals:goal_create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>New Goal</a>{% endif %}</div>
</div>
<div class="row g-4">
    {% for g in goals %}
    <div class="col-12 col-md-6 col-xl-4">
        <div class="ems-card h-100 p-3">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="badge bg-light text-primary border">{% if g.employee %}{{ g.employee.full_name }}{% else %}Team {{ g.team.name }}{% endif %}</span>
                <span class="ems-badge ems-badge-success">{{ g.get_status_display }}</span>
            </div>
            <h5 class="fw-bold text-dark mb-1"><a href="{% url 'goals:goal_detail' g.id %}" class="text-decoration-none text-dark">{{ g.title }}</a></h5>
            <p class="text-muted small mb-2">{{ g.description|truncatewords:10 }}</p>
            <div class="d-flex justify-content-between align-items-center mb-1 small">
                <span class="text-muted">Progress</span>
                <span class="fw-bold text-primary">{{ g.progress_percentage }}%</span>
            </div>
            <div class="progress mb-2" style="height: 6px;"><div class="progress-bar bg-primary" style="width: {{ g.progress_percentage }}%;"></div></div>
            <div class="small text-muted border-top pt-2 mt-auto d-flex justify-content-between">
                <span>Due: {{ g.due_date }}</span>
                <a href="{% url 'goals:goal_detail' g.id %}" class="btn btn-sm btn-outline-primary py-0">Track</a>
            </div>
        </div>
    </div>
    {% empty %}<div class="col-12 text-center text-muted py-5">No goals defined.</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/goals/my_goals.html": """{% extends 'base.html' %}
{% block title %}My Goals — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-bullseye text-primary"></i> My Individual Goals & OKRs</h1></div></div>
<div class="row g-4">
    {% for g in goals %}
    <div class="col-12 col-md-6">
        <div class="ems-card p-3">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <h5 class="fw-bold text-dark mb-0">{{ g.title }}</h5>
                <span class="badge bg-primary">{{ g.progress_percentage }}%</span>
            </div>
            <p class="text-muted small mb-2">{{ g.description }}</p>
            <div class="progress mb-3" style="height: 6px;"><div class="progress-bar bg-primary" style="width: {{ g.progress_percentage }}%;"></div></div>
            <div class="d-flex justify-content-between align-items-center small text-muted">
                <span>Target: {{ g.target_value }} {{ g.unit }} | Due: {{ g.due_date }}</span>
                <a href="{% url 'goals:goal_detail' g.id %}" class="btn btn-sm btn-primary py-0">Update Progress</a>
            </div>
        </div>
    </div>
    {% empty %}<div class="col-12 text-muted py-4">No active goals assigned.</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/goals/goal_detail.html": """{% extends 'base.html' %}
{% block title %}{{ goal.title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ goal.title }}</h1></div></div>
<div class="row g-4">
    <div class="col-12 col-md-7">
        <div class="ems-card p-4">
            <h5 class="fw-bold text-primary mb-3">Goal Details</h5>
            <p>{{ goal.description|default:"No description provided." }}</p>
            <table class="table table-sm border mt-3">
                <tr><th class="bg-light w-40">Target Metric</th><td>{{ goal.target_metric }}</td></tr>
                <tr><th class="bg-light">Target Value</th><td>{{ goal.target_value }} {{ goal.unit }}</td></tr>
                <tr><th class="bg-light">Current Progress</th><td><strong class="text-primary">{{ goal.progress_percentage }}%</strong></td></tr>
                <tr><th class="bg-light">Deadline</th><td>{{ goal.due_date }}</td></tr>
            </table>
        </div>
    </div>
    <div class="col-12 col-md-5">
        <div class="ems-card p-4">
            <h5 class="fw-bold mb-3">Update Progress</h5>
            <form method="post">{% csrf_token %}
                <div class="mb-3"><label class="form-label small fw-semibold">Progress Percentage (0-100) *</label>{{ form.progress_percentage }}</div>
                <div class="mb-3"><label class="form-label small fw-semibold">Current Value</label>{{ form.current_value }}</div>
                <div class="mb-3"><label class="form-label small fw-semibold">Progress Notes</label>{{ form.notes }}</div>
                <button type="submit" class="btn btn-primary w-100">Save Progress</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}""",

    "templates/goals/goal_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12"><label class="form-label small fw-semibold">Goal Title *</label>{{ form.title }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Assigned Employee</label>{{ form.employee }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Assigned Team</label>{{ form.team }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Target Metric</label>{{ form.target_metric }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Target Value</label>{{ form.target_value }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Unit</label>{{ form.unit }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Start Date</label>{{ form.start_date }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Due Date *</label>{{ form.due_date }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Create Goal</button></div>
</form></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Performance Reviews
    # ----------------------------------------------------
    "templates/performance/evaluation_list.html": """{% extends 'base.html' %}
{% block title %}Performance Reviews — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-graph-up text-primary"></i> Performance Reviews & Evaluations</h1></div>
    <div>{% if is_manager_or_above %}<a href="{% url 'performance:conduct' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Conduct Review</a>{% endif %}</div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Department</th><th>Review Cycle</th><th>Evaluator</th><th>Technical</th><th>Comm.</th><th>Productivity</th><th>Leadership</th><th>Score</th></tr></thead>
    <tbody>{% for e in evaluations %}
        <tr>
            <td><strong>{{ e.employee.full_name }}</strong></td>
            <td>{{ e.employee.department.name|default:"--" }}</td>
            <td>{{ e.cycle.title }}</td>
            <td>{{ e.evaluator.full_name|default:"Manager" }}</td>
            <td>{{ e.technical_skills_rating }}</td>
            <td>{{ e.communication_rating }}</td>
            <td>{{ e.productivity_rating }}</td>
            <td>{{ e.leadership_rating }}</td>
            <td><strong class="text-success fs-6">{{ e.final_score }} / 5.0</strong></td>
        </tr>
    {% empty %}<tr><td colspan="9" class="text-center text-muted py-4">No evaluations conducted.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/performance/my_reviews.html": """{% extends 'base.html' %}
{% block title %}My Performance Appraisals — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-graph-up text-primary"></i> My Performance Reviews</h1></div></div>
{% for r in reviews %}
<div class="ems-card p-4 mb-3">
    <div class="d-flex justify-content-between align-items-center">
        <div><h5 class="fw-bold mb-0">{{ r.cycle.title }}</h5><span class="text-muted small">Evaluator: {{ r.evaluator.full_name }}</span></div>
        <div class="fs-3 fw-bold text-success">{{ r.final_score }} / 5.0</div>
    </div>
    <hr>
    <div class="row g-2 small">
        <div class="col-6 col-md-3">Technical Skills: <strong>{{ r.technical_skills_rating }}/5.0</strong></div>
        <div class="col-6 col-md-3">Communication: <strong>{{ r.communication_rating }}/5.0</strong></div>
        <div class="col-6 col-md-3">Productivity: <strong>{{ r.productivity_rating }}/5.0</strong></div>
        <div class="col-6 col-md-3">Leadership: <strong>{{ r.leadership_rating }}/5.0</strong></div>
    </div>
    <div class="mt-3 small"><strong>Manager Strengths Feedback:</strong> {{ r.strengths }}</div>
    <div class="mt-2 small"><strong>Improvement Areas:</strong> {{ r.areas_of_improvement }}</div>
</div>
{% empty %}<div class="text-muted py-4">No reviews recorded.</div>{% endfor %}
{% endblock %}""",

    "templates/performance/evaluation_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Employee *</label>{{ form.employee }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Review Cycle *</label>{{ form.cycle }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Technical Rating (1-5)</label>{{ form.technical_skills_rating }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Communication Rating (1-5)</label>{{ form.communication_rating }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Productivity Rating (1-5)</label>{{ form.productivity_rating }}</div>
        <div class="col-12 col-md-3"><label class="form-label small fw-semibold">Leadership Rating (1-5)</label>{{ form.leadership_rating }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Key Strengths</label>{{ form.strengths }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Areas of Improvement</label>{{ form.areas_of_improvement }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Manager Evaluation Comments</label>{{ form.manager_comments }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Submit Evaluation</button></div>
</form></div></div>
{% endblock %}""",

    "templates/performance/cycle_list.html": """{% extends 'base.html' %}
{% block title %}Review Cycles — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Appraisal Review Cycles</h1></div></div>
<div class="ems-card mb-4"><div class="ems-card-body p-4"><h5 class="fw-bold mb-3">Create Review Cycle</h5>
    <form method="post">{% csrf_token %}<div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small">Title</label>{{ form.title }}</div>
        <div class="col-12 col-md-6"><label class="form-label small">Code</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small">Start Date</label>{{ form.start_date }}</div>
        <div class="col-12 col-md-6"><label class="form-label small">End Date</label>{{ form.end_date }}</div>
    </div><button type="submit" class="btn btn-primary mt-3">Add Cycle</button></form>
</div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Title</th><th>Code</th><th>Dates</th><th>Evaluations Conducted</th></tr></thead>
    <tbody>{% for c in cycles %}
        <tr>
            <td><strong>{{ c.title }}</strong></td>
            <td>{{ c.code }}</td>
            <td>{{ c.start_date }} to {{ c.end_date }}</td>
            <td>{{ c.evaluations.count }} Reviews</td>
        </tr>
    {% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Training & Development
    # ----------------------------------------------------
    "templates/training/catalog.html": """{% extends 'base.html' %}
{% block title %}Training Catalog — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-mortarboard-fill text-primary"></i> Internal Training & Certification Courses</h1></div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'training:create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Add Course</a>{% endif %}</div>
</div>
<div class="row g-4">
    {% for c in courses %}
    <div class="col-12 col-md-6 col-xl-4">
        <div class="ems-card h-100 p-3">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="badge bg-light text-dark border font-monospace">{{ c.code }}</span>
                <span class="badge bg-primary">{{ c.duration_hours }} hrs</span>
            </div>
            <h5 class="fw-bold text-dark mb-1">{{ c.title }}</h5>
            <div class="text-muted small mb-2">{{ c.category.name }} &bull; Provider: {{ c.provider }}</div>
            <p class="text-muted small mb-3">{{ c.description|truncatewords:15 }}</p>
            <div class="border-top pt-2 mt-auto d-flex justify-content-between align-items-center">
                <span class="small text-muted">{{ c.total_enrolled }} Enrolled</span>
                <a href="{% url 'training:enroll' c.id %}" class="btn btn-sm btn-primary">Enroll Now</a>
            </div>
        </div>
    </div>
    {% empty %}<div class="col-12 text-muted py-4">No courses in catalog.</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/training/my_trainings.html": """{% extends 'base.html' %}
{% block title %}My Courses — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-mortarboard text-primary"></i> My Training Enrollments</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Course</th><th>Provider</th><th>Enrolled Date</th><th>Score</th><th>Status</th><th>Certificate Expiry</th></tr></thead>
    <tbody>{% for e in enrollments %}
        <tr>
            <td><strong>{{ e.course.title }}</strong></td>
            <td>{{ e.course.provider }}</td>
            <td>{{ e.enrollment_date }}</td>
            <td>{{ e.score|default:"--" }}%</td>
            <td><span class="ems-badge {% if e.status == 'COMPLETED' %}ems-badge-success{% else %}ems-badge-warning{% endif %}">{{ e.get_status_display }}</span></td>
            <td>{{ e.certificate_expiry_date|default:"N/A" }}</td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No enrollments.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/training/course_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Course Title *</label>{{ form.title }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Code *</label>{{ form.code }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Category</label>{{ form.category }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Provider</label>{{ form.provider }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Duration Hours</label>{{ form.duration_hours }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Pass Score %</label>{{ form.pass_score }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description</label>{{ form.description }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Save Course</button></div>
</form></div></div>
{% endblock %}""",

    "templates/training/expiring_certifications.html": """{% extends 'base.html' %}
{% block title %}Expiring Certifications — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-file-earmark-exclamation text-danger"></i> Expiring Certifications (Next 60 Days)</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Employee</th><th>Department</th><th>Course / Certificate</th><th>Expiration Date</th></tr></thead>
    <tbody>{% for item in expiring %}
        <tr>
            <td><strong>{{ item.employee.full_name }}</strong></td>
            <td>{{ item.employee.department.name }}</td>
            <td>{{ item.course.title }}</td>
            <td><strong class="text-danger">{{ item.certificate_expiry_date }}</strong></td>
        </tr>
    {% empty %}<tr><td colspan="4" class="text-center text-muted py-4">No expiring certifications detected.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Recognition & Feedback
    # ----------------------------------------------------
    "templates/recognition/wall.html": """{% extends 'base.html' %}
{% block title %}Kudos & Recognition Wall — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-trophy-fill text-warning"></i> Employee Recognition & Kudos Wall</h1></div>
    <div><a href="{% url 'recognition:send' %}" class="btn btn-primary btn-sm"><i class="bi bi-heart-fill me-1"></i>Send Kudos</a> <a href="{% url 'recognition:leaderboard' %}" class="btn btn-outline-primary btn-sm"><i class="bi bi-award me-1"></i>Leaderboard</a></div>
</div>
<div class="row g-4">
    {% for r in recognitions %}
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card h-100 p-3 border-start border-4 border-warning">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge bg-warning text-dark"><i class="bi {{ r.category.badge_icon }} me-1"></i>{{ r.category.name }}</span>
                <span class="text-muted small">{{ r.created_at|timesince }} ago</span>
            </div>
            <h5 class="fw-bold text-dark mb-1">{{ r.title }}</h5>
            <p class="text-secondary small mb-3">"{{ r.message }}"</p>
            <div class="border-top pt-2 mt-auto d-flex justify-content-between align-items-center small">
                <span>From: <strong>{{ r.sender.full_name }}</strong></span>
                <span>To: <strong class="text-primary">{{ r.recipient.full_name }}</strong></span>
            </div>
        </div>
    </div>
    {% empty %}<div class="col-12 text-center text-muted py-5">No recognitions yet. Be the first to send Kudos!</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/recognition/send_form.html": """{% extends 'base.html' %}
{% block title %}Send Kudos — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-heart-fill text-danger"></i> Send Colleague Kudos & Recognition</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Recognize Colleague *</label>{{ form.recipient }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Recognition Category *</label>{{ form.category }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Recognition Headline *</label>{{ form.title }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Appreciation Message *</label>{{ form.message }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4"><i class="bi bi-send me-1"></i>Publish Kudos</button></div>
</form></div></div>
{% endblock %}""",

    "templates/recognition/leaderboard.html": """{% extends 'base.html' %}
{% block title %}Recognition Leaderboard — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-award-fill text-warning"></i> Recognition Leaderboard</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Rank</th><th>Employee</th><th>Department</th><th>Kudos Received</th><th>Total Points</th></tr></thead>
    <tbody>{% for emp in top_receivers %}
        <tr>
            <td><strong class="fs-5 text-primary">#{{ forloop.counter }}</strong></td>
            <td><strong>{{ emp.full_name }}</strong></td>
            <td>{{ emp.department.name }}</td>
            <td><span class="badge bg-light text-dark border">{{ emp.total_kudos }} Kudos</span></td>
            <td><strong class="text-warning fs-6">+{{ emp.total_points }} pts</strong></td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center text-muted py-4">No leaderboard data.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Asset Management
    # ----------------------------------------------------
    "templates/assets/asset_list.html": """{% extends 'base.html' %}
{% block title %}Asset Management — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-laptop text-primary"></i> Corporate Asset Inventory</h1></div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'assets:create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Register Asset</a>{% endif %}</div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Asset ID</th><th>Item Name</th><th>Category</th><th>Serial No.</th><th>Assigned To</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>{% for a in assets %}
        <tr>
            <td><span class="badge bg-light text-dark border font-monospace">{{ a.asset_id }}</span></td>
            <td><strong>{{ a.name }}</strong></td>
            <td>{{ a.category.name }}</td>
            <td class="font-monospace small">{{ a.serial_number }}</td>
            <td>{{ a.assigned_to.full_name|default:"Unassigned" }}</td>
            <td><span class="ems-badge {% if a.status == 'ASSIGNED' %}ems-badge-success{% elif a.status == 'AVAILABLE' %}ems-badge-info{% else %}ems-badge-warning{% endif %}">{{ a.get_status_display }}</span></td>
            <td><a href="{% url 'assets:asset_detail' a.id %}" class="btn btn-sm btn-outline-primary py-0">View</a></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center text-muted py-4">No assets in inventory.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/assets/my_assets.html": """{% extends 'base.html' %}
{% block title %}My Assigned Assets — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-laptop text-primary"></i> My Assigned Hardware Assets</h1></div></div>
<div class="row g-4">
    {% for a in assets %}
    <div class="col-12 col-md-6">
        <div class="ems-card p-3">
            <h5 class="fw-bold mb-1">{{ a.name }}</h5>
            <div class="badge bg-light text-dark border font-monospace mb-2">{{ a.asset_id }}</div>
            <div class="small text-muted mb-1">Serial Number: <strong class="font-monospace">{{ a.serial_number }}</strong></div>
            <div class="small text-muted mb-1">Category: {{ a.category.name }}</div>
            <div class="small text-muted">Assigned On: {{ a.assigned_date }}</div>
        </div>
    </div>
    {% empty %}<div class="col-12 text-muted py-4">No equipment assigned.</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/assets/asset_detail.html": """{% extends 'base.html' %}
{% block title %}{{ asset.name }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Asset: {{ asset.name }} ({{ asset.asset_id }})</h1></div></div>
<div class="row g-4">
    <div class="col-12 col-md-7">
        <div class="ems-card p-4">
            <h5 class="fw-bold text-primary mb-3">Asset Metadata</h5>
            <table class="table table-sm border">
                <tr><th class="bg-light w-40">Serial Number</th><td class="font-monospace">{{ asset.serial_number }}</td></tr>
                <tr><th class="bg-light">Category</th><td>{{ asset.category.name }}</td></tr>
                <tr><th class="bg-light">Purchase Cost</th><td>${{ asset.purchase_cost }}</td></tr>
                <tr><th class="bg-light">Purchase Date</th><td>{{ asset.purchase_date }}</td></tr>
                <tr><th class="bg-light">Current Assignee</th><td><strong>{{ asset.assigned_to.full_name|default:"In Central Inventory" }}</strong></td></tr>
            </table>
            {% if is_hr_or_admin and asset.assigned_to %}
            <a href="{% url 'assets:return' asset.id %}" class="btn btn-outline-danger btn-sm mt-2">Return to Inventory</a>
            {% endif %}
        </div>
    </div>
    {% if is_hr_or_admin and not asset.assigned_to %}
    <div class="col-12 col-md-5">
        <div class="ems-card p-4">
            <h5 class="fw-bold mb-3">Assign Asset</h5>
            <form method="post" action="{% url 'assets:assign' asset.id %}">{% csrf_token %}
                <div class="mb-3"><label class="form-label small fw-semibold">Employee</label>{{ assign_form.employee }}</div>
                <div class="mb-3"><label class="form-label small fw-semibold">Notes</label>{{ assign_form.notes }}</div>
                <button type="submit" class="btn btn-primary w-100">Assign Asset</button>
            </form>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}""",

    "templates/assets/asset_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Asset ID *</label>{{ form.asset_id }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Asset Name *</label>{{ form.name }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Category *</label>{{ form.category }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Serial Number *</label>{{ form.serial_number }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Purchase Date *</label>{{ form.purchase_date }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Purchase Cost ($)</label>{{ form.purchase_cost }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Warranty Expiry</label>{{ form.warranty_expiry_date }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Notes</label>{{ form.notes }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Register Asset</button></div>
</form></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Expense Management
    # ----------------------------------------------------
    "templates/expenses/my_expenses.html": """{% extends 'base.html' %}
{% block title %}My Expenses — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-receipt text-primary"></i> My Expense Claims</h1></div>
    <div><a href="{% url 'expenses:claim' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>New Claim</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Claim #</th><th>Title</th><th>Category</th><th>Amount</th><th>Date</th><th>Status</th></tr></thead>
    <tbody>{% for c in claims %}
        <tr>
            <td><span class="badge bg-light text-dark border font-monospace">{{ c.claim_number }}</span></td>
            <td><strong>{{ c.title }}</strong></td>
            <td>{{ c.category.name }}</td>
            <td>${{ c.amount }}</td>
            <td>{{ c.expense_date }}</td>
            <td><span class="ems-badge {% if c.status == 'REIMBURSED' %}ems-badge-success{% elif c.status == 'APPROVED' %}ems-badge-info{% elif c.status == 'REJECTED' %}ems-badge-danger{% else %}ems-badge-warning{% endif %}">{{ c.get_status_display }}</span></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No expense claims submitted.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/expenses/claim_form.html": """{% extends 'base.html' %}
{% block title %}Submit Expense Claim — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-receipt text-primary"></i> Submit Expense Claim</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post" enctype="multipart/form-data">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12"><label class="form-label small fw-semibold">Expense Title *</label>{{ form.title }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Category *</label>{{ form.category }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Amount *</label>{{ form.amount }}</div>
        <div class="col-12 col-md-4"><label class="form-label small fw-semibold">Date Incurred *</label>{{ form.expense_date }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Description / Purpose</label>{{ form.description }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Receipt Upload</label>{{ form.receipt_file }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Submit Claim</button></div>
</form></div></div>
{% endblock %}""",

    "templates/expenses/approvals.html": """{% extends 'base.html' %}
{% block title %}Expense Claims Approval Queue — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-receipt text-primary"></i> Expense Claims Approval Queue</h1></div></div>
<div class="ems-card mb-4"><div class="ems-card-header"><h5 class="ems-card-title text-warning">Pending Claims</h5></div>
<div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Claim #</th><th>Employee</th><th>Category</th><th>Amount</th><th>Date</th><th>Action</th></tr></thead>
    <tbody>{% for c in pending_claims %}
        <tr>
            <td><strong>{{ c.claim_number }}</strong></td>
            <td>{{ c.employee.full_name }}</td>
            <td>{{ c.category.name }}</td>
            <td><strong class="text-success">${{ c.amount }}</strong></td>
            <td>{{ c.expense_date }}</td>
            <td>
                <div class="d-flex gap-1">
                    <a href="{% url 'expenses:approve' c.id %}" class="btn btn-sm btn-success py-0">Approve</a>
                    <a href="{% url 'expenses:reimburse' c.id %}" class="btn btn-sm btn-primary py-0">Reimburse</a>
                </div>
            </td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No pending claims.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Helpdesk / Support
    # ----------------------------------------------------
    "templates/helpdesk/ticket_list.html": """{% extends 'base.html' %}
{% block title %}Helpdesk Support — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-headset text-primary"></i> Helpdesk & Internal Support Queue</h1></div>
    <div><a href="{% url 'helpdesk:create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Create Ticket</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Ticket #</th><th>Subject</th><th>Requester</th><th>Category</th><th>Priority</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>{% for t in tickets %}
        <tr>
            <td><span class="badge bg-light text-dark border font-monospace">{{ t.ticket_number }}</span></td>
            <td><strong>{{ t.subject }}</strong></td>
            <td>{{ t.creator.full_name }}</td>
            <td>{{ t.category.name }}</td>
            <td><span class="badge {% if t.priority == 'URGENT' %}bg-danger{% elif t.priority == 'HIGH' %}bg-warning text-dark{% else %}bg-secondary{% endif %}">{{ t.get_priority_display }}</span></td>
            <td><span class="ems-badge {% if t.status == 'RESOLVED' %}ems-badge-success{% else %}ems-badge-warning{% endif %}">{{ t.get_status_display }}</span></td>
            <td><a href="{% url 'helpdesk:ticket_detail' t.id %}" class="btn btn-sm btn-outline-primary py-0">Open</a></td>
        </tr>
    {% empty %}<tr><td colspan="7" class="text-center text-muted py-4">No support tickets.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/helpdesk/my_tickets.html": """{% extends 'base.html' %}
{% block title %}My Tickets — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-headset text-primary"></i> My Support Requests</h1></div>
    <div><a href="{% url 'helpdesk:create' %}" class="btn btn-primary btn-sm">Create Ticket</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Ticket #</th><th>Subject</th><th>Category</th><th>Status</th><th>Created</th><th>Action</th></tr></thead>
    <tbody>{% for t in tickets %}
        <tr>
            <td><strong>{{ t.ticket_number }}</strong></td>
            <td>{{ t.subject }}</td>
            <td>{{ t.category.name }}</td>
            <td><span class="ems-badge ems-badge-success">{{ t.get_status_display }}</span></td>
            <td>{{ t.created_at|date:'M d, Y' }}</td>
            <td><a href="{% url 'helpdesk:ticket_detail' t.id %}" class="btn btn-sm btn-outline-primary py-0">View</a></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No tickets opened.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/helpdesk/ticket_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post" enctype="multipart/form-data">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Category *</label>{{ form.category }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Priority *</label>{{ form.priority }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Subject *</label>{{ form.subject }}</div>
        <div class="col-12"><label class="form-label small fw-semibold">Issue Details *</label>{{ form.description }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Attachment</label>{{ form.attachment }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Submit Ticket</button></div>
</form></div></div>
{% endblock %}""",

    "templates/helpdesk/ticket_detail.html": """{% extends 'base.html' %}
{% block title %}{{ ticket.subject }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading">[{{ ticket.ticket_number }}] {{ ticket.subject }}</h1><span class="text-muted small">By {{ ticket.creator.full_name }} &bull; Category: {{ ticket.category.name }}</span></div>
    <div><span class="ems-badge ems-badge-success fs-6">{{ ticket.get_status_display }}</span></div>
</div>
<div class="row g-4">
    <div class="col-12 col-lg-8">
        <div class="ems-card mb-4"><div class="ems-card-header"><h5 class="ems-card-title">Issue Description</h5></div>
        <div class="ems-card-body"><p>{{ ticket.description }}</p></div></div>

        <!-- Message Thread -->
        <div class="ems-card"><div class="ems-card-header"><h5 class="ems-card-title">Conversation Thread</h5></div>
        <div class="ems-card-body">
            {% for m in messages_list %}
            <div class="p-3 bg-light rounded mb-3">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <strong>{{ m.sender.full_name }}</strong>
                    <span class="text-muted small">{{ m.created_at }}</span>
                </div>
                <div class="small">{{ m.message }}</div>
            </div>
            {% endfor %}
            <form method="post" action="{% url 'helpdesk:add_message' ticket.id %}">{% csrf_token %}
                <div class="mb-2">{{ message_form.message }}</div>
                <button type="submit" class="btn btn-sm btn-primary">Send Reply</button>
            </form>
        </div></div>
    </div>
    <div class="col-12 col-lg-4">
        {% if ticket.status != 'RESOLVED' %}
        <div class="ems-card"><div class="ems-card-header"><h5 class="ems-card-title">Resolve Ticket</h5></div>
        <div class="ems-card-body"><form method="post" action="{% url 'helpdesk:resolve' ticket.id %}">{% csrf_token %}
            <div class="mb-3">{{ resolve_form.resolution_notes }}</div>
            <button type="submit" class="btn btn-success w-100">Mark as Resolved</button>
        </form></div></div>
        {% else %}
        <div class="ems-card p-3 bg-light"><h6 class="fw-bold text-success">Resolution Documented</h6><p class="small text-muted mb-0">{{ ticket.resolution_notes }}</p></div>
        {% endif %}
    </div>
</div>
{% endblock %}""",

    # ----------------------------------------------------
    # Document Management
    # ----------------------------------------------------
    "templates/documents/library.html": """{% extends 'base.html' %}
{% block title %}Document Repository — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-file-earmark-text text-primary"></i> Company Document Repository</h1></div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'documents:upload' %}" class="btn btn-primary btn-sm"><i class="bi bi-upload me-1"></i>Upload Document</a>{% endif %}</div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Document Title</th><th>Category</th><th>Associated Employee</th><th>Uploaded Date</th><th>Expiry</th><th>Action</th></tr></thead>
    <tbody>{% for d in documents %}
        <tr>
            <td><strong>{{ d.title }}</strong></td>
            <td>{{ d.category.name }}</td>
            <td>{{ d.employee.full_name|default:"Company-Wide" }}</td>
            <td>{{ d.created_at|date:'M d, Y' }}</td>
            <td>{{ d.expiry_date|default:"Permanent" }}</td>
            <td><a href="{{ d.document_file.url }}" class="btn btn-sm btn-outline-primary py-0" download><i class="bi bi-download"></i></a></td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No documents found.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/documents/my_documents.html": """{% extends 'base.html' %}
{% block title %}My Documents — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-file-earmark-text text-primary"></i> My Personal & Compliance Documents</h1></div></div>
<div class="row g-4">
    {% for d in personal_docs %}
    <div class="col-12 col-md-4">
        <div class="ems-card p-3">
            <h5 class="fw-bold mb-1">{{ d.title }}</h5>
            <span class="badge bg-light text-dark border mb-2">{{ d.category.name }}</span>
            <div class="small text-muted mb-3">Uploaded: {{ d.created_at|date:'M d, Y' }}</div>
            <a href="{{ d.document_file.url }}" class="btn btn-sm btn-primary w-100" download><i class="bi bi-download me-1"></i>Download</a>
        </div>
    </div>
    {% empty %}<div class="col-12 text-muted py-4">No personal documents.</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/documents/document_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post" enctype="multipart/form-data">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12"><label class="form-label small fw-semibold">Document Title *</label>{{ form.title }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Category *</label>{{ form.category }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Target Employee</label>{{ form.employee }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Document Reference Number</label>{{ form.document_number }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Expiry Date (Optional)</label>{{ form.expiry_date }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">File Upload *</label>{{ form.document_file }}</div>
        <div class="col-12 col-md-6 form-check mt-4 ms-2">{{ form.is_company_wide }} <label class="form-check-label small fw-semibold">Company-wide policy/handbook</label></div>
        <div class="col-12"><label class="form-label small fw-semibold">Notes</label>{{ form.notes }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Upload Document</button></div>
</form></div></div>
{% endblock %}""",

    "templates/documents/expiring.html": """{% extends 'base.html' %}
{% block title %}Expiring Documents — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-file-earmark-exclamation text-danger"></i> Expiring Compliance Documents (Next 60 Days)</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Document</th><th>Employee</th><th>Category</th><th>Expiry Date</th></tr></thead>
    <tbody>{% for d in expiring %}
        <tr>
            <td><strong>{{ d.title }}</strong></td>
            <td>{{ d.employee.full_name|default:"Company" }}</td>
            <td>{{ d.category.name }}</td>
            <td><strong class="text-danger">{{ d.expiry_date }}</strong></td>
        </tr>
    {% empty %}<tr><td colspan="4" class="text-center text-muted py-4">No expiring documents.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Announcements & Events
    # ----------------------------------------------------
    "templates/announcements/board.html": """{% extends 'base.html' %}
{% block title %}Announcements & Notice Board — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-megaphone-fill text-primary"></i> Company Bulletin & Announcements</h1></div>
    <div>{% if is_hr_or_admin %}<a href="{% url 'announcements:create' %}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Publish Notice</a>{% endif %}</div>
</div>
<div class="row g-4">
    {% for a in announcements %}
    <div class="col-12 col-md-6">
        <div class="ems-card h-100 p-4 {% if a.is_pinned %}border-primary border-2{% endif %}">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge bg-primary-subtle text-primary">{{ a.get_category_display }}</span>
                <span class="text-muted small">{{ a.publish_date }}</span>
            </div>
            <h5 class="fw-bold text-dark mb-2">{% if a.is_pinned %}<i class="bi bi-pin-angle-fill text-danger me-1"></i>{% endif %}{{ a.title }}</h5>
            <p class="text-secondary small mb-3">{{ a.content|linebreaksbr }}</p>
            <div class="text-muted small border-top pt-2 mt-auto">Published by: {{ a.created_by.full_name|default:"Corporate HR" }}</div>
        </div>
    </div>
    {% empty %}<div class="col-12 text-center text-muted py-5">No announcements posted.</div>{% endfor %}
</div>
{% endblock %}""",

    "templates/announcements/announcement_form.html": """{% extends 'base.html' %}
{% block title %}{{ title }} — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">{{ title }}</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12"><label class="form-label small fw-semibold">Notice Title *</label>{{ form.title }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Category *</label>{{ form.category }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Target Department (Optional)</label>{{ form.target_department }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Publish Date *</label>{{ form.publish_date }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Expiry Date</label>{{ form.expiry_date }}</div>
        <div class="col-12 form-check ms-2">{{ form.is_pinned }} <label class="form-check-label small fw-semibold">Pin notice to top of board</label></div>
        <div class="col-12"><label class="form-label small fw-semibold">Bulletin Content *</label>{{ form.content }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Publish Notice</button></div>
</form></div></div>
{% endblock %}""",

    "templates/announcements/events.html": """{% extends 'base.html' %}
{% block title %}Company Events — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-calendar-event text-primary"></i> Company Events & Town Halls</h1></div></div>
<div class="row g-4">
    {% for ev in events %}
    <div class="col-12 col-md-6">
        <div class="ems-card p-4">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <h5 class="fw-bold text-dark mb-0">{{ ev.title }}</h5>
                <span class="badge bg-primary">{{ ev.registrations.count }} Registered</span>
            </div>
            <div class="text-primary small mb-2"><i class="bi bi-calendar me-1"></i>{{ ev.event_date }} &bull; Location: {{ ev.location }}</div>
            <p class="text-muted small mb-3">{{ ev.description }}</p>
            <a href="{% url 'announcements:register_event' ev.id %}" class="btn btn-sm btn-primary">RSVP / Register</a>
        </div>
    </div>
    {% empty %}<div class="col-12 text-muted py-4">No upcoming events.</div>{% endfor %}
</div>
{% endblock %}""",

    # ----------------------------------------------------
    # Notifications Center
    # ----------------------------------------------------
    "templates/notifications/center.html": """{% extends 'base.html' %}
{% block title %}Notification Center — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-bell-fill text-primary"></i> Notification Center</h1></div>
    <div><a href="{% url 'notifications:mark_all_read' %}" class="btn btn-outline-primary btn-sm"><i class="bi bi-check-all me-1"></i>Mark All as Read</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="list-group list-group-flush">
    {% for n in notifications %}
    <div class="list-group-item p-3 {% if not n.is_read %}bg-light{% endif %}">
        <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center gap-2">
                {% if not n.is_read %}<span class="badge bg-primary rounded-pill">&nbsp;</span>{% endif %}
                <strong class="text-dark">{{ n.title }}</strong>
                <span class="badge bg-light text-dark border small font-monospace">{{ n.category }}</span>
            </div>
            <span class="text-muted small">{{ n.created_at|timesince }} ago</span>
        </div>
        <p class="text-secondary small mb-1 mt-1">{{ n.message }}</p>
        {% if n.link %}
        <a href="{% url 'notifications:mark_read' n.id %}" class="small text-primary text-decoration-none">Open Linked Module &rarr;</a>
        {% endif %}
    </div>
    {% empty %}<div class="text-center text-muted py-5">No notifications.</div>{% endfor %}
</div></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Smart Insights Dashboard
    # ----------------------------------------------------
    "templates/insights/dashboard.html": """{% extends 'base.html' %}
{% block title %}Smart Insights Engine — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-cpu-fill text-info"></i> Local Smart Insights Intelligence Hub</h1>
        <p class="ems-page-subheading">100% local mathematical, statistical, and ML workforce analysis — Zero external AI APIs</p>
    </div>
    <div>
        <a href="{% url 'insights:trigger_analysis' %}" class="btn btn-primary btn-sm">
            <i class="bi bi-play-fill me-1"></i>Run Local Intelligence Engine
        </a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Total Signals Detected</div><div class="ems-stat-value text-dark">{{ total_count }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">High Priority / Critical</div><div class="ems-stat-value text-danger">{{ high_priority }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Medium Priority</div><div class="ems-stat-value text-warning">{{ medium_priority }}</div></div></div></div>
    <div class="col-6 col-md-3"><div class="ems-stat-card"><div class="ems-stat-content"><div class="ems-stat-label">Positive Achievements</div><div class="ems-stat-value text-success">{{ positive_trends }}</div></div></div></div>
</div>

<div class="row g-4">
    {% for ins in insights %}
    <div class="col-12 col-lg-6">
        <div class="ems-insight-card {% if ins.severity == 'HIGH' %}high-priority{% elif ins.severity == 'POSITIVE' %}positive{% else %}medium-priority{% endif %} h-100">
            <div class="ems-insight-title mb-2">
                <span>{{ ins.title }}</span>
                <span class="badge {% if ins.severity == 'HIGH' %}bg-danger{% elif ins.severity == 'POSITIVE' %}bg-success{% else %}bg-warning text-dark{% endif %}">
                    {{ ins.get_severity_display }}
                </span>
            </div>
            <div class="small text-muted mb-2">
                <strong>Target:</strong> {{ ins.employee.full_name|default:ins.department.name|default:"System-Wide" }} &bull;
                <strong>Category:</strong> {{ ins.get_category_display }} &bull;
                <strong>Confidence:</strong> {{ ins.confidence_score }}
            </div>
            <div class="small text-dark mb-2"><strong>What Detected:</strong> {{ ins.what_detected }}</div>
            <div class="ems-insight-reason mb-3"><strong>Why Detected (Explainable):</strong> {{ ins.why_detected }}</div>
            <div class="ems-insight-recommendation">
                <i class="bi bi-lightbulb-fill me-1 text-primary"></i> <strong>Recommendation:</strong> {{ ins.recommendation }}
            </div>
            <div class="d-flex justify-content-end mt-2">
                <a href="{% url 'insights:dismiss' ins.id %}" class="btn btn-sm btn-link text-muted p-0" style="font-size: 0.75rem;">Dismiss</a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center text-muted py-5">
        <h5>No active insights generated.</h5>
        <p class="small">Click "Run Local Intelligence Engine" above to trigger mathematical, statistical, and ML analysis across the system.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}""",

    # ----------------------------------------------------
    # Reports & Analytics
    # ----------------------------------------------------
    "templates/reports/hub.html": """{% extends 'base.html' %}
{% block title %}Reports & Analytics Hub — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-file-earmark-bar-graph-fill text-primary"></i> Reports & Analytics Center</h1>
        <p class="ems-page-subheading">Access the 7 mandatory business output streams, chart analytics, and export tools</p>
    </div>
</div>
<div class="row g-4">
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-primary"><i class="bi bi-person-badge me-2"></i>1. Employee 360° View</h5>
            <p class="text-muted small">Complete unified pane of personal details, attendance, reviews, tasks, assets, and skills.</p>
            <a href="{% url 'employees:employee_list' %}" class="btn btn-sm btn-outline-primary">Open Roster & 360°</a>
        </div>
    </div>
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-primary"><i class="bi bi-clock-history me-2"></i>2. Attendance & Leave Reports</h5>
            <p class="text-muted small">Workforce presence ratios, tardiness clustering, leave balances, and department breakdowns.</p>
            <a href="{% url 'reports:attendance_leave' %}" class="btn btn-sm btn-outline-primary">View Report</a>
        </div>
    </div>
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-primary"><i class="bi bi-graph-up me-2"></i>3. Performance Analytics</h5>
            <p class="text-muted small">Multi-cycle appraisal rating distributions, skill radar charts, and regression trends.</p>
            <a href="{% url 'reports:performance_analytics' %}" class="btn btn-sm btn-outline-primary">View Analytics</a>
        </div>
    </div>
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-primary"><i class="bi bi-kanban me-2"></i>4. Project & Task Tracking</h5>
            <p class="text-muted small">Project progress burndown, milestone completion velocities, and overdue task monitoring.</p>
            <a href="{% url 'reports:project_task_tracking' %}" class="btn btn-sm btn-outline-primary">Track Projects</a>
        </div>
    </div>
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-primary"><i class="bi bi-mortarboard me-2"></i>5. Skill & Training Insights</h5>
            <p class="text-muted small">Competency matrices, training enrollments, compliance ratios, and skill gap staffing.</p>
            <a href="{% url 'reports:skills_training' %}" class="btn btn-sm btn-outline-primary">View Insights</a>
        </div>
    </div>
    <div class="col-12 col-md-6 col-lg-4">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-primary"><i class="bi bi-receipt me-2"></i>6. Expense & Asset Tracking</h5>
            <p class="text-muted small">Hardware allocation tracking, lifecycle deprecation, and departmental reimbursement burn.</p>
            <a href="{% url 'reports:expense_assets' %}" class="btn btn-sm btn-outline-primary">Track Expenses</a>
        </div>
    </div>
</div>
{% endblock %}""",

    "templates/reports/attendance_leave_report.html": """{% extends 'base.html' %}
{% block title %}Attendance & Leave Reports — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Attendance & Leave Reports</h1></div></div>
<div class="row g-4 mb-4">
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Attendance Breakdown</h5><div style="height: 250px;"><canvas id="attPieChart"></canvas></div></div></div>
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Summary Metrics</h5>
        <table class="table table-sm border mt-3">
            <tr><th>Present Days Logged</th><td>{{ data.attendance_breakdown.present }}</td></tr>
            <tr><th>Late Arrivals</th><td>{{ data.attendance_breakdown.late }}</td></tr>
            <tr><th>Approved Leaves</th><td>{{ data.leave_breakdown.approved }}</td></tr>
            <tr><th>Pending Leave Requests</th><td>{{ data.leave_breakdown.pending }}</td></tr>
        </table>
    </div></div>
</div>
{% endblock %}
{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    renderEMSChart('attPieChart', 'pie', {
        labels: {{ data.chart_labels|safe }},
        datasets: [{
            data: {{ data.chart_data|safe }},
            backgroundColor: ['#10b981', '#ef4444', '#f59e0b', '#0284c7']
        }]
    });
});
</script>
{% endblock %}""",

    "templates/reports/performance_analytics.html": """{% extends 'base.html' %}
{% block title %}Performance Analytics — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Performance Analytics & Rating Distribution</h1></div></div>
<div class="row g-4">
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Score Distribution</h5><div style="height: 250px;"><canvas id="perfDistChart"></canvas></div></div></div>
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Competency Radar</h5><div style="height: 250px;"><canvas id="perfRadarChart"></canvas></div></div></div>
</div>
{% endblock %}
{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    renderEMSChart('perfDistChart', 'bar', {
        labels: {{ data.dist_labels|safe }},
        datasets: [{
            label: 'Employees in Bracket',
            data: {{ data.dist_data|safe }},
            backgroundColor: '#1e3a8a'
        }]
    });
    renderEMSChart('perfRadarChart', 'radar', {
        labels: {{ data.radar_labels|safe }},
        datasets: [{
            label: 'Company Average Score (out of 5.0)',
            data: {{ data.radar_data|safe }},
            backgroundColor: 'rgba(30, 58, 138, 0.2)',
            borderColor: '#1e3a8a',
            pointBackgroundColor: '#1e3a8a'
        }]
    });
});
</script>
{% endblock %}""",

    "templates/reports/project_task_tracking.html": """{% extends 'base.html' %}
{% block title %}Project & Task Tracking — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Project & Task Tracking Analytics</h1></div></div>
<div class="row g-4 mb-4">
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Tasks by Status</h5><div style="height: 240px;"><canvas id="taskStatusChart"></canvas></div></div></div>
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Tasks by Priority</h5><div style="height: 240px;"><canvas id="taskPriorityChart"></canvas></div></div></div>
</div>
{% endblock %}
{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    renderEMSChart('taskStatusChart', 'doughnut', {
        labels: {{ status_labels_json|safe }},
        datasets: [{
            data: {{ status_data_json|safe }},
            backgroundColor: ['#64748b', '#0284c7', '#f59e0b', '#10b981']
        }]
    });
    renderEMSChart('taskPriorityChart', 'bar', {
        labels: {{ priority_labels_json|safe }},
        datasets: [{
            label: 'Tasks Count',
            data: {{ priority_data_json|safe }},
            backgroundColor: ['#ef4444', '#f97316', '#3b82f6', '#94a3b8']
        }]
    });
});
</script>
{% endblock %}""",

    "templates/reports/skill_training_insights.html": """{% extends 'base.html' %}
{% block title %}Skill & Training Insights — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Skill & Training Insights</h1></div></div>
<div class="row g-4">
    <div class="col-12 col-md-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Training Completion Status</h5>
        <div class="p-3 bg-light rounded text-center mb-3"><div class="fs-2 fw-bold text-success">{{ completed_enrollments }}</div><div class="small text-muted">Completed Certifications</div></div>
        <div class="p-3 bg-light rounded text-center"><div class="fs-2 fw-bold text-primary">{{ active_enrollments }}</div><div class="small text-muted">Active In-Flight Courses</div></div>
    </div></div>
    <div class="col-12 col-md-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Top Company Competencies</h5>
        <ul class="list-group list-group-flush">
            {% for s in skills|slice:":5" %}
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>{{ s.name }} ({{ s.category.name }})</span>
                <span class="badge bg-primary">{{ s.employee_skills.count }} Staff</span>
            </li>
            {% endfor %}
        </ul>
    </div></div>
</div>
{% endblock %}""",

    "templates/reports/expense_asset_tracking.html": """{% extends 'base.html' %}
{% block title %}Expense & Asset Tracking — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading">Expense & Asset Tracking</h1></div></div>
<div class="row g-4">
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Asset Allocation States</h5><div style="height: 240px;"><canvas id="assetChart"></canvas></div></div></div>
    <div class="col-12 col-lg-6"><div class="ems-card p-3"><h5 class="fw-bold mb-3">Expense Claim Lifecycle</h5><div style="height: 240px;"><canvas id="expChart"></canvas></div></div></div>
</div>
{% endblock %}
{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    renderEMSChart('assetChart', 'doughnut', {
        labels: {{ asset_labels_json|safe }},
        datasets: [{
            data: {{ asset_data_json|safe }},
            backgroundColor: ['#0284c7', '#10b981', '#f59e0b', '#64748b']
        }]
    });
    renderEMSChart('expChart', 'doughnut', {
        labels: {{ expense_labels_json|safe }},
        datasets: [{
            data: {{ expense_data_json|safe }},
            backgroundColor: ['#f59e0b', '#0284c7', '#10b981', '#ef4444']
        }]
    });
});
</script>
{% endblock %}""",

    # ----------------------------------------------------
    # Administration & Compliance
    # ----------------------------------------------------
    "templates/administration/audit_logs.html": """{% extends 'base.html' %}
{% block title %}Audit Logs & Activity Trails — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-journal-text text-primary"></i> System Audit Logs & Activity Trails</h1></div>
    <div><a href="{% url 'administration:export_audit_logs' %}" class="btn btn-outline-secondary btn-sm"><i class="bi bi-download me-1"></i>Export Logs</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Timestamp</th><th>User</th><th>Action</th><th>Module</th><th>IP Address</th><th>Description</th></tr></thead>
    <tbody>{% for l in logs %}
        <tr>
            <td class="text-muted small">{{ l.timestamp|date:'Y-m-d H:i:s' }}</td>
            <td><strong>{{ l.username|default:"System" }}</strong></td>
            <td><span class="badge {% if l.action == 'CREATE' %}bg-success{% elif l.action == 'DELETE' %}bg-danger{% elif l.action == 'APPROVE' %}bg-primary{% else %}bg-secondary{% endif %}">{{ l.action }}</span></td>
            <td><span class="font-monospace small">{{ l.module }}</span></td>
            <td class="font-monospace small text-muted">{{ l.ip_address|default:"127.0.0.1" }}</td>
            <td class="small">{{ l.description }}</td>
        </tr>
    {% empty %}<tr><td colspan="6" class="text-center text-muted py-4">No audit logs recorded.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/administration/security_compliance.html": """{% extends 'base.html' %}
{% block title %}Security & Compliance — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div>
        <h1 class="ems-page-heading"><i class="bi bi-shield-check text-success"></i> Security & Compliance Center</h1>
        <p class="ems-page-subheading">Enterprise governance, RBAC enforcement, data protection, and disaster recovery</p>
    </div>
</div>

<div class="row g-4 mb-4">
    <!-- 1. RBAC -->
    <div class="col-12 col-md-6">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-primary mb-2"><i class="bi bi-shield-lock me-2"></i>1. Role-Based Access Control (RBAC)</h5>
            <p class="text-muted small">Granular permission matrix enforced on every view and database operation.</p>
            <div class="d-flex gap-2">
                <span class="badge bg-primary fs-6">{{ roles_count }} Active Roles</span>
                <span class="badge bg-light text-dark border fs-6">{{ permissions_count }} Module Rules</span>
            </div>
            <div class="mt-3"><a href="{% url 'permissions:role_list' %}" class="btn btn-sm btn-outline-primary">Manage Permissions</a></div>
        </div>
    </div>

    <!-- 2. Data Protection -->
    <div class="col-12 col-md-6">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-success mb-2"><i class="bi bi-lock-fill me-2"></i>2. Data Protection & Encryption</h5>
            <p class="text-muted small">Passwords hashed with PBKDF2/Argon2. CSRF tokens enforced on all POST forms. Local secure file validation.</p>
            <span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>Compliant</span>
        </div>
    </div>

    <!-- 3. Audit Logging -->
    <div class="col-12 col-md-6">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-info mb-2"><i class="bi bi-journal-check me-2"></i>3. Immutable Audit Logging</h5>
            <p class="text-muted small">Automatic tracking of user actions, timestamps, and IP addresses for full non-repudiation.</p>
            <a href="{% url 'administration:audit_logs' %}" class="btn btn-sm btn-outline-info">View Logs</a>
        </div>
    </div>

    <!-- 4. Backup & Disaster Recovery -->
    <div class="col-12 col-md-6">
        <div class="ems-card h-100 p-4">
            <h5 class="fw-bold text-warning mb-2"><i class="bi bi-database-check me-2"></i>4. Backup & Disaster Recovery</h5>
            <p class="text-muted small">Automated database snapshot configuration and storage retention rules.</p>
            <span class="badge bg-light text-dark border mb-2 font-monospace">{{ backup_config.status|default:"HEALTHY" }}</span>
            <div><a href="{% url 'administration:backups' %}" class="btn btn-sm btn-outline-warning text-dark">Backup Dashboard</a></div>
        </div>
    </div>
</div>
{% endblock %}""",

    "templates/administration/system_settings.html": """{% extends 'base.html' %}
{% block title %}System Settings — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-sliders text-primary"></i> System Configuration & Parameters</h1></div></div>
<div class="ems-card mb-4"><div class="ems-card-body p-4"><h5 class="fw-bold mb-3">Add / Update Setting</h5>
    <form method="post">{% csrf_token %}<div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small">Key *</label>{{ form.key }}</div>
        <div class="col-12 col-md-6"><label class="form-label small">Value *</label>{{ form.value }}</div>
        <div class="col-12 col-md-6"><label class="form-label small">Category</label>{{ form.category }}</div>
        <div class="col-12 col-md-6"><label class="form-label small">Description</label>{{ form.description }}</div>
    </div><button type="submit" class="btn btn-primary mt-3">Save Setting</button></form>
</div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Key</th><th>Value</th><th>Category</th><th>Description</th></tr></thead>
    <tbody>{% for s in settings %}
        <tr>
            <td><span class="badge bg-light text-dark border font-monospace">{{ s.key }}</span></td>
            <td><strong>{{ s.value }}</strong></td>
            <td>{{ s.get_category_display }}</td>
            <td class="small text-muted">{{ s.description }}</td>
        </tr>
    {% empty %}<tr><td colspan="4" class="text-center text-muted py-4">No custom settings configured.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/administration/backups.html": """{% extends 'base.html' %}
{% block title %}Backup & Recovery — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-database-check text-primary"></i> Database Backup & Recovery</h1></div>
    <div><a href="{% url 'administration:trigger_backup' %}" class="btn btn-primary btn-sm"><i class="bi bi-hdd-stack me-1"></i>Execute Manual Snapshot</a></div>
</div>
<div class="ems-card"><div class="ems-card-body p-4"><form method="post">{% csrf_token %}
    <div class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Backup Strategy</label>{{ form.backup_type }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Frequency</label>{{ form.frequency }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Storage Location</label>{{ form.storage_location }}</div>
        <div class="col-12 col-md-6"><label class="form-label small fw-semibold">Retention Days</label>{{ form.retention_days }}</div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4"><button type="submit" class="btn btn-primary px-4">Update Configuration</button></div>
</form></div></div>
{% endblock %}""",

    # ----------------------------------------------------
    # Additional Authentication Views
    # ----------------------------------------------------
    "templates/authentication/change_password.html": """{% extends 'base.html' %}
{% block title %}Change Password — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-key-fill text-primary"></i> Change Account Password</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-4" style="max-width: 600px;"><form method="post">{% csrf_token %}
    <div class="mb-3"><label class="form-label small fw-semibold">Current Password *</label>{{ form.old_password }}</div>
    <div class="mb-3"><label class="form-label small fw-semibold">New Password *</label>{{ form.new_password }}</div>
    <div class="mb-3"><label class="form-label small fw-semibold">Confirm New Password *</label>{{ form.confirm_password }}</div>
    <button type="submit" class="btn btn-primary px-4">Update Password</button>
</form></div></div>
{% endblock %}""",

    "templates/authentication/user_list.html": """{% extends 'base.html' %}
{% block title %}User Accounts — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header">
    <div><h1 class="ems-page-heading"><i class="bi bi-person-gear text-primary"></i> User Access & Authentication Accounts</h1></div>
</div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Username</th><th>Email</th><th>Role</th><th>Status</th><th>Failed Logins</th><th>Action</th></tr></thead>
    <tbody>{% for u in users %}
        <tr>
            <td><strong>{{ u.username }}</strong></td>
            <td>{{ u.email }}</td>
            <td><span class="badge bg-light text-dark border">{{ u.get_role_display }}</span></td>
            <td><span class="ems-badge {% if u.is_active %}ems-badge-success{% else %}ems-badge-danger{% endif %}">{% if u.is_active %}Active{% else %}Deactivated{% endif %}</span></td>
            <td>{{ u.failed_login_attempts }}</td>
            <td>
                {% if u != user %}
                <a href="{% url 'authentication:user_toggle_status' u.id %}" class="btn btn-sm {% if u.is_active %}btn-outline-danger{% else %}btn-outline-success{% endif %} py-0">
                    {% if u.is_active %}Deactivate{% else %}Activate{% endif %}
                </a>
                {% endif %}
            </td>
        </tr>
    {% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/authentication/login_history.html": """{% extends 'base.html' %}
{% block title %}Login History — Smart Employee Management System{% endblock %}
{% block content %}
<div class="ems-page-header"><div><h1 class="ems-page-heading"><i class="bi bi-clock-history text-primary"></i> Login History & Session Logs</h1></div></div>
<div class="ems-card"><div class="ems-card-body p-0"><div class="table-responsive"><table class="ems-table">
    <thead><tr><th>Timestamp</th><th>Username Attempted</th><th>Status</th><th>IP Address</th><th>Failure Reason</th></tr></thead>
    <tbody>{% for h in history %}
        <tr>
            <td>{{ h.timestamp|date:'Y-m-d H:i:s' }}</td>
            <td><strong>{{ h.username_attempted }}</strong></td>
            <td><span class="badge {% if h.status == 'SUCCESS' %}bg-success{% else %}bg-danger{% endif %}">{{ h.status }}</span></td>
            <td class="font-monospace small">{{ h.ip_address }}</td>
            <td class="small text-muted">{{ h.failure_reason|default:"--" }}</td>
        </tr>
    {% empty %}<tr><td colspan="5" class="text-center text-muted py-4">No login logs.</td></tr>{% endfor %}</tbody>
</table></div></div></div>
{% endblock %}""",

    "templates/authentication/password_reset_request.html": """{% extends 'base.html' %}
{% block auth_content %}
<div class="container"><div class="row justify-content-center"><div class="col-12 col-md-6 col-lg-4">
    <div class="card p-4 shadow-sm border-0 rounded-4">
        <h4 class="fw-bold mb-2">Reset Password</h4>
        <p class="text-muted small mb-4">Enter your corporate email address to receive password reset instructions.</p>
        <form method="post">{% csrf_token %}
            <div class="mb-3">{{ form.email }}</div>
            <button type="submit" class="btn btn-primary w-100 py-2">Send Reset Link</button>
            <div class="text-center mt-3"><a href="{% url 'authentication:login' %}" class="small text-decoration-none">&larr; Back to Login</a></div>
        </form>
    </div>
</div></div></div>
{% endblock %}""",

    "templates/authentication/password_reset_done.html": """{% extends 'base.html' %}
{% block auth_content %}
<div class="container"><div class="row justify-content-center"><div class="col-12 col-md-6 col-lg-5">
    <div class="card p-4 shadow-sm border-0 rounded-4 text-center">
        <div class="text-success fs-1 mb-2"><i class="bi bi-check-circle-fill"></i></div>
        <h4 class="fw-bold mb-2">Reset Link Generated</h4>
        <p class="text-muted small">In production, this link is emailed securely. In this local environment, you can access the reset link below:</p>
        <div class="p-3 bg-light rounded text-break font-monospace small mb-3 border">{{ reset_url }}</div>
        <a href="{{ reset_url }}" class="btn btn-primary py-2">Proceed to Set New Password</a>
    </div>
</div></div></div>
{% endblock %}""",

    "templates/authentication/password_reset_confirm.html": """{% extends 'base.html' %}
{% block auth_content %}
<div class="container"><div class="row justify-content-center"><div class="col-12 col-md-6 col-lg-4">
    <div class="card p-4 shadow-sm border-0 rounded-4">
        <h4 class="fw-bold mb-2">Set New Password</h4>
        <form method="post">{% csrf_token %}
            <div class="mb-3"><label class="form-label small fw-semibold">New Password</label>{{ form.new_password }}</div>
            <div class="mb-3"><label class="form-label small fw-semibold">Confirm Password</label>{{ form.confirm_password }}</div>
            <button type="submit" class="btn btn-primary w-100 py-2">Reset Password</button>
        </form>
    </div>
</div></div></div>
{% endblock %}""",
}

for filepath, content in TEMPLATE_FILES.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filepath}")

print("All templates successfully created!")
