from django.db import models
from django.utils.translation import gettext_lazy as _


class TicketPriority(models.TextChoices):
    URGENT = 'URGENT', _('Urgent')
    HIGH = 'HIGH', _('High')
    MEDIUM = 'MEDIUM', _('Medium')
    LOW = 'LOW', _('Low')

class TicketStatus(models.TextChoices):
    OPEN = 'OPEN', _('Open')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    PENDING_USER = 'PENDING_USER', _('Waiting on User')
    RESOLVED = 'RESOLVED', _('Resolved')
    CLOSED = 'CLOSED', _('Closed')

class TicketCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sla_resolution_hours = models.PositiveIntegerField(default=24, help_text="Target resolution turnaround in hours")
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Ticket Category')
        verbose_name_plural = _('Ticket Categories')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (SLA: {self.sla_resolution_hours}h)"


class SupportTicket(models.Model):
    ticket_number = models.CharField(max_length=50, unique=True, db_index=True)
    creator = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='tickets_created'
    )
    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN
    )

    def __init__(self, *args, **kwargs):
        if 'employee' in kwargs and 'creator' not in kwargs:
            kwargs['creator'] = kwargs.pop('employee')
        if 'title' in kwargs and 'subject' not in kwargs:
            kwargs['subject'] = kwargs.pop('title')
        if 'ticket_number' not in kwargs:
            import uuid
            kwargs['ticket_number'] = f"TICK-{uuid.uuid4().hex[:6].upper()}"
        super().__init__(*args, **kwargs)

    @property
    def employee(self):
        return self.creator

    @employee.setter
    def employee(self, val):
        self.creator = val

    @property
    def title(self):
        return self.subject

    @title.setter
    def title(self, val):
        self.subject = val

    assigned_to = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,

        related_name='assigned_support_tickets'
    )
    resolution_notes = models.TextField(blank=True, null=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='helpdesk/attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Support Ticket')
        verbose_name_plural = _('Support Tickets')
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.ticket_number}] {self.subject} ({self.get_status_display()})"


class TicketMessage(models.Model):
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='ticket_messages'
    )
    message = models.TextField()
    attachment = models.FileField(upload_to='helpdesk/replies/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Ticket Message')
        verbose_name_plural = _('Ticket Messages')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.full_name} on {self.ticket.ticket_number}"
