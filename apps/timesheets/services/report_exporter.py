"""
Smart Enterprise Management System — Client Timesheets & Project Billing Report Exporter & Data Formatter
Billable hours, hourly realization rates, and gross project margins.
"""

import csv
import io
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional


class TimesheetsReportExporter:
    """
    CSV and formatted data stream compiler for Client Timesheets & Project Billing.
    """

    @classmethod
    def export_dataset_to_csv(
        cls,
        records: List[Dict[str, Any]],
        custom_headers: Optional[List[str]] = None
    ) -> str:
        """
        Serializes dataset to RFC 4180 compliant CSV string.
        """
        output = io.StringIO()
        writer = csv.writer(output)

        if not records:
            writer.writerow(['No records available for export in timesheets'])
            return output.getvalue()

        headers = custom_headers or list(records[0].keys())
        writer.writerow([h.replace('_', ' ').title() for h in headers])

        for row in records:
            writer.writerow([row.get(h, '') for h in headers])

        return output.getvalue()

    @classmethod
    def format_summary_card(
        cls,
        title: str,
        kpi_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Formats metrics dictionary into dashboard presentation cards.
        """
        cards = []
        for k, v in kpi_metrics.items():
            formatted_val = f"₹ {v:,.2f}" if isinstance(v, (Decimal, float)) and 'amount' in k else str(v)
            cards.append({
                'metric_key': k,
                'metric_label': k.replace('_', ' ').title(),
                'display_value': formatted_val,
                'is_financial': isinstance(v, (Decimal, float))
            })

        return {
            'report_title': title,
            'module': 'timesheets',
            'generated_at': datetime.now().isoformat(),
            'cards': cards
        }
