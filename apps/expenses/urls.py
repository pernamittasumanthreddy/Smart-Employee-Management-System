from django.urls import path

from apps.expenses import views

app_name = 'expenses'

urlpatterns = [
    path('', views.my_expenses_view, name='index'),
    path('my-expenses/', views.my_expenses_view, name='my_expenses'),
    path('claim/', views.claim_expense_view, name='claim'),
    path('approvals/', views.expense_approvals_view, name='approvals'),
    path('approvals/<int:claim_id>/approve/', views.approve_expense_action, name='approve'),
    path('approvals/<int:claim_id>/reject/', views.reject_expense_action, name='reject'),
    path('approvals/<int:claim_id>/reimburse/', views.reimburse_expense_action, name='reimburse'),
]
