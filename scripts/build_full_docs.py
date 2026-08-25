import os

DOCS_DIR = "documentation"
os.makedirs(DOCS_DIR, exist_ok=True)

CHAPTERS = {
    "07_time_attendance_shift_engine.md": """# Chapter 7: Time, Attendance & Shift Engine

## 7.1 Real-Time Attendance Capture
The Attendance Management module tracks daily clock-in/out records with high-precision timestamping:
- **Shift Grace Period Calculation**: Shift configuration dictates a configurable grace window (default 15 minutes). Punches after grace window trigger automated `late_minutes` tracking and `is_late` flags.
- **Half-Day & Absenteeism Logic**: Automatically computes half-day status if total working hours fall below configured threshold (default 4.0 hours) and full-day threshold (8.0 hours).
- **Network & IP Auditing**: Records client IP address and user agent on every punch event for compliance tracking.

## 7.2 Shift Rosters & Holiday Calendars
- Flexible shift definition (Morning, Day, Evening, Night) with custom hour allocations.
- Direct employee shift assignment with start/end date bounds.
- Company-wide holiday calendar integration preventing false absent records on designated holidays.
""",

    "08_leave_lifecycle_approval.md": """# Chapter 8: Leave Lifecycle & Approval Hierarchy

## 8.1 Leave Policy & Quota Allocations
- **Configurable Leave Types**: Casual Leave (CL), Sick & Medical Leave (SL), Earned / Annual Vacation (EL), Maternity / Paternity Leave.
- **Annual Ledger Allocation**: Automatically creates per-employee annual balances with `total_allocated`, `used_days`, and `pending_days`.
- **Validation Engine**: Calculates business day spans (excluding weekends/holidays) and rejects requests exceeding available balances.

## 8.2 Two-Way Approval Flow
```
[ Employee Application ] 
          │
          ▼
[ Overlap & Balance Check ] ── (Fails) ──> [ Request Rejected Instantly ]
          │ (Passes)
          ▼
[ Pending State + Manager Notification ]
          │
          ├─────────────────────────┐
          ▼                         ▼
   [ Manager Approve ]       [ Manager Reject ]
          │                         │
[ Balance Deducted ]       [ Pending Balance Released ]
```
""",

    "09_workload_balancing_capacity.md": """# Chapter 9: Workload Balancing & Algorithmic Capacity Index

## 9.1 Multi-Factor Capacity Algorithm
The `WorkloadCalculationService` evaluates active deliverables using a multi-factor mathematical formula:
```
Workload Score (0-100) = min(100, max(0, 
    ( Σ (Estimated Hours × Priority Weight × Urgency Factor) / Baseline Hours ) × 75
    + (Overdue Tasks × 5.0)
    + (Active Projects × 3.0)
))
```

### Priority & Urgency Weights:
- **Priority Weights**: URGENT (3.0), HIGH (2.0), MEDIUM (1.0), LOW (0.5).
- **Urgency Factor**: Overdue/Today (2.0), ≤ 3 Days (1.5), ≤ 7 Days (1.2), > 7 Days (1.0).

## 9.2 Capacity Utilization Categories
- **Underutilized (< 35)**: Available capacity for additional project staffing.
- **Balanced (35 - 75)**: Optimal workload distribution.
- **Optimal (76 - 88)**: High-performance delivery cadence.
- **Overloaded (> 88)**: Elevated burnout risk; triggers automated Smart Insight alert.
""",

    "10_project_task_kanban_framework.md": """# Chapter 10: Project, Task & Agile Kanban Delivery Framework

## 10.1 Project Portfolio Management
- Multi-project tracking with milestones, deliverables, project leads, team allocations, and budget burn rates.
- Automatic milestone progress rollups calculated from completion of underlying tasks.

## 10.2 Interactive Agile Kanban Board
- Visual Kanban columns: `TODO`, `IN_PROGRESS`, `REVIEW`, `COMPLETED`.
- Real-time drag-and-drop or state transitions updating actual vs estimated task hours.
- Subtask checklist tracking and threaded team discussion comments.
""",

    "11_skills_matrix_competency.md": """# Chapter 11: Skills Matrix & Organizational Competency Mapping

## 11.1 Skill Architecture
- Categorized skill taxonomy: Backend Engineering, Frontend UI, Cloud & DevOps, Data & Analytics, Management.
- Proficiency levels: 1 (Beginner), 2 (Intermediate), 3 (Advanced), 4 (Expert), 5 (Master).
- Peer endorsements and Manager verification stamps.

## 11.2 Team Matrix Heatmap & Gap Analysis
- Dynamic cross-department skill heatmaps visualizing team competencies.
- Staffing match analyzer matching active project skill requirements against available employee talent profiles.
""",

    "12_goals_okrs_strategic_alignment.md": """# Chapter 12: Goals, OKRs & Strategic Alignment Engine

## 12.1 Objective & Key Results (OKR) Framework
- Supports corporate, departmental, and individual goal cascading.
- Target metric tracking: Numeric targets, percentages, financial currencies, and boolean deliverables.
- Velocity tracking comparing elapsed time against current progress percentage.

## 12.2 Automated Check-Ins
- Periodic progress log entries with notes and confidence ratings.
- Automated detection of stalled OKRs without progress updates for > 14 days.
""",

    "13_performance_appraisal_9box.md": """# Chapter 13: Performance Appraisal, Multi-Factor Rubrics & 9-Box Matrix

## 13.1 Evaluation Rubrics
Structured multi-criteria performance appraisals:
- Technical Competency (1.00 - 5.00)
- Communication & Collaboration (1.00 - 5.00)
- Productivity & Delivery (1.00 - 5.00)
- Leadership & Initiative (1.00 - 5.00)
- Overall Weighted Score & Qualitative Assessment (Strengths, Growth Opportunities, Reviewer Comments).

## 13.2 9-Box Talent Matrix
Maps employees across Performance vs Potential:
- Top Talent / Star Performers (High Performance, High Potential)
- High Professionals (High Performance, Medium Potential)
- Core Contributors (Medium Performance, Medium Potential)
- Coaching Candidates (Low Performance, High Potential)
- Action Required (Low Performance, Low Potential)
""",

    "14_training_development_lifecycle.md": """# Chapter 14: Training, Development & Certification Lifecycle

## 14.1 Course & Curriculum Management
- Internal academy and external certification tracks.
- Duration hours, curriculum outlines, and minimum pass score requirements.

## 14.2 Certification Monitoring & Compliance
- Enrollment progress tracking: Enrolled -> In Progress -> Completed / Failed.
- Certificate upload and automated expiration notification dispatch 30/60 days prior to expiry.
""",

    "15_recognition_gamification.md": """# Chapter 15: Recognition, Gamification & Employee Engagement

## 15.1 Peer-to-Peer Kudos Wall
- Social recognition stream celebrating coworker achievements.
- Badge categories: Technical Excellence, Team Collaboration, Customer Hero, Leadership, Innovation.

## 15.2 Gamified Points & Leaderboards
- Points awarded per recognition badge.
- Real-time monthly and all-time leaderboard showing top recognized employees.
""",

    "16_asset_management_hardware.md": """# Chapter 16: Enterprise Asset Management & Hardware Lifecycle

## 16.1 Asset Tracking & Custody
- Comprehensive tracking of company hardware: Laptops, Monitors, Mobile Devices, Lab Equipment.
- Serial number indexing, warranty expiration monitors, and purchase value records.

## 16.2 Assignment & Maintenance Lifecycle
- Status workflow: `AVAILABLE` -> `ASSIGNED` -> `MAINTENANCE` -> `DAMAGED` -> `RETIRED`.
- Complete custodial assignment and return history logged with timestamps.
""",

    "17_expense_claims_financial_audit.md": """# Chapter 17: Multi-Tier Expense Claims & Financial Auditing

## 17.1 Expense Submission Flow
- Category allocation: Travel & Lodging, Hardware & Equipment, Client Meals, Professional Certifications.
- Receipt file attachment and currency formatting.

## 17.2 Approval & Reimbursement
- Approval workflow with manager review, rejection reasons, and finance payout auditing.
""",

    "18_helpdesk_support_slas.md": """# Chapter 18: Helpdesk, Service Level Agreements (SLAs) & Internal Support

## 18.1 Service Desk Architecture
- Ticket categorization: IT Hardware, Network & VPN, HR & Benefits, Facilities.
- Configurable SLA turnaround targets in hours.
- Priority levels: Urgent, High, Medium, Low.

## 18.2 Conversation Threads & Resolution
- Multi-party message thread per ticket.
- Ticket status lifecycle: `OPEN` -> `IN_PROGRESS` -> `PENDING_USER` -> `RESOLVED` -> `CLOSED`.
""",

    "19_document_management_compliance.md": """# Chapter 19: Enterprise Document Management & Compliance

## 19.1 Document Repository
- Employee specific records: Employment contracts, NDAs, identification, tax forms.
- Company-wide distributions: Employee handbook, code of conduct, information security policies.

## 19.2 Expiration & Compliance Auditing
- Expiration date tracking for visas, work permits, and annual agreements.
- Smart Insights integration alerting HR on upcoming compliance expirations.
"""
}

for filename, content in CHAPTERS.items():
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath}")

print("All 21 documentation chapters generated!")
