"""
Smart Enterprise Management System — Developer REST API & Integrations Report Exporter & Data Formatter
REST endpoints, API keys, rate limiting, and webhook dispatches.
"""

import csv
import io
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional


class ApiReportExporter:
    """
    CSV and formatted data stream compiler for Developer REST API & Integrations.
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
            writer.writerow(['No records available for export in api'])
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
            'module': 'api',
            'generated_at': datetime.now().isoformat(),
            'cards': cards
        }
