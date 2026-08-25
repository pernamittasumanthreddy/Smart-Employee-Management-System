import pytest
from decimal import Decimal
from django.utils import timezone
from apps.workplace.models import MeetingRoom, DeskBooking, TravelRequest
from apps.employees.models import Employee

@pytest.mark.django_db
def test_meeting_room_and_travel():
    room = MeetingRoom.objects.create(
        name="Chanakya Executive Room",
        floor="Floor 5",
        capacity_seats=16,
        has_video_conferencing=True
    )
    assert room.capacity_seats == 16
