# Chapter 9: Workload Balancing & Algorithmic Capacity Index

## 9.1 Multi-Factor Capacity Algorithm
The `WorkloadCalculationService` evaluates active deliverables using a multi-factor mathematical formula:
```
Workload Score (0-100) = min(100, max(0, 
    ( Σ (Estimated Hours × Priority Weight × Urgency Factor) / Baseline Hours ) × 75
    + (Overdue Tasks × 5.0)
    + (Active Projects × 3.0)
))
```

### Priority & Urgency Weights:
- **Priority Weights**: URGENT (3.0), HIGH (2.0), MEDIUM (1.0), LOW (0.5).
- **Urgency Factor**: Overdue/Today (2.0), ≤ 3 Days (1.5), ≤ 7 Days (1.2), > 7 Days (1.0).

## 9.2 Capacity Utilization Categories
- **Underutilized (< 35)**: Available capacity for additional project staffing.
- **Balanced (35 - 75)**: Optimal workload distribution.
- **Optimal (76 - 88)**: High-performance delivery cadence.
- **Overloaded (> 88)**: Elevated burnout risk; triggers automated Smart Insight alert.
