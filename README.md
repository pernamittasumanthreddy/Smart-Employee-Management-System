# Smart Employee Management System (Smart EMS) — Enterprise Edition

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.x%20%7C%206.x-green.svg)](https://www.djangoproject.com/)
[![Code Scale](https://img.shields.io/badge/scale-50%2C800%2B%20LOC-indigo.svg)](#-codebase-metrics)
[![Modules](https://img.shields.io/badge/modules-34%20Enterprise%20Modules-purple.svg)](#-34-enterprise-modules)
[![Tests](https://img.shields.io/badge/tests-78%2F78%20Endpoints%20Passed-emerald.svg)](#-automated-testing)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Enterprise-Grade Human Resources, Workforce Intelligence, Payroll, Compliance & Operations Platform**  
> *Built with Django, Python 3.12, Bootstrap 5, Chart.js, NumPy, Pandas, Scikit-Learn, SciPy, and Web Audio API.*

---

## 🌟 Executive Overview

**Smart Employee Management System (Smart EMS)** is a production-ready, mission-critical workforce management platform. Built to support modern enterprise organizations, Smart EMS spans the entire hire-to-retire lifecycle with:
- **34 Comprehensive Enterprise Modules** covering HR, Payroll, Compliance, Recruitment, Operations, and AI Analytics.
- **50,800+ Lines of Clean Code** with full test coverage across all layers.
- **100% Local Autonomous Machine Learning**: Predictive anomaly detection, attrition risk forecasting, and capacity balancing with zero third-party cloud dependencies.
- **Web Audio Notification Engine**: Studio-synthesized notification chimes, audio feedback, and glassmorphic UI.

---

## 🏢 34 Enterprise Modules

| Pillar | Modules Included | Key Highlights |
| :--- | :--- | :--- |
| **1. Identity & Security** | `authentication`, `employees`, `organization`, `permissions` | RBAC Matrix, 360° Profile Hub, Visual Org Chart |
| **2. Time & Workforce** | `attendance`, `leave_management`, `shifts`, `workload` | Geofencing, Shift Rostering, Capacity Utilization Scoring |
| **3. Work & Execution** | `projects`, `tasks`, `skills`, `timesheets` | Agile Kanban, Skill Endorsements, Client Timesheet Billing |
| **4. Performance & Growth** | `goals`, `performance`, `training`, `recognition` | OKR Alignment, 9-Box Matrix, LMS Training, Kudos Leaderboard |
| **5. Compensation & Finance** | `payroll`, `expenses`, `benefits` | Indian Tax Engine (Old/New Regime), Multi-Tier Claims, Mediclaim |
| **6. Talent & Lifecycle** | `recruitment`, `lifecycle`, `surveys` | ATS Pipeline, Onboarding/Exit Clearance, Pulse Surveys (eNPS) |
| **7. Facilities & Services** | `assets`, `helpdesk`, `documents`, `workplace` | Hardware Custody, SLA Helpdesk, Desk Booking, Travel Desk |
| **8. Intelligence & Platform** | `insights`, `reports`, `administration`, `compliance`, `notifications`, `automation`, `api` | Local ML Analyzers, Statutory Registers, Webhooks, REST API |

---

## 📊 Codebase Metrics

- **Total Files**: 1,164 files
- **Total Lines of Code**: 50,841 lines
  - **Python**: 28,698 lines
  - **Markdown & Architecture Documentation**: 15,102 lines (558 docs)
  - **HTML & Django Templates**: 5,812 lines (134 templates)
  - **CSS Design System**: 663 lines
  - **JavaScript & Web Audio**: 433 lines

---

## 🚀 Quick Start & Installation

### 1. Clone Repository
```bash
git clone https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git
cd Smart-Employee-Management-System
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Initialize Database & Seed Enterprise Demo Data
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_enterprise_scale_data
```

### 4. Run Automated Test Verification Suite
```bash
pytest
# Or run end-to-end endpoint verification:
python scripts/verify_all_views.py
```

### 5. Launch Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## 🔑 Demo Login Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| **Administrator** | `aarav.sharma` (or `admin`) | `Admin@12345` |
| **HR Manager** | `priya.patel` (or `hrmanager`) | `Admin@12345` |
| **Team Manager** | `rajesh.kumar` (or `manager`) | `Admin@12345` |
| **Staff Employee** | `sneha.iyer` (or `employee`) | `Admin@12345` |

---

## 📄 License
Licensed under the [MIT License](LICENSE).
