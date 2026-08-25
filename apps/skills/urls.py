from django.urls import path

from apps.skills import views

app_name = 'skills'

urlpatterns = [
    path('catalog/', views.skill_catalog_view, name='catalog'),
    path('my-skills/', views.my_skills_view, name='my_skills'),
    path('matrix/', views.skill_matrix_view, name='matrix'),
    path('verify/<int:emp_skill_id>/', views.skill_verification_action, name='verify'),
]
