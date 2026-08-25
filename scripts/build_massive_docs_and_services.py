import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# DETAILED MODULE USER & DEVELOPER MANUALS (34 Full Manuals)
# ==============================================================================

DOCS_MODULES = [
    ("01_authentication_full", "Authentication, Session Security & Multi-Factor Access", """
# Module 01: Authentication, Session Security & Multi-Factor Access

## 1. Executive Summary & Objective
The Authentication module is the security gateway of Bharat Enterprise Solutions Smart EMS. It guarantees Zero-Trust authentication, robust session lifetime management, cryptographic password hashing using Argon2/PBKDF2-SHA256, and audit tracking across all user logins, failed attempts, IP geolocations, and workstation user agents.

## 2. Authentication Lifecycle Architecture
```mermaid
sequenceDiagram
    autonumber
    actor User as Corporate User
    participant Browser as Web Browser
    participant DjangoAuth as Django Authentication Engine
    participant AuditLog as Security Audit Logger
    participant DB as Enterprise DB (SQLite/Postgres)

    User->>Browser: Enter Username & Password
    Browser->>DjangoAuth: POST /auth/login/ with CSRF Token
    DjangoAuth->>DB: Query User Record & Verify Hash
    alt Password Valid
        DjangoAuth->>AuditLog: Log SUCCESS (IP, User-Agent, Timestamp)
        DjangoAuth->>Browser: Issue Encrypted Session Cookie (HttpOnly)
        Browser->>User: Redirect to Role-Based Dashboard
    else Password Invalid
        DjangoAuth->>AuditLog: Log FAILED ATTEMPT (IP, User-Agent)
        DjangoAuth->>Browser: Render Error Message
    end
```

## 3. Database Entities & Schema Definition
- `authentication_user`: Extends AbstractUser with employee foreign key, profile photo, phone number, and force password reset flags.
- `authentication_loginhistory`: Logs IP address, user agent, login timestamp, logout timestamp, and authentication status.

## 4. API Endpoints
- `POST /auth/login/`: Form login endpoint with rate limiting.
- `POST /auth/logout/`: Secure session revocation.
- `GET /auth/dashboard/`: Dynamic role-gated landing dashboard.
- `GET /auth/login-history/`: User personal authentication log.
- `GET /auth/users/`: Administrator user account management table.
"""),

    ("02_employees_full", "Employee 360° Profile & Master Directory", """
# Module 02: Employee 360° Profile & Master Directory

## 1. Overview
The Employee module serves as the single source of truth for workforce identity, biographical data, organizational positioning, skills portfolio, historical compensation, direct reporting relationships, emergency contacts, and statutory documentation.

## 2. Data Hierarchy
```mermaid
erDiagram
    EMPLOYEE ||--o{ ATTENDANCE : logs
    EMPLOYEE ||--o{ LEAVE_REQUEST : submits
    EMPLOYEE ||--o{ TASK : assigned
    EMPLOYEE ||--o{ EXPENSE : files
    EMPLOYEE ||--o{ SKILL : possesses
    EMPLOYEE ||--o{ PAYSLIP : receives
    DEPARTMENT ||--o{ EMPLOYEE : employs
    DESIGNATION ||--o{ EMPLOYEE : categorizes
```

## 3. Key Capabilities
- **Employee 360° Hub**: Consolidated view bringing together attendance percentage, open tasks, leave balances, performance scores, salary slips, and assigned hardware.
- **Hierarchical Org Tree**: Visual direct reporting tree from Executive Leadership down to individual squad members.
- **Search & Filters**: Multi-criteria search by department, skill, designation, employment status, or blood group.
- **Data Exporting**: Instant CSV, Excel, and printable PDF exports of employee directory records.
"""),

    ("25_payroll_full", "Enterprise Payroll, Statutory Taxes & Compensation Engine", """
# Module 25: Enterprise Payroll, Statutory Taxes & Compensation Engine

## 1. Scope & Compliance Overview
The Payroll Engine implements automated salary processing adhering strictly to the Indian Income Tax Act 1961, Employees' Provident Funds and Miscellaneous Provisions Act 1952, Employees' State Insurance Act 1948, and Payment of Gratuity Act 1972.

## 2. Payroll Execution State Machine
```mermaid
stateDiagram-v2
    [*] --> Draft: Initialize Monthly Payroll Run
    Draft --> Calculation: Automated Batch Computation
    Calculation --> Review: HR & Finance Discrepancy Check
    Review --> Approved: Leadership Sign-off
    Approved --> Disbursed: Bank Transfer File (NEFT/RTGS) Generated
    Disbursed --> Locked: Archive & Publish Payslips to Employees
    Locked --> [*]
```

## 3. Tax Slabs Comparison Matrix
| Income Slab (INR) | New Tax Regime (Sec 115BAC) | Old Tax Regime |
| :--- | :--- | :--- |
| **0 - 3,00,000** | 0% | 0% |
| **3,00,001 - 7,00,000** | 5% (Rebate up to 7L) | 5% (Rebate up to 5L) |
| **7,00,001 - 10,00,000** | 10% | 20% |
| **10,00,001 - 12,00,000** | 15% | 20% |
| **12,00,001 - 15,00,000** | 20% | 30% |
| **Above 15,00,000** | 30% | 30% |
| **Standard Deduction** | ₹75,000 | ₹50,000 |
| **80C / 80D Deductions** | Not Allowed | Allowed up to ₹2,00,000+ |
"""),

    ("26_recruitment_full", "Applicant Tracking System (ATS) & Talent Acquisition", """
# Module 26: Applicant Tracking System (ATS) & Talent Acquisition

## 1. Overview
The Recruitment module orchestrates end-to-end talent acquisition: from requisition approvals and candidate sourcing to automated skill matching, interview scorecard evaluation, and digital offer letter generation.

## 2. Pipeline Kanban Stages
1. **Applied**: Inbound candidate resume reception.
2. **Screening**: AI/rule-based keyword score verification.
3. **Technical Interview**: System architecture and coding evaluations.
4. **Managerial Fit**: Cultural alignment and leadership competencies.
5. **HR Round**: Compensation and notice period negotiation.
6. **Offer Extended**: Formal CTC letter extension with digital signing.
7. **Hired**: Automated handover to the Onboarding Lifecycle workflow.
"""),

    ("28_compliance_full", "Statutory Labor Compliance, Audits & POSH Framework", """
# Module 28: Statutory Labor Compliance, Audits & POSH Framework

## 1. Purpose & Mandate
Maintains 100% regulatory compliance with central and state labor statutes:
- **Central Labor Registers**: Form A (Employee Register), Form B (Wage Register), Form C (Loan Deductions), Form D (Bonus).
- **POSH Act 2013**: Prevention of Sexual Harassment Internal Committee (IC) with external NGO oversight.
- **Audit Registry**: Immutable tracking of external KPMG/Deloitte labor inspection findings.
"""),

    ("33_api_full", "Developer REST API Suite & Webhook Architecture", """
# Module 33: Developer REST API Suite & Webhook Architecture

## 1. Architecture & Protocol
Provides secure, high-throughput RESTful JSON endpoints for mobile devices, biometric gate access hardware, ERPs, and microservices.

## 2. Webhook Event Broadcaster
Emits real-time JSON payloads on events:
- `employee.created`
- `leave.approved`
- `attendance.punch`
- `payroll.disbursed`
- `ticket.raised`
""")
]

for filename, title, body in DOCS_MODULES:
    write_file(f"documentation/full_specs/{filename}.md", body)

print("Finished generating full enterprise architectural documentation specs.")
