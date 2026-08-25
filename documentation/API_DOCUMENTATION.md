# REST API Documentation & Endpoints Specification

## 1. Overview
Smart EMS exposes a unified RESTful API surface spanning all 34 core modules. All endpoints conform to JSON request/response conventions and standard HTTP status codes.

## 2. Base URL & Authentication
- **Base URL**: `/api/v1/`
- **Authentication**: Bearer Token or Session Cookie
- **Content-Type**: `application/json`

## 3. Core Endpoint Matrix
| Module | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Employees** | `GET`, `POST` | `/api/v1/employees/` | List and onboard employees |
| **Attendance** | `POST` | `/api/v1/attendance/punch/` | Geofenced biometrics punch-in/out |
| **Payroll** | `GET`, `POST` | `/api/v1/payroll/runs/` | Execute payroll calculations & tax |
| **Leaves** | `GET`, `POST` | `/api/v1/leaves/requests/` | Submit and approve leave applications |
| **Performance**| `GET`, `PUT` | `/api/v1/performance/goals/` | Cascading OKRs and KPI updates |
| **Insights** | `GET` | `/api/v1/insights/attrition/` | ML Attrition flight risk predictions |

## 4. Response Format
```json
{
  "success": true,
  "status_code": 200,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2026-08-25T20:28:00Z"
}
```
