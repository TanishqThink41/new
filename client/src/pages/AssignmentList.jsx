import { assignments } from '../api/mockData';
import { format } from 'date-fns';

const getStatusColor = (status) => {
  switch (status) {
    case 'completed':
      return 'bg-orange-900/50 text-orange-400 border border-orange-500/50';
    case 'in_progress':
      return 'bg-zinc-800 text-orange-400 border border-orange-500/50';
    case 'pending':
      return 'bg-black text-orange-400 border border-orange-500/50';
    default:
      return 'bg-zinc-900 text-orange-400 border border-orange-500/50';
  }
};

export default function AssignmentList() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-orange-500">Assignments</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
        {/* Grid Layout Guide */}
        <div className="hidden fixed top-0 left-1/2 transform -translate-x-1/2 w-full max-w-7xl h-full pointer-events-none z-0 opacity-10">
          <div className="grid grid-cols-3 h-full gap-6">
            <div className="bg-orange-500"></div>
            <div className="bg-orange-500"></div>
            <div className="bg-orange-500"></div>
          </div>
        </div>
        {assignments.map((assignment) => (
          <div key={assignment.id} className="bg-zinc-900 rounded-lg p-6 border border-orange-500/20 hover:border-orange-500 transform hover:scale-105 transition-all duration-300 hover:shadow-[0_0_15px_rgba(249,115,22,0.3)] relative z-10">
            <div className="flex justify-between items-start">
              <h2 className="text-xl font-semibold text-orange-500 mb-2">
                {assignment.title}
              </h2>
              <span className={`inline-block px-2 py-1 text-xs font-semibold rounded ${getStatusColor(assignment.status)}`}>
                {assignment.status.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            <p className="text-gray-300 mb-4">{assignment.description}</p>
            <div className="border-t pt-4">
              <p className="text-sm text-gray-400">
                Organization: {assignment.organization.name}
              </p>
              <p className="text-sm text-gray-400">
                Deadline: {format(new Date(assignment.deadline), 'PPP')}
              </p>
              <p className="text-sm text-gray-400">
                Created: {format(new Date(assignment.created_at), 'PPP')}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
