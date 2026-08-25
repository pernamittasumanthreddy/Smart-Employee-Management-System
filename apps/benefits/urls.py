from django.urls import path
from apps.benefits import views

app_name = 'benefits'

urlpatterns = [
    path('', views.benefits_dashboard, name='dashboard'),
    path('policies/', views.policy_list, name='policy_list'),
    path('claims/', views.claims_list, name='claims_list'),
]
