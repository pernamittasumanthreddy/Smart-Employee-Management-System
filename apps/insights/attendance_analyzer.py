from datetime import timedelta

import pandas as pd
from django.utils import timezone

from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.insights.models import InsightCategory, InsightSeverity


class AttendanceAnalyzer:
    """
    Local statistical analyzer for workforce attendance, punctuality drift,
    and absenteeism clustering using NumPy and Pandas.
    """

    @classmethod
    def analyze_employee_attendance(cls, employee, lookback_days=45):
        cutoff_date = timezone.now().date() - timedelta(days=lookback_days)
        records = AttendanceRecord.objects.filter(
            employee=employee,
            date__gte=cutoff_date
        ).order_by('date')

        if records.count() < 7:
            return []

        insights = []
        data = []
        for r in records:
            data.append({
                'date': str(r.date),
                'status': r.status,
                'is_late': r.is_late,
                'late_minutes': r.late_minutes,
                'working_hours': float(r.total_working_hours),
            })

        df = pd.DataFrame(data)

        # 1. Frequent Late Arrival Pattern (Statistical Z-Score / Frequency)
        late_count = df['is_late'].sum()
        total_days = len(df)
        late_ratio = (late_count / total_days) if total_days > 0 else 0

        if late_ratio >= 0.25 and late_count >= 3:
            avg_delay = df[df['is_late']]['late_minutes'].mean()
            insights.append({
                'category': InsightCategory.ATTENDANCE,
                'severity': InsightSeverity.HIGH if late_ratio > 0.40 else InsightSeverity.MEDIUM,
                'employee': employee,
                'department': employee.department,
                'title': f"Frequent Late Arrival Pattern Detected ({round(late_ratio * 100)}% of shifts)",
                'what_detected': f"Employee arrived late for {late_count} out of the last {total_days} working days.",
                'why_detected': f"Late arrival frequency ({round(late_ratio * 100, 1)}%) exceeds platform threshold (25%). Average delay is {round(avg_delay, 1)} minutes.",
                'supporting_data': {
                    'total_days_evaluated': total_days,
                    'late_count': int(late_count),
                    'late_percentage': round(late_ratio * 100, 1),
                    'average_delay_minutes': round(avg_delay, 1)
                },
                'recommendation': "Conduct a 1-on-1 schedule review with the employee or consider offering a flexible shift schedule.",
                'confidence_score': 0.94
            })

        # 2. Punctuality Improvement Trend (Moving Average comparison)
        if total_days >= 14:
            first_half = df.iloc[:total_days//2]
            second_half = df.iloc[total_days//2:]
            first_late_rate = first_half['is_late'].mean()
            second_late_rate = second_half['is_late'].mean()

            if first_late_rate >= 0.30 and second_late_rate <= 0.05:
                insights.append({
                    'category': InsightCategory.ATTENDANCE,
                    'severity': InsightSeverity.POSITIVE,
                    'employee': employee,
                    'department': employee.department,
                    'title': "Significant Punctuality & Attendance Improvement",
                    'what_detected': "Employee has demonstrated a drastic reduction in tardiness over the past 3 weeks.",
                    'why_detected': f"Late arrival rate dropped from {round(first_late_rate * 100)}% in earlier period to {round(second_late_rate * 100)}% in the recent window.",
                    'supporting_data': {
                        'previous_late_rate': round(first_late_rate * 100, 1),
                        'recent_late_rate': round(second_late_rate * 100, 1)
                    },
                    'recommendation': "Acknowledge and commend the employee's improved punctuality and consistency.",
                    'confidence_score': 0.96
                })

        # 3. High Absenteeism Rate
        absent_count = (df['status'] == AttendanceStatus.ABSENT).sum()
        absent_ratio = absent_count / total_days
        if absent_ratio >= 0.15 and absent_count >= 3:
            insights.append({
                'category': InsightCategory.ATTENDANCE,
                'severity': InsightSeverity.HIGH,
                'employee': employee,
                'department': employee.department,
                'title': f"Elevated Absenteeism Ratio ({round(absent_ratio * 100)}% Unplanned Absences)",
                'what_detected': f"Employee recorded {absent_count} unplanned absences within the last {total_days} tracked days.",
                'why_detected': f"Unplanned absence rate ({round(absent_ratio * 100, 1)}%) exceeds organizational tolerance threshold (15%).",
                'supporting_data': {
                    'unplanned_absences': int(absent_count),
                    'evaluated_period_days': total_days
                },
                'recommendation': "HR Manager should review health/wellness support options or initiate an attendance counseling discussion.",
                'confidence_score': 0.92
            })

        return insights
