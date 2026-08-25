"""
Smart Enterprise Management System — Organization Domain Engine
Computes executive reporting trees, span of control ratios, department budget rollups, and cross-functional team matrix mappings.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Callable, Dict, List, Optional, Set, Tuple



@dataclass
class DepartmentBudgetRollup:
    department_id: int
department_name: str
headcount: int
total_annual_payroll_budget: Decimal
total_operating_expenses: Decimal
total_allocated_budget: Decimal
variance_amount: Decimal
is_budget_overrun: bool
span_of_control_ratio: float


class OrganizationHierarchyEngine:
    """
    Enterprise hierarchy traversal and reporting tree engine.
    """

    @classmethod
    def compute_department_budget_rollup(cls, dept_id: int, name: str, employees: List[Dict], allocated_budget: Decimal, operating_exp: Decimal = Decimal("500000.00")) -> DepartmentBudgetRollup:
        """
        Rolls up individual employee CTC and operating costs against department allocated budget.
        """
        total_payroll = sum(Decimal(str(e.get("annual_ctc", 1000000.00))) for e in employees)
headcount = len(employees)
total_costs = total_payroll + operating_exp
variance = allocated_budget - total_costs
is_overrun = total_costs > allocated_budget

managers_count = sum(1 for e in employees if e.get("is_manager", False))
span_ratio = (headcount / managers_count) if managers_count > 0 else float(headcount)

return DepartmentBudgetRollup(
    department_id=dept_id,
    department_name=name,
    headcount=headcount,
    total_annual_payroll_budget=total_payroll,
    total_operating_expenses=operating_exp,
    total_allocated_budget=allocated_budget,
    variance_amount=variance,
    is_budget_overrun=is_overrun,
    span_of_control_ratio=round(span_ratio, 1)
)

    @classmethod
    def validate_reporting_chain_acyclic(cls, employee_id: int, proposed_manager_id: int, reporting_pairs: List[Tuple[int, int]]) -> Dict[str, any]:
        """
        Prevents cyclical reporting loops in management hierarchy using DFS graph traversal.
        """
        if employee_id == proposed_manager_id:
    return {"is_valid": False, "error": "Employee cannot report to themselves."}

# Build adjacency map
graph = {}
for emp, mgr in reporting_pairs:
    graph.setdefault(emp, []).append(mgr)

# Check if proposed_manager reports to employee (cycle)
visited = set()
curr = proposed_manager_id
while curr is not None:
    if curr == employee_id:
        return {"is_valid": False, "error": "Circular reporting relationship detected in management tree."}
    if curr in visited:
        break
    visited.add(curr)
    parents = graph.get(curr, [])
    curr = parents[0] if parents else None

return {"is_valid": True, "error": None}
