import { Link } from 'react-router-dom';
import { employees } from '../api/mockData';

export default function EmployeeList() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-orange-500">Employees</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
        {/* Grid Layout Guide */}
        <div className="hidden fixed top-0 left-1/2 transform -translate-x-1/2 w-full max-w-7xl h-full pointer-events-none z-0 opacity-10">
          <div className="grid grid-cols-3 h-full gap-6">
            <div className="bg-orange-500"></div>
            <div className="bg-orange-500"></div>
            <div className="bg-orange-500"></div>
          </div>
        </div>
        {employees.map((employee) => (
          <Link
            key={employee.id}
            to={`/employees/${employee.id}`}
            className="bg-zinc-900 rounded-lg p-6 border border-orange-500/20 hover:border-orange-500 transform hover:scale-105 transition-all duration-300 hover:shadow-[0_0_15px_rgba(249,115,22,0.3)] relative z-10"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-orange-500 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-semibold transform hover:rotate-12 transition-transform duration-300">
                {employee.user.first_name[0]}
                {employee.user.last_name[0]}
              </div>
              <div>
                <h2 className="text-xl font-semibold text-orange-500">
                  {employee.user.first_name} {employee.user.last_name}
                </h2>
                <p className="text-gray-300">{employee.position}</p>
              </div>
            </div>
            <div className="mt-4">
              <p className="text-sm text-gray-400">{employee.organization.name}</p>
              <p className="text-sm text-gray-400">{employee.department}</p>
              <div className="mt-2">
                <span className={`inline-block px-2 py-1 text-xs font-semibold rounded ${
                  employee.employee_type === 'full_time' 
                    ? 'bg-orange-900/50 text-orange-400 border border-orange-500/50' 
                    : 'bg-zinc-800 text-orange-400 border border-orange-500/50'
                }`}>
                  {employee.employee_type.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
