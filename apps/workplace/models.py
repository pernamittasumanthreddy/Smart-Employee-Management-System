from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class TravelRequest(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending Manager Approval'), ('APPROVED', 'Approved & Booked'), ('REJECTED', 'Rejected'), ('COMPLETED', 'Travel Completed')]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='travel_requests')
    purpose = models.CharField(max_length=200, help_text="e.g. AWS Summit London 2026, Client On-site Workshop")
    origin_city = models.CharField(max_length=100, default="Bengaluru")
    destination_city = models.CharField(max_length=100, default="San Francisco / London")
    departure_date = models.DateField()
    return_date = models.DateField()
    flight_preference = models.CharField(max_length=100, default="Economy Non-stop")
    hotel_needed = models.BooleanField(default=True)
    advance_cash_requested = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('50000.00'))
    estimated_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('180000.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    manager_approval_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        if 'estimated_cost' in kwargs and 'estimated_total_cost' not in kwargs:
            kwargs['estimated_total_cost'] = kwargs.pop('estimated_cost')
        super().__init__(*args, **kwargs)

    @property
    def estimated_cost(self):
        return self.estimated_total_cost

    @estimated_cost.setter
    def estimated_cost(self, val):
        self.estimated_total_cost = val

    def __str__(self):
        return f"Travel: {self.employee.full_name} -> {self.destination_city} ({self.departure_date})"


class DeskBooking(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='desk_bookings')
    building = models.CharField(max_length=100, default="Tower Alpha")
    floor = models.CharField(max_length=50, default="Floor 4 - Tech Hub")
    desk_number = models.CharField(max_length=30, default="DESK-4A-12")
    booking_date = models.DateField(default=timezone.now)
    time_slot = models.CharField(max_length=30, choices=[('FULL_DAY', 'Full Day (9 AM - 6 PM)'), ('MORNING', 'Morning (8 AM - 1 PM)'), ('EVENING', 'Afternoon/Evening (1 PM - 8 PM)')], default='FULL_DAY')
    has_dual_monitors = models.BooleanField(default=True)
    is_checked_in = models.BooleanField(default=True)
    status = models.CharField(max_length=30, default='CONFIRMED')

    class Meta:
        unique_together = ('building', 'floor', 'desk_number', 'booking_date', 'time_slot')

    def __str__(self):
        return f"{self.desk_number} - {self.employee.full_name} ({self.booking_date})"


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Aryabhata Boardroom, Ramanujan Brainstorm Pod")
    building = models.CharField(max_length=100, default="Tower Alpha")
    floor = models.CharField(max_length=50, default="Floor 3")
    capacity_seats = models.IntegerField(default=12)
    has_video_conferencing = models.BooleanField(default=True)
    has_whiteboard = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        if 'capacity' in kwargs and 'capacity_seats' not in kwargs:
            kwargs['capacity_seats'] = kwargs.pop('capacity')
        if 'has_video_conference' in kwargs and 'has_video_conferencing' not in kwargs:
            kwargs['has_video_conferencing'] = kwargs.pop('has_video_conference')
        if 'floor_number' in kwargs and 'floor' not in kwargs:
            kwargs['floor'] = f"Floor {kwargs.pop('floor_number')}"
        super().__init__(*args, **kwargs)

    @property
    def capacity(self):
        return self.capacity_seats

    @capacity.setter
    def capacity(self, val):
        self.capacity_seats = val

    @property
    def has_video_conference(self):
        return self.has_video_conferencing

    @has_video_conference.setter
    def has_video_conference(self, val):
        self.has_video_conferencing = val

    def __str__(self):
        return f"{self.name} ({self.capacity_seats} Seats, {self.floor})"



class VisitorPass(models.Model):
    visitor_name = models.CharField(max_length=150)
    visitor_company = models.CharField(max_length=150, default="External Partner / Client")
    visitor_email = models.EmailField()
    visitor_phone = models.CharField(max_length=30)
    host_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='hosted_visitors')
    visit_date = models.DateField(default=timezone.now)
    pass_code = models.CharField(max_length=50, unique=True)
    purpose = models.CharField(max_length=200, default="Quarterly Strategic Planning")
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    badge_number = models.CharField(max_length=30, default="VIS-042")

    def __str__(self):
        return f"Visitor: {self.visitor_name} -> Host: {self.host_employee.full_name}"
