import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Organization, Employee, Assignment, EmployeeAssignment

def serialize_employee(employee):
    return {
        'id': employee.id,
        'user': {
            'username': employee.user.username,
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name,
            'email': employee.user.email
        },
        'organization': {
            'id': employee.organization.id,
            'name': employee.organization.name,
            'description': employee.organization.description
        },
        'employee_type': employee.employee_type,
        'department': employee.department,
        'position': employee.position,
        'joining_date': employee.joining_date.isoformat(),
        'is_active': employee.is_active
    }

def serialize_assignment(assignment):
    return {
        'id': assignment.id,
        'title': assignment.title,
        'description': assignment.description,
        'organization': {
            'id': assignment.organization.id,
            'name': assignment.organization.name
        },
        'deadline': assignment.deadline.isoformat(),
        'status': assignment.status,
        'created_at': assignment.created_at.isoformat()
    }

def serialize_employee_assignment(ea):
    return {
        'id': ea.id,
        'employee': ea.employee_id,
        'assignment': ea.assignment_id,
        'start_time': ea.start_time.isoformat(),
        'end_time': ea.end_time.isoformat() if ea.end_time else None,
        'duration': str(ea.duration) if ea.duration else None,
        'evaluation_score': float(ea.evaluation_score) if ea.evaluation_score else None,
        'evaluation_comments': ea.evaluation_comments,
        'is_completed': ea.is_completed
    }

# Employee Views
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        data = [serialize_employee(employee) for employee in employees]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'GET':
        data = serialize_employee(employee)
        # Add assignments data
        assignments = EmployeeAssignment.objects.filter(employee=employee)
        data['assignments'] = [serialize_employee_assignment(ea) for ea in assignments]
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Assignment Views
def assignment_list(request):
    if request.method == 'GET':
        assignments = Assignment.objects.all()
        data = [serialize_assignment(assignment) for assignment in assignments]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if request.method == 'GET':
        data = serialize_assignment(assignment)
        # Add assigned employees data
        assigned_employees = EmployeeAssignment.objects.filter(assignment=assignment)
        data['assigned_employees'] = [serialize_employee_assignment(ea) for ea in assigned_employees]
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Organization Views
def organization_list(request):
    if request.method == 'GET':
        organizations = Organization.objects.all()
        data = [model_to_dict(org, fields=['id', 'name', 'description', 'address']) 
                for org in organizations]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def organization_detail(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    
    if request.method == 'GET':
        data = model_to_dict(org, fields=['id', 'name', 'description', 'address'])
        # Add employees and assignments data
        data['employees'] = [serialize_employee(emp) for emp in org.employees.all()]
        data['assignments'] = [serialize_assignment(asn) for asn in org.assignments.all()]
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

from datetime import datetime
from django.utils import timezone

# Employee Assignment Views
@csrf_exempt
def employee_assignment_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['employee_id', 'assignment_id', 'start_time']
            for field in required_fields:
                if field not in data:
                    return JsonResponse(
                        {'error': f'Missing required field: {field}'}, 
                        status=400
                    )
            
            # Validate and parse dates
            try:
                start_time = datetime.fromisoformat(data.get('start_time').replace('Z', '+00:00'))
                start_time = timezone.make_aware(start_time) if timezone.is_naive(start_time) else start_time
                
                end_time = None
                if data.get('end_time'):
                    end_time = datetime.fromisoformat(data.get('end_time').replace('Z', '+00:00'))
                    end_time = timezone.make_aware(end_time) if timezone.is_naive(end_time) else end_time
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
            
            # Check if employee and assignment exist
            try:
                employee = Employee.objects.get(id=data.get('employee_id'))
                assignment = Assignment.objects.get(id=data.get('assignment_id'))
            except (Employee.DoesNotExist, Assignment.DoesNotExist):
                return JsonResponse(
                    {'error': 'Employee or Assignment not found'}, 
                    status=404
                )
            
            # Check for duplicate assignment
            if EmployeeAssignment.objects.filter(
                employee=employee,
                assignment=assignment
            ).exists():
                return JsonResponse(
                    {'error': 'Employee is already assigned to this assignment'}, 
                    status=400
                )
            
            # Create the assignment
            ea = EmployeeAssignment.objects.create(
                employee=employee,
                assignment=assignment,
                start_time=start_time,
                end_time=end_time,
                evaluation_score=data.get('evaluation_score', None),
                evaluation_comments=data.get('evaluation_comments', ''),
                is_completed=data.get('is_completed', False)
            )
            return JsonResponse(serialize_employee_assignment(ea), status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def employee_assignment_update(request, ea_id):
    ea = get_object_or_404(EmployeeAssignment, id=ea_id)
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            if 'end_time' in data:
                ea.end_time = data['end_time']
            if 'evaluation_score' in data:
                score = float(data['evaluation_score'])
                if not (0 <= score <= 5):
                    return JsonResponse(
                        {'error': 'Evaluation score must be between 0 and 5'}, 
                        status=400
                    )
                ea.evaluation_score = score
            if 'evaluation_comments' in data:
                ea.evaluation_comments = data['evaluation_comments']
            if 'is_completed' in data:
                ea.is_completed = data['is_completed']
            
            ea.save()
            return JsonResponse(serialize_employee_assignment(ea))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
