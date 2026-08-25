from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.permissions.decorators import hr_or_admin_required
from apps.training.forms import CourseForm
from apps.training.models import Course, EnrollmentStatus, TrainingEnrollment


@login_required
def course_catalog_view(request):
    search = request.GET.get('search', '').strip()
    courses = Course.objects.filter(is_active=True).select_related('category').annotate(
        total_enrolled=Count('enrollments')
    )
    if search:
        courses = courses.filter(Q(title__icontains=search) | Q(code__icontains=search) | Q(provider__icontains=search))
        
    return render(request, 'training/catalog.html', {'courses': courses, 'search': search})

@login_required
def my_trainings_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    enrollments = TrainingEnrollment.objects.filter(employee=employee).select_related('course__category')
    return render(request, 'training/my_trainings.html', {'enrollments': enrollments})

@login_required
def enroll_course_action(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    _enrollment, created = TrainingEnrollment.objects.get_or_create(
        employee=employee,
        course=course,
        defaults={'status': EnrollmentStatus.ENROLLED}
    )
    if created:
        messages.success(request, f"Successfully enrolled in '{course.title}'.")
    else:
        messages.info(request, f"You are already enrolled in '{course.title}'.")
    return redirect('training:my_trainings')

@login_required
@hr_or_admin_required
def course_create_view(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        course = form.save()
        messages.success(request, f"Course '{course.title}' added to catalog.")
        return redirect('training:catalog')
    return render(request, 'training/course_form.html', {'form': form, 'title': 'Add New Training Course'})

@login_required
def expiring_certifications_view(request):
    """
    Lists certifications expiring within 60 days across the workforce.
    """
    today = timezone.now().date()
    sixty_days = today + timezone.timedelta(days=60)
    expiring = TrainingEnrollment.objects.filter(
        status=EnrollmentStatus.COMPLETED,
        certificate_expiry_date__isnull=False,
        certificate_expiry_date__lte=sixty_days
    ).select_related('employee__department', 'course').order_by('certificate_expiry_date')

    return render(request, 'training/expiring_certifications.html', {'expiring': expiring, 'today': today})
