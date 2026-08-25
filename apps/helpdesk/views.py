import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.helpdesk.forms import SupportTicketForm, TicketMessageForm, TicketResolveForm
from apps.helpdesk.models import (
    SupportTicket,
    TicketCategory,
    TicketStatus,
)
from apps.notifications.services import NotificationService


@login_required
def ticket_list_view(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status')
    cat_id = request.GET.get('category')

    tickets = SupportTicket.objects.all().select_related('creator__department', 'category', 'assigned_to')

    if search:
        tickets = tickets.filter(Q(subject__icontains=search) | Q(ticket_number__icontains=search))
    if status:
        tickets = tickets.filter(status=status)
    if cat_id:
        tickets = tickets.filter(category_id=cat_id)

    categories = TicketCategory.objects.all()
    open_count = tickets.filter(status=TicketStatus.OPEN).count()
    in_progress = tickets.filter(status=TicketStatus.IN_PROGRESS).count()
    resolved = tickets.filter(status=TicketStatus.RESOLVED).count()

    return render(request, 'helpdesk/ticket_list.html', {
        'tickets': tickets,
        'categories': categories,
        'selected_status': status,
        'selected_cat': cat_id,
        'search': search,
        'open_count': open_count,
        'in_progress': in_progress,
        'resolved': resolved,
    })

@login_required
def my_tickets_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    tickets = SupportTicket.objects.filter(creator=employee).select_related('category', 'assigned_to')
    return render(request, 'helpdesk/my_tickets.html', {'tickets': tickets})

@login_required
def ticket_create_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    form = SupportTicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.creator = employee
        ticket.ticket_number = f"TICK-{timezone.now().year}-{secrets.token_hex(2).upper()}"
        ticket.save()
        messages.success(request, f"Support ticket [{ticket.ticket_number}] created.")
        return redirect('helpdesk:ticket_detail', ticket_id=ticket.id)

    return render(request, 'helpdesk/ticket_form.html', {'form': form, 'title': 'Create Support Ticket'})

@login_required
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(
        SupportTicket.objects.select_related('creator__department', 'category', 'assigned_to').prefetch_related('messages__sender'),
        id=ticket_id
    )
    message_form = TicketMessageForm()
    resolve_form = TicketResolveForm()

    return render(request, 'helpdesk/ticket_detail.html', {
        'ticket': ticket,
        'messages_list': ticket.messages.all(),
        'message_form': message_form,
        'resolve_form': resolve_form,
    })

@login_required
def ticket_add_message(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    sender = getattr(request.user, 'employee_profile', None)
    if request.method == 'POST' and sender:
        form = TicketMessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ticket = ticket
            msg.sender = sender
            msg.save()
            
            # If user replied, mark in progress; if admin replied, notify user
            if sender == ticket.creator:
                if ticket.status == TicketStatus.PENDING_USER:
                    ticket.status = TicketStatus.IN_PROGRESS
                    ticket.save()
            else:
                if ticket.creator.user:
                    NotificationService.create_notification(
                        user=ticket.creator.user,
                        title="Helpdesk Ticket Update",
                        message=f"New response on ticket [{ticket.ticket_number}]: {ticket.subject}",
                        category='HELP',
                        link=f"/helpdesk/{ticket.id}/"
                    )

            messages.success(request, "Message posted to ticket.")
    return redirect('helpdesk:ticket_detail', ticket_id=ticket.id)

@login_required
def ticket_resolve_action(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if request.method == 'POST':
        form = TicketResolveForm(request.POST)
        if form.is_valid():
            ticket.status = TicketStatus.RESOLVED
            ticket.resolution_notes = form.cleaned_data['resolution_notes']
            ticket.resolved_at = timezone.now()
            ticket.save()

            if ticket.creator.user:
                NotificationService.create_notification(
                    user=ticket.creator.user,
                    title="Ticket Resolved",
                    message=f"Your ticket [{ticket.ticket_number}] has been resolved.",
                    category='HELP',
                    link=f"/helpdesk/{ticket.id}/"
                )

            messages.success(request, f"Ticket [{ticket.ticket_number}] marked as resolved.")
    return redirect('helpdesk:ticket_detail', ticket_id=ticket.id)
