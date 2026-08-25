from django.urls import path

from apps.performance import views

app_name = 'performance'

urlpatterns = [
    path('', views.evaluations_list_view, name='evaluation_list'),
    path('my-reviews/', views.my_performance_reviews_view, name='my_reviews'),
    path('conduct/', views.conduct_evaluation_view, name='conduct'),
    path('cycles/', views.cycle_list_view, name='cycle_list'),
]
