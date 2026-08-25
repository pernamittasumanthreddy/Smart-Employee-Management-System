# Smart Employee Management System (Smart EMS)
> **Enterprise-Grade Human Resources & Workforce Intelligence Platform**  
> *Developed with Django, Python, Bootstrap 5, Chart.js, NumPy, Pandas, Scikit-Learn, and SciPy.*

---

## 🌟 Executive Overview
**Smart Employee Management System (Smart EMS)** is a comprehensive, production-ready workforce management suite. Designed for modern high-performance organizations, Smart EMS combines operational workflows (Attendance, Leave, Shifts, Projects, Tasks, Assets, Expenses, Helpdesk) with **100% local, autonomous machine learning and statistical workforce analytics** — with zero cloud or third-party API dependencies.

---

## 🚀 Key System Features

### 1. 🏢 Core & Security
- **Custom Authentication**: Enhanced session management, failed login attempt locking, password reset tokens.
- **RBAC Matrix**: Granular permissions (View, Add, Edit, Delete, Approve, Export, Admin) across 4 roles (`ADMIN`, `HR`, `MANAGER`, `EMPLOYEE`).
- **Organization Hierarchy**: Multi-department, multi-team, designation structuring with visual organizational trees.
- **Employee 360° View**: Unified single-pane profile aggregating 11 operational dimensions.

### 2. ⏱️ Time & Workforce
- **Attendance Management**: Daily clock-in/out, shift grace minutes, late minutes computation, IP logging.
- **Leave Management**: Leave quotas, balance ledgers, multi-day approval workflow with email notifications.
- **Shift & Holiday Management**: Work shifts, roster scheduling, company holiday calendar.
- **Workload Management**: Algorithmic workload scoring (0-100), capacity utilization statuses, overload alerts.

### 3. 🎯 Work & Productivity
- **Project Management**: Multi-project tracking, budget allocation, milestones, and automated progress rollups.
- **Task Management**: Interactive Agile Kanban boards, subtasks, priority weights, time tracking.
- **Skills Management**: Skill taxonomy, proficiency ratings (1-5), peer endorsements, team matrix heatmaps.
- **Goals & OKRs**: Objectives & Key Results tracking, progress velocities, check-in histories.

### 4. 📈 Employee Development
- **Performance Management**: Appraisal cycles, multi-criteria rubric evaluation, 9-box talent matrix.
- **Training & Development**: Corporate course catalog, progress tracking, certification expiration alerts.
- **Recognition & Feedback**: Social kudos wall, customizable badge categories, points leaderboard.

### 5. 🛠️ Employee Services
- **Asset Management**: Hardware inventory, custodial assignments, warranty expiration monitors.
- **Expense Management**: Multi-currency expense claims, receipt file attachments, multi-tier approvals.
- **Helpdesk & Support**: Service desk ticketing, SLA resolution tracking, threaded conversations.
- **Document Management**: Employee contract records, company-wide policies, compliance expiration tracking.
- **Announcements & Events**: Broadcast bulletins, pinned notices, company events with RSVP tracking.
- **Notification Center**: Real-time notifications with category filtering and unread counters.

### 6. 🧠 Intelligence & Administration
- **Smart Insights Engine**: 100% local ML & statistical analyzers (`AnomalyDetector`, `AttendanceAnalyzer`, `WorkloadAnalyzer`, `SkillAnalyzer`, etc.).
- **Reports & Analytics**: 7 mandatory business outputs, aggregation charts, CSV data exports.
- **Audit & Administration**: Full audit logging middleware, security compliance monitors, automated database backups.

---

## 🛠️ Technology Stack
- **Backend Framework**: Python 3.12+ / Django 5.x / 6.x
- **Data Layer**: Relational Database (SQLite / PostgreSQL)
- **Data Science & ML**: NumPy, Pandas, Scikit-learn, SciPy
- **Frontend & UI**: Django Templates, Vanilla CSS Design System, Bootstrap Icons, Chart.js
- **Testing**: Pytest, Pytest-Django (100% Pass Rate)

---

## 📦 Quick Start & Installation

### 1. Clone & Setup Virtual Environment
```bash
git clone <repository_url>
cd EMS
python -m venv venv
venv\\Scripts\\activate   # On Windows
# source venv/bin/activate # On Linux/macOS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply Migrations & Seed Enterprise Demo Data
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### 4. Run Automated Test Suite
```bash
pytest
```

### 5. Start Development Server
```bash
python manage.py runserver 8000
```
Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 🔑 Demo Credentials
| Role | Username | Password | Dashboard URL |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@12345` | `/dashboards/admin/` |
| **HR Manager** | `hrmanager` | `Admin@12345` | `/dashboards/hr/` |
| **Team Manager** | `manager` | `Admin@12345` | `/dashboards/manager/` |
| **Employee** | `employee` | `Admin@12345` | `/dashboards/employee/` |

---

## 📚 Complete Enterprise Documentation
Detailed technical documentation is available in the [`documentation/`](./documentation/) directory:
- [01. Executive Summary & Overview](./documentation/01_executive_summary.md)
- [02. System Architecture & Design](./documentation/02_system_architecture.md)
- [03. Complete 24-Module Specification](./documentation/03_24_module_specification.md)
- [04. RBAC & Security Architecture](./documentation/04_rbac_security.md)
- [05. Database Schema & Data Dictionary](./documentation/05_database_schema.md)
- [06. Employee 360° Comprehensive System](./documentation/06_employee_360.md)
- [07. Time, Attendance & Shift Engine](./documentation/07_time_attendance_shift_engine.md)
- [08. Leave Lifecycle & Approval Hierarchy](./documentation/08_leave_lifecycle_approval.md)
- [09. Workload Balancing & Capacity Index](./documentation/09_workload_balancing_capacity.md)
- [10. Project & Agile Kanban Framework](./documentation/10_project_task_kanban_framework.md)
- [11. Skills Matrix & Competency Mapping](./documentation/11_skills_matrix_competency.md)
- [12. Goals, OKRs & Alignment Engine](./documentation/12_goals_okrs_strategic_alignment.md)
- [13. Performance Appraisal & 9-Box Matrix](./documentation/13_performance_appraisal_9box.md)
- [14. Training & Certification Lifecycle](./documentation/14_training_development_lifecycle.md)
- [15. Recognition & Gamification](./documentation/15_recognition_gamification.md)
- [16. Hardware Asset Management](./documentation/16_asset_management_hardware.md)
- [17. Multi-Tier Expense Claims](./documentation/17_expense_claims_financial_audit.md)
- [18. Helpdesk & Support SLAs](./documentation/18_helpdesk_support_slas.md)
- [19. Document Management & Compliance](./documentation/19_document_management_compliance.md)
- [20. Smart Insights & Local ML Engines](./documentation/20_smart_insights_ml.md)
- [21. Deployment & Maintenance Guide](./documentation/21_deployment_and_operations.md)

---

## 📄 License
This project is licensed under the MIT Enterprise License.
