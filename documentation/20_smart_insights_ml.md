# Chapter 20: Smart Insights Engine: Local ML, Anomaly Detection & Statistical Analytics

## 20.1 100% Local Intelligence Architecture
Smart EMS is completely self-contained. It performs zero external API calls and requires no third-party cloud AI subscriptions. All intelligence is computed directly on the server utilizing:
- **NumPy & Pandas**: High-performance vector operations and DataFrame statistical rollups.
- **Scikit-learn**: IsolationForest anomaly detection, linear regression trend estimation.
- **SciPy**: Standard deviation calculations, IQR dispersion, and z-score anomaly modeling.

## 20.2 The 10 Specialized Analyzer Modules
1. `AttendanceAnalyzer`: Computes punctuality degradation, consecutive late trends, and absenteeism spikes.
2. `WorkloadAnalyzer`: Calculates employee capacity strain, impending burnout risk, and task distribution imbalances.
3. `SkillAnalyzer`: Analyzes organization-wide competency gaps, single points of failure, and training recommendations.
4. `GoalAnalyzer`: Tracks OKR velocity, detects stalled milestones, and projects completion dates.
5. `PerformanceAnalyzer`: Maps employees to the 9-box talent matrix and identifies top performers and at-risk contributors.
6. `TrainingAnalyzer`: Identifies expired certifications, skill refreshers, and course pass rates.
7. `AnomalyDetector`: Local IsolationForest and Z-Score outlier detection across attendance and expense submissions.
8. `ScoringEngine`: Synthesizes multi-factor health scores for departments and teams.
9. `RecommendationEngine`: Generates prescriptive, contextual action items for HR and managers.
10. `SmartInsightService`: Orchestration pipeline managing automated insight triggers and retention.
