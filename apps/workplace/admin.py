from django.contrib import admin
from apps.workplace.models import TravelRequest, DeskBooking, MeetingRoom, VisitorPass

@admin.register(TravelRequest)
class TravelRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'purpose', 'destination_city', 'departure_date', 'status')

@admin.register(DeskBooking)
class DeskBookingAdmin(admin.ModelAdmin):
    list_display = ('desk_number', 'employee', 'building', 'floor', 'booking_date')

@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'capacity_seats', 'has_video_conferencing')

@admin.register(VisitorPass)
class VisitorPassAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'host_employee', 'visit_date', 'badge_number')
