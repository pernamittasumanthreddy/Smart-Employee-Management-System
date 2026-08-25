# Authentication & Role-Based Access Control (RBAC) Guide

## 1. Overview
Smart EMS provides an enterprise-grade authentication and authorization framework built on top of Django's core authentication infrastructure, extended with multi-tenant role hierarchies, session hardening, and comprehensive permission matrices.

## 2. User Roles & Hierarchy
The platform defines four primary user tiers:
1. **Superadmin / Executive Administrator** (`ADMIN`): Full read/write/delete privileges across all 34 apps, tenant settings, and audit logs.
2. **HR Manager** (`HR_MANAGER`): Permissions for employee lifecycle, payroll processing, statutory compliance, performance reviews, and leave approvals.
3. **Department / Team Manager** (`MANAGER`): Team roster management, shift approvals, 1-on-1 performance evaluations, and expense claim verification.
4. **Staff Employee** (`EMPLOYEE`): Self-service portal access (attendance punch-in, leave application, payslip downloads, peer kudos, and helpdesk tickets).

## 3. Session Management & Security Controls
- **Cryptographic Hashing**: Argon2 / PBKDF2 with SHA256 password hashing.
- **CSRF & Clickjacking Protection**: Enforced on all mutating HTTP POST/PUT/DELETE requests.
- **Session Timeout & Inactivity Guards**: Automated session invalidation following configurable idle periods.
- **Audit Logging**: All authentication attempts, privilege escalations, and credential resets are recorded with timestamp and IP origin.
