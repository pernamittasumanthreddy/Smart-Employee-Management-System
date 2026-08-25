import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

MODULES_DATA = [
    ("01_authentication", "Authentication, RBAC & Identity", "Manages enterprise user sessions, multi-factor login security, password hashing, and user authentication audit history."),
    ("02_employees", "Employee 360° Profiles & Directory", "Centralized workforce repository containing complete personal, educational, banking, and professional employee lifecycles."),
    ("03_organization", "Organizational Hierarchy & Chart", "Configures enterprise business units, divisions, departments, agile squads, and designation grade ladders."),
    ("04_permissions", "Granular Roles & Permissions Matrix", "Fine-grained role definition granting module-level permissions across Administrator, HR, Manager, and Staff personas."),
    ("05_attendance", "Workforce Attendance & Biometric Ingestion", "Automated shift punch capture, GPS geofencing radius validation, and daily biometric terminal ingestion."),
    ("06_leave_management", "Leave Requests & Accrual Engine", "Annual privilege leave quota tracking, statutory maternity/paternity policies, and multi-tier manager approval flows."),
    ("07_shifts", "Shift Scheduling & Statutory Holidays", "24/7 rotational shift planning, overtime rules, night differential allowances, and official holiday calendars."),
    ("08_workload", "Workload Balancing & Capacity Planning", "Real-time task allocation analytics, burnout risk indicators, and sprint capacity distribution."),
    ("09_projects", "Project Portfolio & Milestone Tracking", "Cross-departmental project management, milestone deliverables, and budget burn-rate tracking."),
    ("10_tasks", "Task Management & Agile Kanban Boards", "Subtask task checklists, drag-and-drop status boards, priority flags, and estimated-vs-actual hours."),
    ("11_skills", "Skills Catalog & Competency Matrix", "Organizational capability mapping, proficiency grading, and single point of failure gap analytics."),
    ("12_goals", "Goals, Targets & OKRs Framework", "Objective & Key Results (OKR) cascades aligning corporate strategies with quarterly individual targets."),
    ("13_performance", "Performance Appraisals & 360 Reviews", "Structured review cycles, self-evaluations, manager appraisals, and normalized bell-curve rankings."),
    ("14_training", "Corporate Learning & LMS Catalog", "Employee upskilling courses, mandatory compliance modules, enrollment tracking, and certification awards."),
    ("15_recognition", "Peer Recognition, Kudos & Gamification", "Social appreciation feed, peer praise badges, monthly kudos leaderboards, and values recognition."),
    ("16_assets", "IT Assets & Hardware Inventory", "Asset provisioning, hardware lifecycle depreciation, warranty tracking, and serial number barcoding."),
    ("17_expenses", "Expense Claims & Reimbursement Pipeline", "Travel and corporate expense claims, receipt attachment OCR, manager approvals, and finance payment batches."),
    ("18_helpdesk", "Internal IT & HR Support Ticketing", "Incident resolution ticketing, SLA deadline escalations, threaded discussion notes, and satisfaction ratings."),
    ("19_documents", "Document Management & Policy Vault", "Encrypted storage for offer letters, identity proofs, compliance declarations, and standard operating policies."),
    ("20_announcements", "Company Broadcasts & Event Calendar", "Town hall meetings, quarterly leadership updates, holiday alerts, and organization-wide broadcast bulletins."),
    ("21_notifications", "Real-time Alerts & Notification Center", "Multi-channel in-app badge alerts, high-priority notifications, and email event triggers."),
    ("22_insights", "Smart Workforce Insights (ML / Analytics)", "Machine learning models forecasting flight risk, attrition indicators, and team sentiment patterns."),
    ("23_reports", "Enterprise Reports & Export Hub", "Multi-dimensional analytical summaries, tabular CSV/Excel downloads, and headcount turnover metrics."),
    ("24_administration", "System Administration & Audit Logs", "Comprehensive immutable audit trails, system parameter configurations, and automated database backups."),
    ("25_payroll", "Enterprise Payroll & Tax Engine", "Salary structures, Indian Income Tax calculations (Old vs New Regime), PF/ESI statutory compliance, and monthly payslips."),
    ("26_recruitment", "Talent Acquisition & ATS Pipeline", "Job requisitions, candidate pipeline Kanban board, interview scorecards, and digital offer letters."),
    ("27_lifecycle", "Employee Onboarding & Exit Clearances", "Automated new hire task checklists, probation confirmations, resignation tracking, and multi-department exit clearances."),
    ("28_compliance", "Labor Law Compliance & POSH Framework", "Form A, B, C, D statutory registers, internal compliance audits, and confidential POSH committee redressal."),
    ("29_benefits", "Corporate Benefits & Health Insurance", "Group Mediclaim floater coverage, dependent enrollments, TPA claims processing, and flexible benefit plans."),
    ("30_timesheets", "Client Timesheets & Project Billing", "Weekly billable hours logging, client project rate cards, and manager approval sign-offs."),
    ("31_surveys", "Workforce Pulse & eNPS Analytics", "Quarterly Employee Net Promoter Score surveys, anonymous pulse polls, and sentiment distribution dashboards."),
    ("32_workplace", "Smart Workplace, Desks & Travel Requests", "Hot-desking reservations, boardroom scheduling, corporate travel authorizations, and visitor passes."),
    ("33_api", "Developer REST API & Webhooks Suite", "JSON RESTful API endpoints for external integrations, biometric device sync, and OpenAPI 3.0 specs."),
    ("34_automation", "Event-Driven Workflow Automation Engine", "Custom trigger-action workflow rules across employee milestones, notifications, and task creation."),
]

for code, title, desc in MODULES_DATA:
    content = f"""# {title} — Architectural & Functional Specification

## 1. Module Overview
The **{title}** module ({code}) forms a core operational component of the Bharat Enterprise Solutions Smart EMS platform.
{desc}

## 2. Business Value & Key Capabilities
- **Enterprise Scalability**: Designed for zero-downtime execution in high-concurrency environments.
- **Role-Based Authorization**: Deeply integrated with the core RBAC matrix to restrict sensitive data by role.
- **Audit & Compliance**: Every create, update, and delete event is tracked in the immutable security audit log.
- **Automated Workflow Integration**: Dispatches events to the automation engine for reactive notifications.

## 3. Data Architecture & Entity Relationships
The module implements robust Django ORM models with database constraints, foreign keys, unique indices, and transaction-safe atomic mutations.

## 4. API Endpoints & Interfaces
- Standard RESTful endpoints supported with JSON payload responses.
- Clean view handlers with filtering, sorting, pagination, and export capabilities.

## 5. Security & Data Protection
- CSRF middleware validation across all web forms.
- Data field masking for personally identifiable information (PII).
- Role-gated view decorators ensuring only authorized personnel access operational controls.
"""
    write_file(f"documentation/modules/{code}.md", content)

print("Finished generating documentation for all 34 enterprise modules.")
