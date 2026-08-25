from django.urls import path

from apps.recognition import views

app_name = 'recognition'

urlpatterns = [
    path('', views.recognition_wall_view, name='wall'),
    path('send/', views.send_recognition_view, name='send'),
    path('leaderboard/', views.recognition_leaderboard_view, name='leaderboard'),
]
