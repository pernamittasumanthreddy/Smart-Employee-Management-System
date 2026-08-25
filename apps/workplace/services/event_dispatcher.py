"""
Smart Enterprise Management System — Smart Workplace & Facility Desk Booking Domain Event Dispatcher & Bus
Hot-desking capacity, desk sharing ratios, and travel requests.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
import uuid


@dataclass
class DomainEventEnvelope:
    event_id: str
    event_type: str
    module: str
    payload: Dict[str, Any]
    emitted_at: datetime
    priority: str # CRITICAL, HIGH, NORMAL, LOW
    is_processed: bool = False
    delivery_attempts: int = 0


class WorkplaceEventDispatcher:
    """
    Asynchronous event bus and domain webhook broadcaster for Smart Workplace & Facility Desk Booking.
    """

    REGISTERED_LISTENERS: List[Callable[[DomainEventEnvelope], None]] = []

    @classmethod
    def emit_event(
        cls,
        event_name: str,
        entity_id: int,
        event_data: Dict[str, Any],
        priority: str = 'NORMAL'
    ) -> DomainEventEnvelope:
        envelope = DomainEventEnvelope(
            event_id=f"EVT-WOR-{uuid.uuid4().hex[:8].upper()}",
            event_type=f"workplace.{event_name}",
            module="workplace",
            payload={'entity_id': entity_id, **event_data},
            emitted_at=datetime.now(),
            priority=priority,
            is_processed=False
        )

        for listener in cls.REGISTERED_LISTENERS:
            try:
                listener(envelope)
                envelope.delivery_attempts += 1
            except Exception:
                pass

        envelope.is_processed = True
        return envelope

    @classmethod
    def register_listener(cls, listener_fn: Callable[[DomainEventEnvelope], None]) -> None:
        if listener_fn not in cls.REGISTERED_LISTENERS:
            cls.REGISTERED_LISTENERS.append(listener_fn)

    @classmethod
    def clear_listeners(cls) -> None:
        cls.REGISTERED_LISTENERS.clear()
