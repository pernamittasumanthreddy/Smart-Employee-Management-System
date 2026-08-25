from django.urls import path
from apps.workplace import views

app_name = 'workplace'

urlpatterns = [
    path('', views.workplace_dashboard, name='dashboard'),
    path('travel/', views.travel_list, name='travel_list'),
    path('desks/', views.desk_booking_portal, name='desk_booking'),
]
