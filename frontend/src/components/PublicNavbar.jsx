import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PublicNavbar = () => {
    const { user } = useAuth();

    return (
        <nav className="fixed w-full z-50 bg-black/20 backdrop-blur-md border-b border-white/10 transition-all duration-300">
            <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                {/* Logo */}
                <Link to="/" className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
                    TallerPro
                </Link>

                {/* Desktop Menu */}
                <div className="hidden md:flex items-center gap-8">
                    <Link to="/" className="text-gray-300 hover:text-white font-medium transition-colors text-sm">Inicio</Link>
                    <Link to="/marketplace" className="text-gray-300 hover:text-white font-medium transition-colors text-sm">Venta de Autos</Link>
                    <a href="#services" className="text-gray-300 hover:text-white font-medium transition-colors text-sm">Servicios</a>
                    <a href="#about" className="text-gray-300 hover:text-white font-medium transition-colors text-sm">Nosotros</a>
                </div>

                {/* Auth Buttons */}
                <div className="flex items-center gap-4">
                    {user ? (
                        <>
                            <span className="hidden md:inline text-gray-300 text-sm">Hola, {user.username}</span>
                            <Link
                                to={user.role === 'client' ? "/client/dashboard" : "/dashboard"}
                                className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full text-sm font-bold transition-all shadow-lg hover:shadow-blue-500/50"
                            >
                                Mi Panel
                            </Link>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="hidden md:inline text-gray-300 hover:text-white font-medium transition-colors text-sm">
                                Iniciar Sesión
                            </Link>
                            <Link
                                to="/register"
                                className="px-5 py-2 bg-white/10 hover:bg-white/20 border border-white/20 text-white rounded-full text-sm font-bold backdrop-blur-md transition-all hover:scale-105"
                            >
                                Registrarse
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default PublicNavbar;
