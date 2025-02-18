import apiClient from './apiClient';

export const employeeAssignmentService = {
    // Get all employee assignments
    getAll: async (params = {}) => {
        const response = await apiClient.get('/employee-assignments/', { params });
        return response.data;
    },

    // Get employee assignment by ID
    getById: async (id) => {
        const response = await apiClient.get(`/employee-assignments/${id}/`);
        return response.data;
    },

    // Create new employee assignment
    create: async (data) => {
        const response = await apiClient.post('/employee-assignments/', data);
        return response.data;
    },

    // Update employee assignment
    update: async (id, data) => {
        const response = await apiClient.put(`/employee-assignments/${id}/`, data);
        return response.data;
    },

    // Delete employee assignment
    delete: async (id) => {
        await apiClient.delete(`/employee-assignments/${id}/`);
    },

    // Mark assignment as complete
    complete: async (id) => {
        const response = await apiClient.post(`/employee-assignments/${id}/complete/`);
        return response.data;
    },

    // Evaluate assignment
    evaluate: async (id, { evaluationScore, evaluationComments }) => {
        const response = await apiClient.post(`/employee-assignments/${id}/evaluate/`, {
            evaluation_score: evaluationScore,
            evaluation_comments: evaluationComments,
        });
        return response.data;
    },

    // Filter assignments
    getFiltered: async ({ employeeId, assignmentId, isCompleted }) => {
        const params = {};
        if (employeeId) params.employee = employeeId;
        if (assignmentId) params.assignment = assignmentId;
        if (isCompleted !== undefined) params.is_completed = isCompleted;
        return await this.getAll(params);
    },
};