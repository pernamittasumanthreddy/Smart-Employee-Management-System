from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from apps.employees.models import Employee
from apps.notifications.services import NotificationService
from apps.recognition.forms import RecognitionForm
from apps.recognition.models import EmployeeRecognition


@login_required
def recognition_wall_view(request):
    recognitions = EmployeeRecognition.objects.all().select_related('sender__department', 'recipient__department', 'category')[:50]
    return render(request, 'recognition/wall.html', {'recognitions': recognitions})

@login_required
def send_recognition_view(request):
    sender = getattr(request.user, 'employee_profile', None)
    if not sender:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    form = RecognitionForm(request.POST or None)
    # Prevent self-recognition
    form.fields['recipient'].queryset = Employee.objects.filter(employment_status='ACTIVE').exclude(id=sender.id)

    if request.method == 'POST' and form.is_valid():
        recog = form.save(commit=False)
        recog.sender = sender
        recog.points_awarded = recog.category.points
        recog.save()

        # Notify recipient
        if recog.recipient.user:
            NotificationService.create_notification(
                user=recog.recipient.user,
                title="Kudos Received! 🎉",
                message=f"{sender.full_name} recognized you for {recog.category.name}: '{recog.title}'",
                category='RECOG',
                link="/recognition/"
            )

        messages.success(request, f"Kudos sent to {recog.recipient.full_name}!")
        return redirect('recognition:wall')

    return render(request, 'recognition/send_form.html', {'form': form})

@login_required
def recognition_leaderboard_view(request):
    """
    Renders top recognized employees by total kudos points.
    """
    top_receivers = Employee.objects.filter(employment_status='ACTIVE').annotate(
        total_kudos=Count('recognitions_received'),
        total_points=Sum('recognitions_received__points_awarded')
    ).filter(total_kudos__gt=0).order_by('-total_points')[:15]

    return render(request, 'recognition/leaderboard.html', {'top_receivers': top_receivers})
