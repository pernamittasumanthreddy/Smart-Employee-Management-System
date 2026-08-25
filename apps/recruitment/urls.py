from django.urls import path
from apps.recruitment import views

app_name = 'recruitment'

urlpatterns = [
    path('', views.recruitment_dashboard, name='dashboard'),
    path('requisitions/', views.requisition_list, name='requisition_list'),
    path('requisitions/create/', views.requisition_create, name='requisition_create'),
    path('pipeline/', views.candidate_pipeline, name='pipeline'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('offers/', views.offer_list, name='offer_list'),
]
