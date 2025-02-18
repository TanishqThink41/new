import apiClient from './apiClient';

export const organizationService = {
    // Get all organizations
    getAll: async () => {
        const response = await apiClient.get('/organizations/');
        return response.data;
    },

    // Get organization by ID
    getById: async (id) => {
        const response = await apiClient.get(`/organizations/${id}/`);
        return response.data;
    },

    // Create new organization
    create: async (data) => {
        const response = await apiClient.post('/organizations/', data);
        return response.data;
    },

    // Update organization
    update: async (id, data) => {
        const response = await apiClient.put(`/organizations/${id}/`, data);
        return response.data;
    },

    // Delete organization
    delete: async (id) => {
        await apiClient.delete(`/organizations/${id}/`);
    },

    // Get organization's employees
    getEmployees: async (id) => {
        const response = await apiClient.get(`/organizations/${id}/employees/`);
        return response.data;
    },

    // Get organization's assignments
    getAssignments: async (id) => {
        const response = await apiClient.get(`/organizations/${id}/assignments/`);
        return response.data;
    },
};