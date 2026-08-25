from django.urls import path

from apps.documents import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_library_view, name='library'),
    path('my-documents/', views.my_documents_view, name='my_documents'),
    path('upload/', views.document_upload_view, name='upload'),
    path('expiring/', views.expiring_documents_view, name='expiring'),
]
