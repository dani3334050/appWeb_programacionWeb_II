import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import RegisterPage from './pages/RegisterPage';
import LandingPage from './pages/LandingPage';
import Marketplace from './pages/Marketplace';
import Dashboard from './pages/Dashboard';
import ClientsPage from './pages/ClientsPage';
import OrdersPage from './pages/OrdersPage';
import CreateOrderPage from './pages/CreateOrderPage';
import OrderDetailPage from './pages/OrderDetailPage';
import ServicesPage from './pages/ServicesPage';
import PaymentsPage from './pages/PaymentsPage';
import MainLayout from './layouts/MainLayout';

import TechniciansPage from './pages/TechniciansPage'; // Import TechniciansPage
import ChatWidget from './components/ChatWidget'; // Import ChatWidget
// import PropTypes from 'prop-types'; // Unused in this file currently

const PrivateRoute = () => {
    const { user, loading } = useAuth();

    if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">Cargando...</div>;
    return user ? <Outlet /> : <Navigate to="/login" />;
};

function App() {
    return (
        <AuthProvider>
            <Router>
                <ChatWidget />
                <Routes>
                    {/* Public Routes */}
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/marketplace" element={<Marketplace />} />

                    {/* Protected Routes */}
                    <Route element={<PrivateRoute />}>

                        <Route element={<MainLayout />}>
                            {/* Dashboard moved to /dashboard to avoid conflict with Landing Page */}
                            <Route path="/dashboard" element={<Dashboard />} />

                            <Route path="/technicians" element={<TechniciansPage />} />

                            <Route path="/clients" element={<ClientsPage />} />
                            <Route path="/orders" element={<OrdersPage />} />
                            <Route path="/orders/new" element={<CreateOrderPage />} />
                            <Route path="/orders/:id" element={<OrderDetailPage />} />
                            <Route path="/services" element={<ServicesPage />} />
                            <Route path="/payments" element={<PaymentsPage />} />
                        </Route>
                    </Route>

                    {/* Fallback for unknown routes */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;
