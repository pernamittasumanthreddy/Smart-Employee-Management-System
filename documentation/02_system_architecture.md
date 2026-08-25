# Chapter 2: System Architecture & High-Level Design

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
