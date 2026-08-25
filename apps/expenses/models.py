from django.db import models
from django.utils.translation import gettext_lazy as _


class ExpenseStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending Approval')
    APPROVED = 'APPROVED', _('Approved')
    REJECTED = 'REJECTED', _('Rejected')
    REIMBURSED = 'REIMBURSED', _('Reimbursed / Paid')

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Expense Category')
        verbose_name_plural = _('Expense Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class ExpenseClaim(models.Model):
    claim_number = models.CharField(max_length=50, unique=True, db_index=True)
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        related_name='claims'
    )
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    expense_date = models.DateField()
    description = models.TextField()
    receipt_file = models.FileField(upload_to='expenses/receipts/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ExpenseStatus.choices,
        default=ExpenseStatus.PENDING
    )
    reviewed_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_expenses'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Expense Claim')
        verbose_name_plural = _('Expense Claims')
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.claim_number}] {self.employee.full_name} - ${self.amount} ({self.get_status_display()})"
