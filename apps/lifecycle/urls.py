from django.urls import path
from apps.lifecycle import views

app_name = 'lifecycle'

urlpatterns = [
    path('', views.lifecycle_dashboard, name='dashboard'),
    path('onboarding/', views.onboarding_list, name='onboarding_list'),
    path('onboarding/<int:pk>/', views.onboarding_detail, name='onboarding_detail'),
    path('resignations/', views.resignation_list, name='resignation_list'),
    path('resignations/<int:pk>/', views.resignation_detail, name='resignation_detail'),
    path('certificates/<int:pk>/', views.certificate_view, name='certificate_view'),
]
