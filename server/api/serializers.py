from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Organization, Employee, Assignment, EmployeeAssignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'address']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source='organization',
        write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'user_id', 'organization', 'organization_id',
            'employee_type', 'department', 'position', 'joining_date',
            'is_active'
        ]

class AssignmentSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source='organization',
        write_only=True
    )

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'organization', 'organization_id',
            'deadline', 'status', 'created_at'
        ]

class EmployeeAssignmentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )
    assignment_id = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all(),
        source='assignment',
        write_only=True
    )

    class Meta:
        model = EmployeeAssignment
        fields = [
            'id', 'employee', 'employee_id', 'assignment', 'assignment_id',
            'start_time', 'end_time', 'duration', 'evaluation_score',
            'evaluation_comments', 'is_completed'
        ]
        read_only_fields = ['duration']

    def validate_evaluation_score(self, value):
        if value is not None and not (0 <= value <= 5):
            raise serializers.ValidationError(
                'Evaluation score must be between 0 and 5'
            )
        return value
