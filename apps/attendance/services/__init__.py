from datetime import datetime, time, timedelta

from django.db.models import Q
from django.utils import timezone

from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.shifts.models import ShiftAssignment, WorkShift


class AttendanceService:
    @staticmethod
    def get_employee_shift(employee, target_date=None):
        target_date = target_date or timezone.now().date()
        assignment = ShiftAssignment.objects.filter(
            employee=employee,
            is_active=True,
            start_date__lte=target_date
        ).filter(Q(end_date__isnull=True) | Q(end_date__gte=target_date)).select_related('shift').first()
        
        if assignment:
            return assignment.shift
        # Fallback default general shift
        default_shift, _ = WorkShift.objects.get_or_create(
            code='GEN',
            defaults={
                'name': 'General Day Shift',
                'start_time': time(9, 0),
                'end_time': time(17, 30),
                'grace_period_minutes': 15,
                'half_day_hours': 4.0,
                'full_day_hours': 8.0,
            }
        )
        return default_shift

    @staticmethod
    def check_in(employee, ip_address=None, notes=None):
        today = timezone.now().date()
        now_time = timezone.now().time()

        record, _created = AttendanceRecord.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={'status': AttendanceStatus.PRESENT, 'ip_address': ip_address, 'notes': notes}
        )

        if record.check_in_time:
            return record, False, "Already checked in today."

        record.check_in_time = now_time
        record.ip_address = ip_address
        if notes:
            record.notes = notes

        shift = AttendanceService.get_employee_shift(employee, today)
        shift_start_dt = datetime.combine(today, shift.start_time)
        grace_start_dt = shift_start_dt + timedelta(minutes=shift.grace_period_minutes)
        now_dt = datetime.combine(today, now_time)

        if now_dt > grace_start_dt:
            record.is_late = True
            diff = (now_dt - shift_start_dt).total_seconds() / 60.0
            record.late_minutes = int(diff)
        else:
            record.is_late = False
            record.late_minutes = 0

        record.status = AttendanceStatus.PRESENT
        record.save()
        return record, True, "Checked in successfully."

    @staticmethod
    def check_out(employee, ip_address=None):
        today = timezone.now().date()
        now_time = timezone.now().time()

        record = AttendanceRecord.objects.filter(employee=employee, date=today).first()
        if not record or not record.check_in_time:
            return None, False, "Cannot check out before checking in."

        record.check_out_time = now_time
        shift = AttendanceService.get_employee_shift(employee, today)
        shift_end_dt = datetime.combine(today, shift.end_time)
        now_dt = datetime.combine(today, now_time)

        if now_dt < shift_end_dt:
            record.is_early_departure = True
            diff = (shift_end_dt - now_dt).total_seconds() / 60.0
            record.early_minutes = int(diff)
        else:
            record.is_early_departure = False
            record.early_minutes = 0

        record.calculate_hours()
        return record, True, f"Checked out successfully. Total working hours: {record.total_working_hours} hrs."
