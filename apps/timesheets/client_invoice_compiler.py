from decimal import Decimal
from typing import List, Dict, Any

class ClientInvoiceCompiler:
    '''
    Aggregates billable timesheet records, applies hourly rate cards, computes GST (18%),
    and generates formal corporate client invoices.
    '''

    GST_RATE = Decimal('0.18')

    @classmethod
    def generate_invoice_summary(cls, client_name: str, invoice_number: str, line_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        subtotal = Decimal('0.00')
        for item in line_items:
            hours = Decimal(str(item.get('hours', 0)))
            rate = Decimal(str(item.get('hourly_rate', 0)))
            line_total = (hours * rate).quantize(Decimal('0.01'))
            item['line_total'] = line_total
            subtotal += line_total

        gst_amount = (subtotal * cls.GST_RATE).quantize(Decimal('0.01'))
        grand_total = (subtotal + gst_amount).quantize(Decimal('0.01'))

        return {
            'client_name': client_name,
            'invoice_number': invoice_number,
            'line_items': line_items,
            'subtotal': subtotal,
            'gst_rate_percent': 18.0,
            'gst_amount': gst_amount,
            'grand_total': grand_total,
            'currency': 'INR',
        }
