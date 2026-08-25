import pandas as pd

from apps.insights.models import InsightCategory, InsightSeverity
from apps.workload.models import EmployeeWorkloadMetric


class WorkloadAnalyzer:
    """
    Workload distribution and capacity anomaly analyzer using mathematical
    workload scoring and standard deviation clustering.
    """

    @classmethod
    def analyze_workload_health(cls):
        metrics = EmployeeWorkloadMetric.objects.all().select_related('employee__department', 'employee__team')
        if not metrics.exists():
            return []

        insights = []
        data = []
        for m in metrics:
            data.append({
                'employee_id': m.employee.id,
                'employee_name': m.employee.full_name,
                'department_id': m.employee.department_id,
                'department_name': m.employee.department.name if m.employee.department else 'N/A',
                'team_id': m.employee.team_id,
                'team_name': m.employee.team.name if m.employee.team else 'N/A',
                'score': m.workload_score,
                'active_tasks': m.active_tasks_count,
                'estimated_hours': float(m.estimated_task_hours),
                'overdue_tasks': m.overdue_tasks_count,
                'status': m.utilization_status,
            })

        df = pd.DataFrame(data)

        # 1. Overloaded Employees at High Risk of Burnout
        overloaded = df[df['score'] >= 85]
        for _, row in overloaded.iterrows():
            from apps.employees.models import Employee
            emp = Employee.objects.get(id=row['employee_id'])
            insights.append({
                'category': InsightCategory.WORKLOAD,
                'severity': InsightSeverity.HIGH,
                'employee': emp,
                'department': emp.department,
                'title': f"High Burnout Risk: Workload Index at {row['score']}%",
                'what_detected': f"{row['employee_name']} has {row['active_tasks']} active tasks ({row['estimated_hours']} estimated hours) and {row['overdue_tasks']} overdue deliverables.",
                'why_detected': f"Workload score of {row['score']}% significantly exceeds the safe threshold (85%). Overdue task count: {row['overdue_tasks']}.",
                'supporting_data': {
                    'workload_score': int(row['score']),
                    'active_tasks': int(row['active_tasks']),
                    'estimated_hours': row['estimated_hours'],
                    'overdue_tasks': int(row['overdue_tasks'])
                },
                'recommendation': "Reassign 2-3 non-urgent tasks to available peers or adjust target milestone delivery dates.",
                'confidence_score': 0.95
            })

        # 2. Underutilized Workforce Members with Available Bandwidth
        underutilized = df[df['score'] <= 25]
        for _, row in underutilized.iterrows():
            from apps.employees.models import Employee
            emp = Employee.objects.get(id=row['employee_id'])
            insights.append({
                'category': InsightCategory.WORKLOAD,
                'severity': InsightSeverity.LOW,
                'employee': emp,
                'department': emp.department,
                'title': f"Available Bandwidth: Workload at {row['score']}%",
                'what_detected': f"{row['employee_name']} has only {row['active_tasks']} active task(s) with {row['estimated_hours']} hours allocated.",
                'why_detected': f"Employee workload ({row['score']}%) is well below nominal target capacity (50-80%).",
                'supporting_data': {
                    'workload_score': int(row['score']),
                    'active_tasks': int(row['active_tasks']),
                    'estimated_hours': row['estimated_hours']
                },
                'recommendation': "Allocate new incoming project tasks or enroll the employee in upskilling training courses.",
                'confidence_score': 0.91
            })

        # 3. Team-Level Workload Imbalance (Variance & Standard Deviation)
        if 'team_id' in df.columns and len(df['team_id'].dropna().unique()) > 0:
            for team_id, team_df in df.groupby('team_id'):
                if len(team_df) >= 3:
                    std_dev = team_df['score'].std()
                    if std_dev > 25.0:
                        t_name = team_df['team_name'].iloc[0]
                        max_emp = team_df.loc[team_df['score'].idxmax()]['employee_name']
                        min_emp = team_df.loc[team_df['score'].idxmin()]['employee_name']
                        from apps.organization.models import Team
                        team_obj = Team.objects.filter(id=team_id).first()

                        insights.append({
                            'category': InsightCategory.WORKLOAD,
                            'severity': InsightSeverity.MEDIUM,
                            'employee': None,
                            'department': team_obj.department if team_obj else None,
                            'title': f"Severe Workload Imbalance in Team '{t_name}'",
                            'what_detected': f"Significant task distribution disparity detected across members of team '{t_name}'.",
                            'why_detected': f"Team workload standard deviation is high (σ={round(std_dev, 1)}). Highest load: {max_emp} ({team_df['score'].max()}%), Lowest: {min_emp} ({team_df['score'].min()}%).",
                            'supporting_data': {
                                'team_name': t_name,
                                'standard_deviation': round(std_dev, 1),
                                'max_workload': int(team_df['score'].max()),
                                'min_workload': int(team_df['score'].min())
                            },
                            'recommendation': "Team Manager should rebalance sprint backlog and delegate tasks from high-load members to low-load members.",
                            'confidence_score': 0.89
                        })

        return insights
