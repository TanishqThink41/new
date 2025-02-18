import apiClient from './apiClient';

export const assignmentService = {
    // Get all assignments
    getAll: async (params = {}) => {
        const response = await apiClient.get('/assignments/', { params });
        return response.data;
    },

    // Get assignment by ID
    getById: async (id) => {
        const response = await apiClient.get(`/assignments/${id}/`);
        return response.data;
    },

    // Create new assignment
    create: async (data) => {
        const response = await apiClient.post('/assignments/', data);
        return response.data;
    },

    // Update assignment
    update: async (id, data) => {
        const response = await apiClient.put(`/assignments/${id}/`, data);
        return response.data;
    },

    // Delete assignment
    delete: async (id) => {
        await apiClient.delete(`/assignments/${id}/`);
    },

    // Get assigned employees for an assignment
    getAssignedEmployees: async (id) => {
        const response = await apiClient.get(`/assignments/${id}/assigned_employees/`);
        return response.data;
    },

    // Filter assignments by organization and status
    getFiltered: async ({ organizationId, status }) => {
        const params = {};
        if (organizationId) params.organization = organizationId;
        if (status) params.status = status;
        return await this.getAll(params);
    },
};