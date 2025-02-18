import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'bg-blue-700' : '';
  };

  return (
    <nav className="bg-orange-600 p-4 shadow-lg">
      <div className="container mx-auto">
        <div className="flex space-x-4">
          <Link
            to="/"
            className={`text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-orange-700 hover:scale-105 transform transition-all duration-200 ${isActive('/') ? 'bg-orange-700' : ''}`}
          >
            Employees
          </Link>
          <Link
            to="/assignments"
            className={`text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-orange-700 hover:scale-105 transform transition-all duration-200 ${isActive('/assignments') ? 'bg-orange-700' : ''}`}
          >
            Assignments
          </Link>
        </div>
      </div>
    </nav>
  );
}
