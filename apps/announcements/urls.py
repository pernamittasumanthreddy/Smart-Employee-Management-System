from django.urls import path

from apps.announcements import views

app_name = 'announcements'

urlpatterns = [
    path('', views.announcement_board_view, name='board'),
    path('create/', views.announcement_create_view, name='create'),
    path('events/', views.event_list_view, name='events'),
    path('events/<int:event_id>/register/', views.event_register_action, name='register_event'),
    path('workspace-calendar/', views.workspace_calendar_view, name='workspace_calendar'),
]
