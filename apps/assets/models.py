from django.db import models
from django.utils.translation import gettext_lazy as _


class AssetStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', _('Available in Inventory')
    ASSIGNED = 'ASSIGNED', _('Assigned to Employee')
    MAINTENANCE = 'MAINTENANCE', _('Under Maintenance')
    DAMAGED = 'DAMAGED', _('Damaged')
    LOST = 'LOST', _('Lost / Stolen')
    RETIRED = 'RETIRED', _('Retired / Disposed')

class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Asset Category')
        verbose_name_plural = _('Asset Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Asset(models.Model):
    asset_id = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.CASCADE,
        related_name='assets'
    )
    serial_number = models.CharField(max_length=100, unique=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AssetStatus.choices,
        default=AssetStatus.AVAILABLE
    )
    assigned_to = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_assets'
    )
    assigned_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')
        ordering = ['asset_id']

    def __str__(self):
        return f"[{self.asset_id}] {self.name} ({self.get_status_display()})"


class AssetHistory(models.Model):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='history'
    )
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asset_history'
    )
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Asset History')
        verbose_name_plural = _('Asset Histories')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.asset.asset_id} - {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
