import { useParams } from 'react-router-dom';
import { employees, employeeAssignments, assignments } from '../api/mockData';
import { format } from 'date-fns';

export default function EmployeeProfile() {
  const { id } = useParams();
  const employee = employees.find(e => e.id === parseInt(id));
  const employeeAssignmentList = employeeAssignments.filter(ea => ea.employee === parseInt(id));

  if (!employee) {
    return <div>Employee not found</div>;
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
        {employeeAssignmentList.map((ea) => {
          const assignment = assignments.find(a => a.id === ea.assignment);
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
        })}
      </div>
    </div>
  );
}
