"""
Django settings for Smart Employee Management System.
Production-style architecture supporting SQLite, PostgreSQL, and MySQL.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-smart-employee-management-system-production-secret-key-2026-secure-hash'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Group 1: Core & Security
    'apps.authentication.apps.AuthenticationConfig',
    'apps.employees.apps.EmployeesConfig',
    'apps.organization.apps.OrganizationConfig',
    'apps.permissions.apps.PermissionsConfig',

    # Group 2: Time & Workforce
    'apps.attendance.apps.AttendanceConfig',
    'apps.leave_management.apps.LeaveManagementConfig',
    'apps.shifts.apps.ShiftsConfig',
    'apps.workload.apps.WorkloadConfig',

    # Group 3: Work & Productivity
    'apps.projects.apps.ProjectsConfig',
    'apps.tasks.apps.TasksConfig',
    'apps.skills.apps.SkillsConfig',
    'apps.goals.apps.GoalsConfig',

    # Group 4: Employee Development
    'apps.performance.apps.PerformanceConfig',
    'apps.training.apps.TrainingConfig',
    'apps.recognition.apps.RecognitionConfig',

    # Group 5: Employee Services
    'apps.assets.apps.AssetsConfig',
    'apps.expenses.apps.ExpensesConfig',
    'apps.helpdesk.apps.HelpdeskConfig',
    'apps.documents.apps.DocumentsConfig',
    'apps.announcements.apps.AnnouncementsConfig',
    'apps.notifications.apps.NotificationsConfig',

    # Group 6: Intelligence & Administration
    'apps.insights.apps.InsightsConfig',
    'apps.reports.apps.ReportsConfig',
    'apps.administration.apps.AdministrationConfig',

    # Group 7: Compensation, Talent & Lifecycle (Enterprise Expansion)
    'apps.payroll.apps.PayrollConfig',
    'apps.recruitment.apps.RecruitmentConfig',
    'apps.lifecycle.apps.LifecycleConfig',
    'apps.compliance.apps.ComplianceConfig',
    'apps.benefits.apps.BenefitsConfig',
    'apps.timesheets.apps.TimesheetsConfig',
    'apps.surveys.apps.SurveysConfig',
    'apps.workplace.apps.WorkplaceConfig',
    'apps.api.apps.ApiConfig',
    'apps.automation.apps.AutomationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom Audit and Request tracking middleware
    'apps.administration.middleware.AuditLoggingMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.notifications.context_processors.notification_context',
                'apps.permissions.context_processors.role_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
# Default to SQLite for zero-config local run, easily switchable via DATABASE_URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Model
AUTH_USER_MODEL = 'authentication.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads, avatars, documents, receipts)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session and Security Configuration
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
LOGIN_URL = 'authentication:login'
LOGIN_REDIRECT_URL = 'authentication:dashboard'
LOGOUT_REDIRECT_URL = 'authentication:login'

# Maximum upload size: 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760
