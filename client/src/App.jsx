import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import EmployeeList from './pages/EmployeeList';
import AssignmentList from './pages/AssignmentList';
import EmployeeProfile from './pages/EmployeeProfile';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black">
        <Navbar />
        <main className="py-4">
          <Routes>
            <Route path="/" element={<EmployeeList />} />
            <Route path="/assignments" element={<AssignmentList />} />
            <Route path="/employees/:id" element={<EmployeeProfile />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
