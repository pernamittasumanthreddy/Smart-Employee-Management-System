from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.assets.forms import AssetAssignForm, AssetForm
from apps.assets.models import Asset, AssetCategory, AssetHistory, AssetStatus
from apps.notifications.services import NotificationService
from apps.permissions.decorators import hr_or_admin_required


@login_required
def asset_list_view(request):
    search = request.GET.get('search', '').strip()
    cat_id = request.GET.get('category')
    status = request.GET.get('status')

    assets = Asset.objects.all().select_related('category', 'assigned_to__department')

    if search:
        assets = assets.filter(Q(name__icontains=search) | Q(asset_id__icontains=search) | Q(serial_number__icontains=search))
    if cat_id:
        assets = assets.filter(category_id=cat_id)
    if status:
        assets = assets.filter(status=status)

    categories = AssetCategory.objects.all()
    total_assets = assets.count()
    assigned_count = assets.filter(status=AssetStatus.ASSIGNED).count()
    available_count = assets.filter(status=AssetStatus.AVAILABLE).count()

    return render(request, 'assets/asset_list.html', {
        'assets': assets,
        'categories': categories,
        'selected_cat': cat_id,
        'selected_status': status,
        'search': search,
        'total_assets': total_assets,
        'assigned_count': assigned_count,
        'available_count': available_count,
    })

@login_required
def my_assets_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    assets = Asset.objects.filter(assigned_to=employee).select_related('category')
    return render(request, 'assets/my_assets.html', {'assets': assets})

@login_required
def asset_detail_view(request, asset_id):
    asset = get_object_or_404(
        Asset.objects.select_related('category', 'assigned_to__department').prefetch_related('history__employee'),
        id=asset_id
    )
    assign_form = AssetAssignForm()
    return render(request, 'assets/asset_detail.html', {
        'asset': asset,
        'history': asset.history.all(),
        'assign_form': assign_form,
    })

@login_required
@hr_or_admin_required
def asset_create_view(request):
    form = AssetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        asset = form.save()
        AssetHistory.objects.create(
            asset=asset,
            action='ASSET_REGISTERED',
            notes=f"Initial asset registration into inventory (Cost: ${asset.purchase_cost})"
        )
        messages.success(request, f"Asset '{asset.name}' [{asset.asset_id}] registered successfully.")
        return redirect('assets:asset_detail', asset_id=asset.id)
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Register New Corporate Asset'})

@login_required
@hr_or_admin_required
def asset_assign_action(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetAssignForm(request.POST)
        if form.is_valid():
            emp = form.cleaned_data['employee']
            notes = form.cleaned_data['notes']
            asset.assigned_to = emp
            asset.assigned_date = timezone.now().date()
            asset.status = AssetStatus.ASSIGNED
            asset.save()

            AssetHistory.objects.create(
                asset=asset,
                employee=emp,
                action='ASSIGNED',
                notes=notes or f"Assigned to {emp.full_name}"
            )

            if emp.user:
                NotificationService.create_notification(
                    user=emp.user,
                    title="Asset Assigned",
                    message=f"Corporate asset [{asset.asset_id}] {asset.name} has been assigned to you.",
                    category='ASSET',
                    link="/assets/my-assets/"
                )

            messages.success(request, f"Asset assigned to {emp.full_name}.")
    return redirect('assets:asset_detail', asset_id=asset.id)

@login_required
@hr_or_admin_required
def asset_return_action(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    prev_emp = asset.assigned_to
    asset.assigned_to = None
    asset.assigned_date = None
    asset.status = AssetStatus.AVAILABLE
    asset.save()

    AssetHistory.objects.create(
        asset=asset,
        employee=prev_emp,
        action='RETURNED',
        notes=f"Asset returned to central inventory by {prev_emp.full_name if prev_emp else 'Staff'}"
    )

    messages.success(request, f"Asset [{asset.asset_id}] marked as returned and available in inventory.")
    return redirect('assets:asset_detail', asset_id=asset.id)
