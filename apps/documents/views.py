from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.documents.forms import EmployeeDocumentForm
from apps.documents.models import DocumentCategory, EmployeeDocument
from apps.permissions.decorators import hr_or_admin_required


@login_required
def document_library_view(request):
    search = request.GET.get('search', '').strip()
    cat_id = request.GET.get('category')

    docs = EmployeeDocument.objects.all().select_related('employee__department', 'category', 'uploaded_by')

    if search:
        docs = docs.filter(Q(title__icontains=search) | Q(document_number__icontains=search))
    if cat_id:
        docs = docs.filter(category_id=cat_id)

    categories = DocumentCategory.objects.all()
    return render(request, 'documents/library.html', {
        'documents': docs,
        'categories': categories,
        'selected_cat': cat_id,
        'search': search,
    })

@login_required
def my_documents_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    personal_docs = EmployeeDocument.objects.filter(employee=employee).select_related('category')
    company_policies = EmployeeDocument.objects.filter(is_company_wide=True).select_related('category')

    return render(request, 'documents/my_documents.html', {
        'personal_docs': personal_docs,
        'company_policies': company_policies,
    })

@login_required
@hr_or_admin_required
def document_upload_view(request):
    form = EmployeeDocumentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        doc = form.save(commit=False)
        current_emp = getattr(request.user, 'employee_profile', None)
        doc.uploaded_by = current_emp
        doc.save()
        messages.success(request, f"Document '{doc.title}' uploaded successfully.")
        return redirect('documents:library')
    return render(request, 'documents/document_form.html', {'form': form, 'title': 'Upload Corporate / Employee Document'})

@login_required
def expiring_documents_view(request):
    today = timezone.now().date()
    sixty_days = today + timezone.timedelta(days=60)
    expiring = EmployeeDocument.objects.filter(
        expiry_date__isnull=False,
        expiry_date__lte=sixty_days
    ).select_related('employee__department', 'category').order_by('expiry_date')

    return render(request, 'documents/expiring.html', {'expiring': expiring, 'today': today})
