from django.urls import path
from . import views

urlpatterns = [
    # Organization URLs
    path('organizations/', views.organization_list, name='organization-list'),
    path('organizations/<int:org_id>/', views.organization_detail, name='organization-detail'),
    
    # Employee URLs
    path('employees/', views.employee_list, name='employee-list'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee-detail'),
    
    # Assignment URLs
    path('assignments/', views.assignment_list, name='assignment-list'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment-detail'),
    
    # Employee Assignment URLs
    path('employee-assignments/create/', views.employee_assignment_create, name='employee-assignment-create'),
    path('employee-assignments/<int:ea_id>/update/', views.employee_assignment_update, name='employee-assignment-update'),
]
