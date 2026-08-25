from django.urls import path

from apps.insights import views

app_name = 'insights'

urlpatterns = [
    path('', views.smart_insights_dashboard_view, name='dashboard'),
    path('trigger/', views.trigger_analysis_action, name='trigger_analysis'),
    path('<int:insight_id>/dismiss/', views.dismiss_insight_action, name='dismiss'),
]
