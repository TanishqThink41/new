export const employees = [
  {
    id: 1,
    user: {
      username: "john.doe",
      first_name: "John",
      last_name: "Doe",
      email: "john.doe@example.com"
    },
    organization: {
      id: 1,
      name: "Tech Innovators Inc.",
      description: "Leading technology innovation company"
    },
    employee_type: "full_time",
    department: "Engineering",
    position: "Senior Developer",
    joining_date: "2025-01-01",
    is_active: true
  },
  {
    id: 2,
    user: {
      username: "jane.smith",
      first_name: "Jane",
      last_name: "Smith",
      email: "jane.smith@example.com"
    },
    organization: {
      id: 1,
      name: "Tech Innovators Inc.",
      description: "Leading technology innovation company"
    },
    employee_type: "intern",
    department: "Engineering",
    position: "Junior Developer",
    joining_date: "2025-01-02",
    is_active: true
  },
  {
    id: 3,
    user: {
      username: "bob.wilson",
      first_name: "Bob",
      last_name: "Wilson",
      email: "bob.wilson@example.com"
    },
    organization: {
      id: 2,
      name: "Digital Solutions Ltd.",
      description: "Digital transformation consultancy"
    },
    employee_type: "full_time",
    department: "Design",
    position: "UI/UX Designer",
    joining_date: "2025-01-03",
    is_active: true
  }
];

export const assignments = [
  {
    id: 1,
    title: "Develop New API Features",
    description: "Implement REST API endpoints for the new client portal",
    organization: {
      id: 1,
      name: "Tech Innovators Inc."
    },
    deadline: "2025-03-01T00:00:00Z",
    status: "in_progress",
    created_at: "2025-01-15T00:00:00Z"
  },
  {
    id: 2,
    title: "Mobile App UI Design",
    description: "Create UI/UX design for the new mobile application",
    organization: {
      id: 2,
      name: "Digital Solutions Ltd."
    },
    deadline: "2025-02-28T00:00:00Z",
    status: "pending",
    created_at: "2025-01-16T00:00:00Z"
  },
  {
    id: 3,
    title: "Database Optimization",
    description: "Optimize database queries for better performance",
    organization: {
      id: 1,
      name: "Tech Innovators Inc."
    },
    deadline: "2025-02-15T00:00:00Z",
    status: "completed",
    created_at: "2025-01-17T00:00:00Z"
  }
];

export const employeeAssignments = [
  {
    id: 1,
    employee: 1,
    assignment: 1,
    start_time: "2025-01-15T09:00:00Z",
    end_time: null,
    duration: null,
    evaluation_score: 4.5,
    evaluation_comments: "Excellent progress on API implementation",
    is_completed: false
  },
  {
    id: 2,
    employee: 2,
    assignment: 1,
    start_time: "2025-01-15T09:00:00Z",
    end_time: "2025-01-20T17:00:00Z",
    duration: "5 days",
    evaluation_score: 4.0,
    evaluation_comments: "Good work on documentation",
    is_completed: true
  },
  {
    id: 3,
    employee: 3,
    assignment: 2,
    start_time: "2025-01-16T10:00:00Z",
    end_time: null,
    duration: null,
    evaluation_score: null,
    evaluation_comments: "",
    is_completed: false
  }
];
