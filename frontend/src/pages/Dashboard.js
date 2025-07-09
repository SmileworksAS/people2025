import { Link } from 'react-router-dom';

function Dashboard() {
  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Orbdent Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/chat" className="bg-blue-500 text-white p-4 rounded-lg text-center hover:bg-blue-600">
          Chat
        </Link>
        <Link to="/calendar" className="bg-blue-500 text-white p-4 rounded-lg text-center hover:bg-blue-600">
          Calendar
        </Link>
        <Link to="/news" className="bg-blue-500 text-white p-4 rounded-lg text-center hover:bg-blue-600">
          News Feed
        </Link>
      </div>
    </div>
  );
}

export default Dashboard;
