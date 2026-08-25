from django.urls import path

from apps.notifications import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_center_view, name='center'),
    path('<int:notif_id>/read/', views.mark_notification_read, name='mark_read'),
    path('read-all/', views.mark_all_notifications_read, name='mark_all_read'),
]
