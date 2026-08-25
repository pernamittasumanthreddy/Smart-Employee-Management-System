from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.workplace.models import TravelRequest, DeskBooking, MeetingRoom, VisitorPass

@login_required
def workplace_dashboard(request):
    travel_requests = TravelRequest.objects.select_related('employee').all()[:6]
    desk_bookings = DeskBooking.objects.select_related('employee').all()[:8]
    meeting_rooms = MeetingRoom.objects.filter(is_active=True)
    visitors = VisitorPass.objects.select_related('host_employee').all()[:6]

    context = {
        'travel_requests': travel_requests,
        'desk_bookings': desk_bookings,
        'meeting_rooms': meeting_rooms,
        'visitors': visitors,
    }
    return render(request, 'workplace/dashboard.html', context)

@login_required
def travel_list(request):
    travels = TravelRequest.objects.select_related('employee')
    return render(request, 'workplace/travel_list.html', {'travels': travels})

@login_required
def desk_booking_portal(request):
    bookings = DeskBooking.objects.select_related('employee').all()[:20]
    return render(request, 'workplace/desk_booking.html', {'bookings': bookings})
