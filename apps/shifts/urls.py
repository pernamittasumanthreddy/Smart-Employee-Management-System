from django.urls import path

from apps.shifts import views

app_name = 'shifts'

urlpatterns = [
    path('', views.shift_list_view, name='shift_list'),
    path('create/', views.shift_create_view, name='shift_create'),
    path('assign/', views.shift_assign_view, name='shift_assign'),
    path('holidays/', views.holiday_list_view, name='holiday_list'),
    path('holidays/create/', views.holiday_create_view, name='holiday_create'),
]
