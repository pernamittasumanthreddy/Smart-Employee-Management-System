"""
Smart Enterprise Management System — Employee Pulse Surveys & eNPS Business Schemas & Data Contracts
Survey distribution, eNPS index calculation, and driver regression.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional


@dataclass
class SurveysDataContract:
    contract_id: str
    entity_code: str
    display_title: str
    status: str
    attributes: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def serialize_to_dict(self) -> Dict[str, Any]:
        return {
            'contract_id': self.contract_id,
            'entity_code': self.entity_code,
            'display_title': self.display_title,
            'status': self.status,
            'attributes': self.attributes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

    @classmethod
    def deserialize_from_dict(cls, data: Dict[str, Any]) -> 'SurveysDataContract':
        return cls(
            contract_id=data.get('contract_id', 'UNKNOWN'),
            entity_code=data.get('entity_code', 'ENT-000'),
            display_title=data.get('display_title', 'Untitled Entity'),
            status=data.get('status', 'ACTIVE'),
            attributes=data.get('attributes', {}),
            is_active=data.get('is_active', True)
        )
