from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Organization, Employee, Assignment, EmployeeAssignment
import json

class APITestCase(TestCase):
    def setUp(self):
        # Create test client
        self.client = Client()

        # Create test organization
        self.org = Organization.objects.create(
            name='Test Corp',
            description='Test Description',
            address='123 Test St'
        )

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
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

        # Create test employee assignment
        self.employee_assignment = EmployeeAssignment.objects.create(
            employee=self.employee,
            assignment=self.assignment,
            start_time=timezone.now(),
            is_completed=False
        )

    def test_organization_list(self):
        url = reverse('organization-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Corp')

    def test_organization_detail(self):
        url = reverse('organization-detail', args=[self.org.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'Test Corp')
        self.assertTrue('employees' in data)
        self.assertTrue('assignments' in data)

    def test_organization_detail_not_found(self):
        url = reverse('organization-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_employee_list(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['user']['username'], 'testuser')

    def test_employee_detail(self):
        url = reverse('employee-detail', args=[self.employee.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['user']['username'], 'testuser')
        self.assertTrue('assignments' in data)

    def test_employee_detail_not_found(self):
        url = reverse('employee-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_assignment_list(self):
        url = reverse('assignment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Assignment')

    def test_assignment_detail(self):
        url = reverse('assignment-detail', args=[self.assignment.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Test Assignment')
        self.assertTrue('assigned_employees' in data)

    def test_assignment_detail_not_found(self):
        url = reverse('assignment-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_employee_assignment_create(self):
        # Create a new assignment for this test
        new_assignment = Assignment.objects.create(
            organization=self.org,
            title='New Test Assignment',
            description='New Test Description',
            deadline=timezone.now().date() + timedelta(days=7),
            status='pending'
        )
        
        url = reverse('employee-assignment-create')
        current_time = timezone.now()
        data = {
            'employee_id': self.employee.id,
            'assignment_id': new_assignment.id,
            'start_time': current_time.isoformat(),
            'is_completed': False
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        if response.status_code != 201:
            print('Error response:', response.content.decode())
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['employee'], self.employee.id)
        self.assertEqual(response_data['assignment'], new_assignment.id)

    def test_employee_assignment_create_invalid_data(self):
        url = reverse('employee-assignment-create')
        data = {
            'employee_id': 999,  # Invalid ID
            'assignment_id': self.assignment.id,
            'start_time': timezone.now().isoformat()
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_employee_assignment_update(self):
        url = reverse('employee-assignment-update', args=[self.employee_assignment.id])
        data = {
            'is_completed': True,
            'evaluation_score': 4.5,
            'evaluation_comments': 'Great work!'
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['is_completed'])
        self.assertEqual(float(response_data['evaluation_score']), 4.5)
        self.assertEqual(response_data['evaluation_comments'], 'Great work!')

    def test_employee_assignment_update_not_found(self):
        url = reverse('employee-assignment-update', args=[999])
        data = {'is_completed': True}
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_employee_assignment_update_invalid_score(self):
        url = reverse('employee-assignment-update', args=[self.employee_assignment.id])
        data = {'evaluation_score': 6.0}  # Invalid score > 5.0
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

class EdgeCaseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.org = Organization.objects.create(name='Test Corp')
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.employee = Employee.objects.create(
            user=self.user,
            organization=self.org,
            employee_type='full_time',
            joining_date=timezone.now().date()
        )

    def test_empty_lists(self):
        # Test empty assignment list
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_malformed_json(self):
        # Test malformed JSON in POST request
        url = reverse('employee-assignment-create')
        response = self.client.post(
            url,
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_required_fields(self):
        # Test missing required fields in employee assignment creation
        url = reverse('employee-assignment-create')
        data = {'employee_id': self.employee.id}  # Missing assignment_id
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_date_formats(self):
        # Test invalid date format in employee assignment creation
        url = reverse('employee-assignment-create')
        data = {
            'employee_id': self.employee.id,
            'assignment_id': 1,
            'start_time': 'invalid-date'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_assignment(self):
        # Test assigning same assignment to employee twice
        assignment = Assignment.objects.create(
            organization=self.org,
            title='Test',
            deadline=timezone.now().date()
        )
        
        # Create first assignment
        EmployeeAssignment.objects.create(
            employee=self.employee,
            assignment=assignment,
            start_time=timezone.now()
        )
        
        # Try to create duplicate assignment
        url = reverse('employee-assignment-create')
        data = {
            'employee_id': self.employee.id,
            'assignment_id': assignment.id,
            'start_time': timezone.now().isoformat()
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
