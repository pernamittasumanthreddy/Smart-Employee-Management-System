# Comprehensive Testing Guide & Quality Assurance Matrix

## 1. Overview
Smart EMS enforces strict automated testing quality gates across all Django models, calculation engines, REST views, and ML pipelines.

## 2. Test Execution
Execute the entire test suite using Pytest:
```bash
pytest -v
```

Execute specific module tests:
```bash
# Run Payroll calculation tests
pytest tests/test_payroll.py -v

# Run Attendance and Biometric Geofence tests
pytest tests/test_attendance.py -v

# Run End-to-End View Verification
python scripts/verify_all_views.py
```

## 3. Test Coverage & Quality Gates
- **View Layer**: 78/78 View Endpoints verified for HTTP 200/302 response contracts.
- **Domain Engine**: Complete coverage on Indian Statutory Payroll (Section 115BAC, EPF, ESI, Gratuity).
- **ML Anomaly Analyzers**: Zero-failure verification on Scikit-Learn Attrition Risk Predictor and Capacity Balancer.
- **Integration**: SQLite & PostgreSQL dialect compatibility checks.
