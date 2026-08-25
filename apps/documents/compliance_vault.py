import hashlib
from typing import Dict, Any, List
from django.utils import timezone
from apps.documents.models import Document
from apps.employees.models import Employee

class ComplianceDocumentVault:
    '''
    Enterprise Secure Document Vault:
    - Cryptographic SHA-256 integrity verification
    - Mandatory compliance document expiration alerts (e.g. Visa, Passports, NDA renewals)
    - Departmental policy distribution tracking
    '''

    @staticmethod
    def compute_sha256_checksum(content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    @classmethod
    def audit_expiring_compliance_documents(cls, days_threshold: int = 60) -> List[Dict[str, Any]]:
        docs = Document.objects.select_related('uploaded_by').all()
        results = []
        now = timezone.now().date()

        for d in docs:
            exp_date = getattr(d, 'expiry_date', None)
            if exp_date:
                days_left = (exp_date - now).days
                if 0 <= days_left <= days_threshold:
                    results.append({
                        'document_id': d.id,
                        'title': d.title,
                        'uploaded_by': d.uploaded_by.full_name if d.uploaded_by else 'System',
                        'days_to_expiration': days_left,
                        'risk_severity': 'HIGH' if days_left <= 15 else 'MEDIUM',
                    })
        return results
