import os

DOCS_DIR = "documentation"
os.makedirs(DOCS_DIR, exist_ok=True)

CHAPTERS = {
    "01_executive_summary.md": """# Chapter 1: Executive Summary & System Overview

## 1.1 Executive Summary
The **Smart Employee Management System (Smart EMS)** is an enterprise-grade, human-crafted human resource and workforce management platform. Designed specifically for modern, data-driven organizations, Smart EMS bridges the gap between administrative operational workflows and predictive workforce intelligence.

## 1.2 Mission & Design Principles
- **Autonomous & Privacy-Preserving**: 100% self-contained Python architecture. Zero external cloud API calls, zero third-party AI dependencies, and complete data privacy.
- **Enterprise-Grade Rigor**: Complete implementation of all 24 modular subsystems across 6 functional pillars.
- **Dynamic Human-Centered Design**: Built with modern UI aesthetics—glassmorphism, subtle micro-interactions, dark/light contrast, and high-density information architecture.
- **Predictive Local Intelligence**: Embedded machine learning, statistical variance analyzers, and z-score anomaly detectors operating directly on Django querysets.

## 1.3 System Pillars
```
+---------------------------------------------------------------------------------------------------+
|                                 SMART EMPLOYEE MANAGEMENT SYSTEM                                   |
+-------------------+--------------------+--------------------+--------------------+----------------+
| Core & Security   | Time & Workforce   | Work & Productivity| Employee Dev       | Services & ML  |
| - Authentication  | - Attendance (GPS) | - Projects & Milest| - Performance 9-Box| - Assets       |
| - Roles & RBAC    | - Leave Lifecycle  | - Kanban Tasks     | - Training & Certs | - Expenses     |
| - Organization    | - Shifts & Roster  | - Skill Heatmaps   | - Kudos & Gamify   | - Helpdesk SLA |
| - Employee 360    | - Workload Scoring | - OKRs & Goals     |                    | - Smart Insights|
+-------------------+--------------------+--------------------+--------------------+----------------+
```
""",

    "02_system_architecture.md": """# Chapter 2: System Architecture & High-Level Design

## 2.1 Technology Stack
- **Backend Framework**: Python 3.12+ / Django 5.x / 6.x
- **Data Persistence**: Relational SQLite / PostgreSQL with ACID compliance
- **Machine Learning & Analytics**: NumPy, Pandas, Scikit-learn, SciPy
- **Presentation Layer**: Django Server-Side Templates, Vanilla CSS Design System, Bootstrap Icons, Chart.js
- **Testing & Quality Assurance**: Pytest, Pytest-Django

## 2.2 Architectural Layers
1. **Presentation Layer**: HTML5 Semantic templates, responsive CSS Grid/Flexbox design tokens, interactive Chart.js visualizations.
2. **Controller / Routing Layer**: Django class-based and functional views protected by RBAC matrix decorators (`@require_permission`).
3. **Domain & Business Logic Layer**: Service classes (`Employee360Service`, `AttendanceService`, `LeaveService`, `WorkloadCalculationService`, `SmartInsightService`).
4. **Local Intelligence Layer**: 9 specialized local ML/statistical engines (`AnomalyDetector`, `AttendanceAnalyzer`, `WorkloadAnalyzer`, `SkillAnalyzer`, etc.).
5. **Data Layer**: 24 Django app models with foreign keys, index optimizations, constraints, and audit logging.
""",

    "03_24_module_specification.md": """# Chapter 3: Complete 24-Module Specification & Features

The system implements the exact 24 modules across 6 functional groups without exception:

### Group 1: Core & Security
1. **Authentication**: Custom User model, session management, failed login lockout, password reset tokens, security logs.
2. **Employee Management**: Master records, personal info, education, work experience, banking, reporting manager hierarchy.
3. **Organization Management**: Enterprise profiles, departments, teams, designations, organizational tree hierarchy.
4. **Roles & Permissions**: RBAC matrix, granular permission codes (VIEW, ADD, EDIT, DELETE, APPROVE, EXPORT, ADMIN) across 24 modules.

### Group 2: Time & Workforce
5. **Attendance Management**: Check-in/out, shift grace minutes, late tracking, IP recording, overtime calculation.
6. **Leave Management**: Leave types, annual quotas, pending/used balances, multi-day approval workflow.
7. **Shift & Holiday Management**: Work shifts, roster assignments, rotational patterns, company holiday calendar.
8. **Workload Management**: Algorithmic workload indexing (0-100), capacity utilization statuses, overload alerts.

### Group 3: Work & Productivity
9. **Project Management**: Project milestones, client tracking, financial budgets, automatic progress rollups.
10. **Task Management**: Kanban task board, subtasks, priority weights, time tracking, discussion threads.
11. **Skills Management**: Skill catalog, proficiency levels (1-5), verified endorsements, team skill matrix heatmap.
12. **Goals Management**: Strategic OKRs, target metrics, velocity tracking, milestone check-ins.

### Group 4: Employee Development
13. **Performance Management**: Appraisal cycles, multi-criteria rubric evaluation, 9-box talent matrix.
14. **Training & Development**: Course catalog, employee enrollments, pass scores, certification expiration monitoring.
15. **Recognition & Feedback**: Peer-to-peer kudos wall, gamified badge categories, points leaderboard.

### Group 5: Employee Services
16. **Asset Management**: Hardware inventory, serial number tracking, assignment histories, warranty monitoring.
17. **Expense Management**: Multi-currency expense claims, receipt attachments, multi-tier approval workflows.
18. **Helpdesk / Support**: Support ticket lifecycle, SLA resolution tracking, priority dispatch, conversation history.
19. **Document Management**: Employee records, company policies, version control, expiration tracking.
20. **Announcements & Events**: Bulletins, pinned notices, company events, RSVP attendee management.
21. **Notifications**: Real-time notification center, category filtering, unread badge counters.

### Group 6: Intelligence & Administration
22. **Smart Insights**: 100% local ML & statistical engines, anomaly detection, burnout alerts, attrition risk scoring.
23. **Reports & Analytics**: 7 mandatory business outputs, aggregation charts, CSV data exports.
24. **Audit & System Administration**: Audit logs, security compliance, system settings, backup management.
""",

    "04_rbac_security.md": """# Chapter 4: Role-Based Access Control (RBAC) & Security Architecture

## 4.1 RBAC Role Matrix
Smart EMS defines four core system personas:
1. **Administrator (ADMIN)**: Full administrative access across all 24 modules, audit trails, and backup configurations.
2. **HR Manager (HR)**: Complete oversight of employee records, attendance, leave approvals, payroll/expenses, performance reviews, and recruitment.
3. **Team Manager (MANAGER)**: Operational oversight over direct reports, task assignments, project milestones, skill validations, and first-level approvals.
4. **Employee (EMPLOYEE)**: Self-service access to profile 360, attendance clock-in, leave applications, task Kanban, kudos, training, and tickets.

## 4.2 Security Architecture & Hardening
- **Password Security**: Argon2 / PBKDF2 hashing with salt.
- **Session Security**: HttpOnly, SameSite cookies, session expiration after inactivity.
- **Brute Force Protection**: Automatic account lockout after 5 consecutive failed login attempts within 15 minutes.
- **Audit Logging**: Automatic interceptor middleware recording user, IP, action, module, and timestamp on all state mutations.
""",

    "05_database_schema.md": """# Chapter 5: Database Schema & Data Dictionary

Comprehensive relational entity models structured across 24 apps:
- `apps.authentication.User`: Central identity model extending `AbstractUser`.
- `apps.permissions.Role`, `apps.permissions.ModulePermission`: Granular RBAC definitions.
- `apps.organization.Department`, `Team`, `Designation`, `OrganizationProfile`: Organizational backbone.
- `apps.employees.Employee`, `EmployeeEducation`, `EmployeeExperience`, `EmployeeBankDetail`: Master employee records.
- `apps.attendance.AttendanceRecord`: Daily attendance logs with timestamps and geofencing/IP metadata.
- `apps.leave_management.LeaveType`, `LeaveBalance`, `LeaveRequest`: Leave management ledger.
- `apps.shifts.WorkShift`, `ShiftAssignment`, `CompanyHoliday`: Roster schedule engine.
- `apps.workload.EmployeeWorkloadMetric`, `WorkloadHistory`: Workload capacity indexes.
- `apps.projects.Project`, `ProjectMilestone`, `ProjectSkillRequirement`: Project planning models.
- `apps.tasks.Task`, `SubTask`, `TaskComment`: Granular task execution.
- `apps.skills.SkillCategory`, `Skill`, `EmployeeSkill`: Competency matrix.
- `apps.goals.Goal`, `GoalProgressUpdate`: OKR performance targets.
- `apps.performance.ReviewCycle`, `PerformanceEvaluation`: 360 review rubrics.
- `apps.training.Course`, `TrainingEnrollment`: Corporate university engine.
- `apps.recognition.RecognitionCategory`, `EmployeeRecognition`: Social kudos wall.
- `apps.assets.AssetCategory`, `Asset`: Inventory management.
- `apps.expenses.ExpenseCategory`, `ExpenseClaim`: Financial reimbursement claims.
- `apps.helpdesk.TicketCategory`, `SupportTicket`, `TicketMessage`: Service desk ticketing.
- `apps.documents.DocumentCategory`, `EmployeeDocument`: Compliance records.
- `apps.announcements.Announcement`, `CompanyEvent`, `EventRegistration`: Internal communications.
- `apps.notifications.Notification`: User notifications.
- `apps.insights.SmartInsight`: Machine learning findings & actionable recommendations.
- `apps.administration.AuditLog`, `SystemSetting`, `BackupConfiguration`: Administrative control.
""",

    "06_employee_360.md": """# Chapter 6: Employee 360° Comprehensive System

The **Employee 360° Profile** serves as the central operational hub for each employee.
Aggregated through `Employee360Service`, it presents 11 integrated views:
1. **Overview & Profile Header**: Job title, department, direct manager, employment status, tenure, contact info.
2. **Attendance Summary**: 30-day attendance breakdown (Present, Late, Absent, Half-Day, Total Hours).
3. **Leave Ledger**: Real-time balances across Casual, Sick, and Annual leave categories.
4. **Workload & Capacity**: Current workload score (0-100), active tasks count, estimated hours backlog.
5. **Projects & Deliverables**: Active project assignments, leadership roles, and milestone tracking.
6. **Task Kanban Summary**: Assigned tasks broken down by status (Todo, In Progress, Review, Done).
7. **Skill Profile**: Endorsed skills with verified proficiency badges.
8. **Goals & OKRs**: Current quarter targets and milestone progress bars.
9. **Performance History**: Historical appraisal scores and manager feedback.
10. **Hardware Assets**: Assigned laptops, displays, and peripherals.
11. **Documents & Certifications**: Validated employment contracts, NDA status, and course certificates.
""",

    "20_smart_insights_ml.md": """# Chapter 20: Smart Insights Engine: Local ML, Anomaly Detection & Statistical Analytics

## 20.1 100% Local Intelligence Architecture
Smart EMS is completely self-contained. It performs zero external API calls and requires no third-party cloud AI subscriptions. All intelligence is computed directly on the server utilizing:
- **NumPy & Pandas**: High-performance vector operations and DataFrame statistical rollups.
- **Scikit-learn**: IsolationForest anomaly detection, linear regression trend estimation.
- **SciPy**: Standard deviation calculations, IQR dispersion, and z-score anomaly modeling.

## 20.2 The 10 Specialized Analyzer Modules
1. `AttendanceAnalyzer`: Computes punctuality degradation, consecutive late trends, and absenteeism spikes.
2. `WorkloadAnalyzer`: Calculates employee capacity strain, impending burnout risk, and task distribution imbalances.
3. `SkillAnalyzer`: Analyzes organization-wide competency gaps, single points of failure, and training recommendations.
4. `GoalAnalyzer`: Tracks OKR velocity, detects stalled milestones, and projects completion dates.
5. `PerformanceAnalyzer`: Maps employees to the 9-box talent matrix and identifies top performers and at-risk contributors.
6. `TrainingAnalyzer`: Identifies expired certifications, skill refreshers, and course pass rates.
7. `AnomalyDetector`: Local IsolationForest and Z-Score outlier detection across attendance and expense submissions.
8. `ScoringEngine`: Synthesizes multi-factor health scores for departments and teams.
9. `RecommendationEngine`: Generates prescriptive, contextual action items for HR and managers.
10. `SmartInsightService`: Orchestration pipeline managing automated insight triggers and retention.
""",

    "21_deployment_and_operations.md": """# Chapter 21: Deployment, CLI Operations, Troubleshooting & Maintenance Guide

## 21.1 Environment Setup
```bash
# 1. Clone / Enter project directory
cd c:/Users/BABI/Desktop/EMS

# 2. Activate virtual environment
python -m venv venv
venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Populate enterprise demo dataset
python manage.py seed_data

# 6. Run automated test suite
pytest

# 7. Start development server
python manage.py runserver 8000
```

## 21.2 Management CLI Commands
- `python manage.py seed_data`: Seeds 28 employees, 45-day attendance history, projects, tasks, skills, and initial insights.
- `python manage.py calculate_workload`: Recalculates workload index scores and capacity statuses for all active employees.
- `python manage.py generate_insights`: Executes full local ML and statistical analysis suite, generating actionable findings.
"""
}

for filename, content in CHAPTERS.items():
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath}")

print("Documentation generated successfully!")
