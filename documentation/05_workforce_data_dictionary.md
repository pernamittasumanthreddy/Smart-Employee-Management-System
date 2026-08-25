# Smart EMS Enterprise Data Dictionary & Model Schema

## 1. Core Model Tables
- `authentication_user`: Custom User entity extending AbstractUser with email authentication.
- `employees_employee`: Master workforce record with 360 profile linkage, employee ID, and reporting hierarchy.
- `organization_department`: Department nodes, budgets, codes, and leadership assignments.
- `payroll_salarystructure`: Compensation grades, CTC formulas, basic, HRA, and statutory percentages.
- `payroll_payslip`: Monthly wage receipts, earnings, deductions, and payment status.
- `recruitment_jobrequisition`: Headcount requests, required skill keywords, and hiring manager links.
- `lifecycle_onboardingworkflow`: Milestone checklists for new hire onboarding journeys.
- `compliance_statutoryregister`: Form A, B, C, D statutory registers for labor bureau inspections.
- `benefits_insurancepolicy`: Group medical insurance floater policies and coverage caps.
- `timesheets_weeklytimesheet`: Billable project hours submissions and manager approval records.
- `surveys_survey`: eNPS and anonymous workforce satisfaction questionnaire records.
- `workplace_deskbooking`: Hot-desk and meeting room reservation allocations.
- `automation_automationrule`: Event-condition-action workflow triggers.
