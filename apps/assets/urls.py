from django.urls import path

from apps.assets import views

app_name = 'assets'

urlpatterns = [
    path('', views.asset_list_view, name='asset_list'),
    path('my-assets/', views.my_assets_view, name='my_assets'),
    path('create/', views.asset_create_view, name='create'),
    path('<int:asset_id>/', views.asset_detail_view, name='asset_detail'),
    path('<int:asset_id>/assign/', views.asset_assign_action, name='assign'),
    path('<int:asset_id>/return/', views.asset_return_action, name='return'),
]
