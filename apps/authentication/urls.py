from django.urls import path

from apps.authentication import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('password-reset/', views.password_reset_request_view, name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('login-history/', views.login_history_view, name='login_history'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/toggle-status/', views.user_toggle_status_view, name='user_toggle_status'),
]
