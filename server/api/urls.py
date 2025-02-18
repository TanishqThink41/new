from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'organizations', viewsets.OrganizationViewSet)
router.register(r'employees', viewsets.EmployeeViewSet)
router.register(r'assignments', viewsets.AssignmentViewSet)
router.register(r'employee-assignments', viewsets.EmployeeAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
