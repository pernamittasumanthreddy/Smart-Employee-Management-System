from django.urls import path
from apps.surveys import views

app_name = 'surveys'

urlpatterns = [
    path('', views.survey_dashboard, name='dashboard'),
    path('<int:pk>/', views.survey_detail, name='survey_detail'),
]
