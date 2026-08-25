# Chapter 5: Database Schema & Data Dictionary

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
