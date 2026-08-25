# Chapter 7: Time, Attendance & Shift Engine

## 7.1 Real-Time Attendance Capture
The Attendance Management module tracks daily clock-in/out records with high-precision timestamping:
- **Shift Grace Period Calculation**: Shift configuration dictates a configurable grace window (default 15 minutes). Punches after grace window trigger automated `late_minutes` tracking and `is_late` flags.
- **Half-Day & Absenteeism Logic**: Automatically computes half-day status if total working hours fall below configured threshold (default 4.0 hours) and full-day threshold (8.0 hours).
- **Network & IP Auditing**: Records client IP address and user agent on every punch event for compliance tracking.

## 7.2 Shift Rosters & Holiday Calendars
- Flexible shift definition (Morning, Day, Evening, Night) with custom hour allocations.
- Direct employee shift assignment with start/end date bounds.
- Company-wide holiday calendar integration preventing false absent records on designated holidays.
