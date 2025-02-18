from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Organization, Employee, Assignment, EmployeeAssignment
from .serializers import (
    UserSerializer, OrganizationSerializer, EmployeeSerializer,
    AssignmentSerializer, EmployeeAssignmentSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        organization = self.get_object()
        employees = Employee.objects.filter(organization=organization)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        organization = self.get_object()
        assignments = Assignment.objects.filter(organization=organization)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        employee = self.get_object()
        assignments = EmployeeAssignment.objects.filter(employee=employee)
        serializer = EmployeeAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Employee.objects.all()
        organization_id = self.request.query_params.get('organization', None)
        if organization_id is not None:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    @action(detail=True, methods=['get'])
    def assigned_employees(self, request, pk=None):
        assignment = self.get_object()
        employee_assignments = EmployeeAssignment.objects.filter(assignment=assignment)
        serializer = EmployeeAssignmentSerializer(employee_assignments, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Assignment.objects.all()
        organization_id = self.request.query_params.get('organization', None)
        status = self.request.query_params.get('status', None)
        
        if organization_id is not None:
            queryset = queryset.filter(organization_id=organization_id)
        if status is not None:
            queryset = queryset.filter(status=status)
            
        return queryset

class EmployeeAssignmentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAssignment.objects.all()
    serializer_class = EmployeeAssignmentSerializer

    def get_queryset(self):
        queryset = EmployeeAssignment.objects.all()
        employee_id = self.request.query_params.get('employee', None)
        assignment_id = self.request.query_params.get('assignment', None)
        is_completed = self.request.query_params.get('is_completed', None)
        
        if employee_id is not None:
            queryset = queryset.filter(employee_id=employee_id)
        if assignment_id is not None:
            queryset = queryset.filter(assignment_id=assignment_id)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')
            
        return queryset

    def create(self, request, *args, **kwargs):
        # Check for duplicate assignment
        employee_id = request.data.get('employee_id')
        assignment_id = request.data.get('assignment_id')
        
        if EmployeeAssignment.objects.filter(
            employee_id=employee_id,
            assignment_id=assignment_id
        ).exists():
            return Response(
                {'error': 'Employee is already assigned to this assignment'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        employee_assignment = self.get_object()
        employee_assignment.is_completed = True
        employee_assignment.save()
        serializer = self.get_serializer(employee_assignment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def evaluate(self, request, pk=None):
        employee_assignment = self.get_object()
        
        score = request.data.get('evaluation_score')
        comments = request.data.get('evaluation_comments', '')
        
        if score is None:
            return Response(
                {'error': 'Evaluation score is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            score = float(score)
            if not (0 <= score <= 5):
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Evaluation score must be a number between 0 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        employee_assignment.evaluation_score = score
        employee_assignment.evaluation_comments = comments
        employee_assignment.save()
        
        serializer = self.get_serializer(employee_assignment)
        return Response(serializer.data)
