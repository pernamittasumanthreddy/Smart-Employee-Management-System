from django.urls import path

from apps.helpdesk import views

app_name = 'helpdesk'

urlpatterns = [
    path('', views.ticket_list_view, name='ticket_list'),
    path('my-tickets/', views.my_tickets_view, name='my_tickets'),
    path('create/', views.ticket_create_view, name='create'),
    path('<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('<int:ticket_id>/reply/', views.ticket_add_message, name='add_message'),
    path('<int:ticket_id>/resolve/', views.ticket_resolve_action, name='resolve'),
]
