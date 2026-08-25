from django.urls import path

from apps.training import views

app_name = 'training'

urlpatterns = [
    path('', views.course_catalog_view, name='index'),
    path('catalog/', views.course_catalog_view, name='catalog'),
    path('my-trainings/', views.my_trainings_view, name='my_trainings'),
    path('enroll/<int:course_id>/', views.enroll_course_action, name='enroll'),
    path('create/', views.course_create_view, name='create'),
    path('expiring/', views.expiring_certifications_view, name='expiring'),
]
