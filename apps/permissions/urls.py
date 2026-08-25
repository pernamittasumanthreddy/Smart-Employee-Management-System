from django.urls import path

from apps.permissions import views

app_name = 'permissions'

urlpatterns = [
    path('', views.role_list, name='role_list'),
    path('roles/', views.role_list, name='roles'),
    path('matrix/<int:role_id>/', views.role_matrix, name='role_matrix'),
]
