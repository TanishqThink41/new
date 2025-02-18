import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { employeeService, employeeAssignmentService } from '../services';

export default function EmployeeProfile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [employee, setEmployee] = useState(null);
  const [employeeAssignments, setEmployeeAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEmployeeData = async () => {
      try {
        // First get employee data
        const employeeData = await employeeService.getById(id);
        setEmployee(employeeData);
        setError(null);

        // Then get assignments data using the employee's assignments endpoint
        try {
          const assignmentsData = await employeeService.getAssignments(id);
          setEmployeeAssignments(assignmentsData);
        } catch (assignmentErr) {
          console.error('Failed to fetch assignments:', assignmentErr);
          // Don't set error here, just show empty assignments
          setEmployeeAssignments([]);
        }
      } catch (err) {
        console.error('Failed to fetch employee data:', err);
        setError('Failed to load employee data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchEmployeeData();
  }, [id]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-orange-500 mx-auto"></div>
        <p className="text-orange-500 mt-4">Loading employee data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <p className="text-red-500">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!employee) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <p className="text-orange-500">Employee not found</p>
        <button 
          onClick={() => navigate('/employees')} 
          className="mt-4 px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors"
        >
          Back to Employees
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 text-gray-300">
      {/* Profile Header */}
      <div className="bg-zinc-900 rounded-lg p-6 mb-8 border border-orange-500/20 hover:border-orange-500 transition-all duration-300 hover:shadow-[0_0_15px_rgba(249,115,22,0.3)]">

        <div className="flex items-center space-x-6">
          <div className="bg-orange-500 text-white rounded-full w-20 h-20 flex items-center justify-center text-3xl font-semibold transform hover:rotate-12 transition-transform duration-300 hover:scale-110">
            {employee.user.first_name[0]}
            {employee.user.last_name[0]}
          </div>
          <div>
            <h1 className="text-3xl font-bold text-orange-500">
              {employee.user.first_name} {employee.user.last_name}
            </h1>
            <p className="text-xl text-gray-300">{employee.position}</p>
            <div className="mt-2 space-y-1">
              <p className="text-gray-400">{employee.organization.name}</p>
              <p className="text-gray-400">{employee.department}</p>
              <span className={`inline-block px-3 py-1 text-sm font-semibold rounded ${
                employee.employee_type === 'full_time' 
                  ? 'bg-orange-900/50 text-orange-400 border border-orange-500/50' 
                  : 'bg-zinc-800 text-orange-400 border border-orange-500/50'
              }`}>
                {employee.employee_type.replace('_', ' ').toUpperCase()}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Assignments Section */}
      <h2 className="text-2xl font-bold text-orange-500 mb-6">Assignments</h2>
      <div className="space-y-6">
        {employeeAssignments.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-400">No assignments found for this employee.</p>
          </div>
        ) : (
          employeeAssignments.map((ea) => {
            const assignment = ea.assignment;
            return (
            <div key={ea.id} className="bg-zinc-900 rounded-lg p-6 border border-orange-500/20 hover:border-orange-500 transform hover:scale-[1.02] transition-all duration-300 hover:shadow-[0_0_15px_rgba(249,115,22,0.3)]">

              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-orange-500">{assignment.title}</h3>
                <span className={`inline-block px-3 py-1 text-sm font-semibold rounded ${
                  ea.is_completed ? 'bg-orange-900/50 text-orange-400 border border-orange-500/50' : 'bg-zinc-800 text-orange-400 border border-orange-500/50'
                }`}>
                  {ea.is_completed ? 'COMPLETED' : 'IN PROGRESS'}
                </span>
              </div>
              <p className="text-gray-300 mb-4">{assignment.description}</p>
              
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-400">Start Date</p>
                  <p className="font-medium">{format(new Date(ea.start_time), 'PPP')}</p>
                </div>
                {ea.end_time && (
                  <div>
                    <p className="text-sm text-gray-400">End Date</p>
                    <p className="font-medium">{format(new Date(ea.end_time), 'PPP')}</p>
                  </div>
                )}
              </div>

              {ea.evaluation_score && (
                <div className="border-t pt-4">
                  <div className="flex items-center mb-2">
                    <p className="text-sm text-gray-400 mr-2">Evaluation Score:</p>
                    <div className="flex items-center">
                      <span className="text-lg font-semibold text-orange-500">{ea.evaluation_score}</span>
                      <span className="text-gray-400 text-sm">/5.0</span>
                    </div>
                  </div>
                  {ea.evaluation_comments && (
                    <p className="text-gray-400 text-sm italic">"{ea.evaluation_comments}"</p>
                  )}
                </div>
              )}
            </div>
          );
          })
        )}
      </div>
    </div>
  );
}
