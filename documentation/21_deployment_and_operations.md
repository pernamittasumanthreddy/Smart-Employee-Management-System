# Chapter 21: Deployment, CLI Operations, Troubleshooting & Maintenance Guide

## 21.1 Environment Setup
```bash
# 1. Clone / Enter project directory
cd c:/Users/BABI/Desktop/EMS

# 2. Activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Populate enterprise demo dataset
python manage.py seed_data

# 6. Run automated test suite
pytest

# 7. Start development server
python manage.py runserver 8000
```

## 21.2 Management CLI Commands
- `python manage.py seed_data`: Seeds 28 employees, 45-day attendance history, projects, tasks, skills, and initial insights.
- `python manage.py calculate_workload`: Recalculates workload index scores and capacity statuses for all active employees.
- `python manage.py generate_insights`: Executes full local ML and statistical analysis suite, generating actionable findings.
