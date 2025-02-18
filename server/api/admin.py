from django.contrib import admin
from .models import Organization, Employee, Assignment, EmployeeAssignment

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'employee_type', 'department', 'position', 'joining_date', 'is_active')
    list_filter = ('organization', 'employee_type', 'department', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department', 'position')
    date_hierarchy = 'joining_date'

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'deadline', 'status', 'created_at')
    list_filter = ('organization', 'status', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'

@admin.register(EmployeeAssignment)
class EmployeeAssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'assignment', 'start_time', 'end_time', 'duration', 'evaluation_score', 'is_completed')
    list_filter = ('is_completed', 'created_at', 'employee__organization')
    search_fields = ('employee__user__username', 'assignment__title')
    date_hierarchy = 'start_time'
    readonly_fields = ('duration',)
