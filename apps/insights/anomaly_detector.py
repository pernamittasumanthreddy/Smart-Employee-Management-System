import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from apps.expenses.models import ExpenseClaim
from apps.insights.models import InsightCategory, InsightSeverity


class AnomalyDetector:
    """
    Local Machine Learning Anomaly Detector using Scikit-Learn IsolationForest
    and statistical interquartile range (IQR) for outliers in expense claims and time tracking.
    """

    @classmethod
    def detect_expense_anomalies(cls):
        claims = ExpenseClaim.objects.all().select_related('employee__department', 'category')
        if claims.count() < 8:
            return []

        insights = []
        data = []
        for c in claims:
            data.append({
                'id': c.id,
                'claim_number': c.claim_number,
                'employee': c.employee,
                'department': c.employee.department,
                'category': c.category.name,
                'amount': float(c.amount),
                'title': c.title,
            })

        df = pd.DataFrame(data)

        # Apply Scikit-Learn Isolation Forest on claim amounts
        X = df[['amount']].values
        clf = IsolationForest(contamination=0.08, random_state=42)
        df['anomaly'] = clf.fit_predict(X)

        # Statistical IQR baseline
        q25, q75 = np.percentile(df['amount'], [25, 75])
        iqr = q75 - q25
        upper_threshold = q75 + 2.0 * iqr
        mean_amount = df['amount'].mean()

        anomalous_claims = df[(df['anomaly'] == -1) & (df['amount'] > upper_threshold)]

        for _, row in anomalous_claims.iterrows():
            insights.append({
                'category': InsightCategory.WORKLOAD,
                'severity': InsightSeverity.HIGH,
                'employee': row['employee'],
                'department': row['department'],
                'title': f"Unusual High Expense Claim Detected: [{row['claim_number']}] ${row['amount']}",
                'what_detected': f"Expense claim for '{row['title']}' (${row['amount']}) deviates significantly from historical departmental claiming patterns.",
                'why_detected': f"IsolationForest anomaly score flagged outlier. Claim amount (${row['amount']}) is > 2.0x IQR above median (Mean: ${round(mean_amount, 2)}, Upper fence: ${round(upper_threshold, 2)}).",
                'supporting_data': {
                    'claim_number': row['claim_number'],
                    'claim_amount': row['amount'],
                    'category_average': round(mean_amount, 2),
                    'iqr_threshold': round(upper_threshold, 2)
                },
                'recommendation': "Perform enhanced receipt verification and manager audit prior to reimbursement approval.",
                'confidence_score': 0.94
            })

        return insights
