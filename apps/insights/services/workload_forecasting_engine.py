"""
Workload & Capacity Predictive Forecasting Engine:
Calculates team capacity, sprint velocity, bottleneck bottlenecks, and burnout forecasts.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TeamCapacityForecast:
    team_name: str
    total_engineers: int
    gross_available_hours: float
    planned_leaves_hours: float
    net_effective_capacity_hours: float
    current_assigned_hours: float
    capacity_utilization_rate: float
    workload_status: str # OVERLOADED, OPTIMAL, UNDERUTILIZED
    estimated_sprint_story_points: int
    overload_risk_members: List[str]


class WorkloadForecastingEngine:
    """
    Algorithmic team workload balance and capacity predictor.
    """

    HOURS_PER_DAY = 8.0
    WORKING_DAYS_PER_SPRINT = 10 # 2-week sprint
    MAX_HEALTHY_UTILIZATION = 90.0 # Percentage
    MIN_HEALTHY_UTILIZATION = 60.0

    @classmethod
    def forecast_sprint_capacity(
        cls,
        team_name: str,
        member_workloads: List[Dict]
    ) -> TeamCapacityForecast:
        total_members = len(member_workloads)
        gross_hours = total_members * cls.HOURS_PER_DAY * cls.WORKING_DAYS_PER_SPRINT

        total_leave_hours = 0.0
        total_assigned_hours = 0.0
        overload_members = []

        for m in member_workloads:
            leave_hrs = m.get('leave_days', 0) * cls.HOURS_PER_DAY
            total_leave_hours += leave_hrs
            member_net_cap = (cls.WORKING_DAYS_PER_SPRINT * cls.HOURS_PER_DAY) - leave_hrs
            assigned_hrs = m.get('assigned_hours', 0.0)
            total_assigned_hours += assigned_hrs

            if member_net_cap > 0:
                member_util = (assigned_hrs / member_net_cap) * 100.0
                if member_util > 105.0:
                    overload_members.append(f"{m.get('name', 'Dev')} ({member_util:.0f}% load)")

        net_capacity = max(0.0, gross_hours - total_leave_hours)
        util_rate = (total_assigned_hours / net_capacity * 100.0) if net_capacity > 0 else 0.0

        if util_rate > cls.MAX_HEALTHY_UTILIZATION:
            status = 'OVERLOADED'
        elif util_rate < cls.MIN_HEALTHY_UTILIZATION:
            status = 'UNDERUTILIZED'
        else:
            status = 'OPTIMAL'

        # Story points estimation: ~6 net productive engineering hours per story point
        estimated_points = int(net_capacity / 6.0)

        return TeamCapacityForecast(
            team_name=team_name,
            total_engineers=total_members,
            gross_available_hours=round(gross_hours, 1),
            planned_leaves_hours=round(total_leave_hours, 1),
            net_effective_capacity_hours=round(net_capacity, 1),
            current_assigned_hours=round(total_assigned_hours, 1),
            capacity_utilization_rate=round(util_rate, 1),
            workload_status=status,
            estimated_sprint_story_points=estimated_points,
            overload_risk_members=overload_members
        )
