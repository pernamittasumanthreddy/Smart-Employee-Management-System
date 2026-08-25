# Chapter 8: Leave Lifecycle & Approval Hierarchy

## 8.1 Leave Policy & Quota Allocations
- **Configurable Leave Types**: Casual Leave (CL), Sick & Medical Leave (SL), Earned / Annual Vacation (EL), Maternity / Paternity Leave.
- **Annual Ledger Allocation**: Automatically creates per-employee annual balances with `total_allocated`, `used_days`, and `pending_days`.
- **Validation Engine**: Calculates business day spans (excluding weekends/holidays) and rejects requests exceeding available balances.

## 8.2 Two-Way Approval Flow
```
[ Employee Application ] 
          │
          ▼
[ Overlap & Balance Check ] ── (Fails) ──> [ Request Rejected Instantly ]
          │ (Passes)
          ▼
[ Pending State + Manager Notification ]
          │
          ├─────────────────────────┐
          ▼                         ▼
   [ Manager Approve ]       [ Manager Reject ]
          │                         │
[ Balance Deducted ]       [ Pending Balance Released ]
```
