import pytest
from decimal import Decimal
from django.utils import timezone
from apps.workplace.models import MeetingRoom, DeskBooking, TravelRequest, VisitorPass
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestWorkplaceDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="wp.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-WP-DEEP-01",
            first_name="Tanvi",
            last_name="Azmi",
            email="tanvi.wp@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.room = MeetingRoom.objects.create(
            name="Executive Boardroom Silicon",
            floor_number=4,
            capacity=18,
            has_video_conference=True,
            is_active=True
        )

    def test_desk_booking_and_travel(self):
        booking = DeskBooking.objects.create(
            employee=self.emp,
            desk_number="FL3-DESK-42",
            booking_date=timezone.now().date(),
            status="CONFIRMED"
        )
        travel = TravelRequest.objects.create(
            employee=self.emp,
            origin_city="Bengaluru",
            destination_city="Mumbai",
            departure_date=timezone.now().date(),
            return_date=timezone.now().date(),
            purpose="Quarterly Executive Strategy Review",
            estimated_cost=Decimal('28000.00'),
            status="APPROVED"
        )
        assert booking.status == "CONFIRMED"
        assert travel.estimated_cost == Decimal('28000.00')
