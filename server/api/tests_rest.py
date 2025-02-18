from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
from .models import Organization, Employee, Assignment, EmployeeAssignment
import json

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        # Create test organization
        self.org = Organization.objects.create(
            name='Test Organization',
            description='Test Description',
            address='Test Address'
        )
        
        # Create test employee
        self.employee = Employee.objects.create(
            user=self.user,
            organization=self.org,
            employee_type='full_time',
            department='Engineering',
            position='Developer',
            joining_date=timezone.now().date()
        )
        
        # Create test assignment
        self.assignment = Assignment.objects.create(
            organization=self.org,
            title='Test Assignment',
            description='Test Description',
            deadline=timezone.now().date() + timedelta(days=7),
            status='pending'
        )

    def test_organization_list(self):
        """Test retrieving organization list"""
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Organization')

    def test_organization_detail(self):
        """Test retrieving organization detail"""
        url = reverse('organization-detail', args=[self.org.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Organization')

    def test_organization_create(self):
        """Test creating a new organization"""
        url = reverse('organization-list')
        data = {
            'name': 'New Organization',
            'description': 'New Description',
            'address': 'New Address'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 2)

    def test_employee_list(self):
        """Test retrieving employee list"""
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['position'], 'Developer')

    def test_employee_detail(self):
        """Test retrieving employee detail"""
        url = reverse('employee-detail', args=[self.employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['position'], 'Developer')

    def test_employee_create(self):
        """Test creating a new employee"""
        new_user = User.objects.create_user(
            username='newuser',
            password='newpass123'
        )
        url = reverse('employee-list')
        data = {
            'user_id': new_user.id,
            'organization_id': self.org.id,
            'employee_type': 'intern',
            'department': 'Marketing',
            'position': 'Manager',
            'joining_date': timezone.now().date().isoformat()
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Error response:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_assignment_list(self):
        """Test retrieving assignment list"""
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Assignment')

    def test_assignment_detail(self):
        """Test retrieving assignment detail"""
        url = reverse('assignment-detail', args=[self.assignment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Assignment')

    def test_assignment_create(self):
        """Test creating a new assignment"""
        url = reverse('assignment-list')
        data = {
            'organization_id': self.org.id,
            'title': 'New Assignment',
            'description': 'New Description',
            'deadline': (timezone.now().date() + timedelta(days=14)).isoformat(),
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 2)

    def test_employee_assignment_create(self):
        """Test creating a new employee assignment"""
        url = reverse('employeeassignment-list')
        data = {
            'employee_id': self.employee.id,
            'assignment_id': self.assignment.id,
            'start_time': timezone.now().isoformat(),
            'is_completed': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeAssignment.objects.count(), 1)

    def test_employee_assignment_duplicate(self):
        """Test creating a duplicate employee assignment"""
        # Create first assignment
        EmployeeAssignment.objects.create(
            employee=self.employee,
            assignment=self.assignment,
            start_time=timezone.now()
        )
        
        # Try to create duplicate
        url = reverse('employeeassignment-list')
        data = {
            'employee_id': self.employee.id,
            'assignment_id': self.assignment.id,
            'start_time': timezone.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EmployeeAssignment.objects.count(), 1)

    def test_employee_assignment_evaluate(self):
        """Test evaluating an employee assignment"""
        ea = EmployeeAssignment.objects.create(
            employee=self.employee,
            assignment=self.assignment,
            start_time=timezone.now()
        )
        
        url = reverse('employeeassignment-evaluate', args=[ea.id])
        data = {
            'evaluation_score': 4.5,
            'evaluation_comments': 'Good work!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['evaluation_score']), 4.5)
        self.assertEqual(response.data['evaluation_comments'], 'Good work!')

    def test_employee_assignment_invalid_score(self):
        """Test evaluating with invalid score"""
        ea = EmployeeAssignment.objects.create(
            employee=self.employee,
            assignment=self.assignment,
            start_time=timezone.now()
        )
        
        url = reverse('employeeassignment-evaluate', args=[ea.id])
        data = {
            'evaluation_score': 6,  # Invalid score > 5
            'evaluation_comments': 'Good work!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_organization_employees(self):
        """Test retrieving organization employees"""
        url = reverse('organization-employees', args=[self.org.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['position'], 'Developer')

    def test_organization_assignments(self):
        """Test retrieving organization assignments"""
        url = reverse('organization-assignments', args=[self.org.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Assignment')

    def test_employee_assignments(self):
        """Test retrieving employee assignments"""
        ea = EmployeeAssignment.objects.create(
            employee=self.employee,
            assignment=self.assignment,
            start_time=timezone.now()
        )
        
        url = reverse('employee-assignments', args=[self.employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['assignment']['title'], 'Test Assignment')
