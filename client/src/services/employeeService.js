import apiClient from './apiClient';

export const employeeService = {
    // Get all employees
    getAll: async (organizationId = null) => {
        const params = organizationId ? { organization: organizationId } : {};
        const response = await apiClient.get('/employees/', { params });
        return response.data;
    },

    // Get employee by ID
    getById: async (id) => {
        const response = await apiClient.get(`/employees/${id}/`);
        return response.data;
    },

    // Create new employee
    create: async (data) => {
        const response = await apiClient.post('/employees/', data);
        return response.data;
    },

    // Update employee
    update: async (id, data) => {
        const response = await apiClient.put(`/employees/${id}/`, data);
        return response.data;
    },

    // Delete employee
    delete: async (id) => {
        await apiClient.delete(`/employees/${id}/`);
    },

    // Get employee's assignments
    getAssignments: async (id) => {
        const response = await apiClient.get(`/employees/${id}/assignments/`);
        return response.data;
    },
};