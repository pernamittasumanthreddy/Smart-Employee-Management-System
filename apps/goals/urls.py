from django.urls import path

from apps.goals import views

app_name = 'goals'

urlpatterns = [
    path('', views.goal_list_view, name='goal_list'),
    path('my-goals/', views.my_goals_view, name='my_goals'),
    path('create/', views.goal_create_view, name='goal_create'),
    path('<int:goal_id>/', views.goal_detail_view, name='goal_detail'),
]
