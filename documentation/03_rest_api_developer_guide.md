# Smart EMS Developer REST API & Webhook Integration Guide

## 1. Authentication
API requests require token authentication via the `X-EMS-API-KEY` HTTP header or Bearer token authorization.

```http
GET /api/v1/employees/ HTTP/1.1
Host: 127.0.0.1:8000
X-EMS-API-KEY: ems_live_sec_token_984729104857201948571029384756
Accept: application/json
```

## 2. Core Endpoints Specification
- `GET /api/v1/employees/`: Returns active employee profiles with department and designation mapping.
- `GET /api/v1/attendance/today/`: Live daily presence statistics and check-in times.
- `POST /api/v1/biometric/sync/`: Ingests gate punch events from biometric fingerprint / facial terminals.
- `GET /api/v1/projects/`: Real-time project status and milestone progress metrics.
