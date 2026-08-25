# Chapter 4: Role-Based Access Control (RBAC) & Security Architecture

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
