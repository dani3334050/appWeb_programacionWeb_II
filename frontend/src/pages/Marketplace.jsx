import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import MarketplaceModal from '../components/MarketplaceModal';
import PublicNavbar from '../components/PublicNavbar';

const Marketplace = () => {
    const { user } = useAuth();
    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        fetchListings();
    }, []);

    const fetchListings = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/marketplace/');
            if (response.ok) {
                const data = await response.json();
                setListings(data);
            }
        } catch (error) {
            console.error("Error fetching listings:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white">
            <PublicNavbar />

            {/* Hero / Header (With top padding to account for fixed navbar) */}
            <div className="bg-gradient-to-r from-blue-900 to-gray-900 pt-32 pb-12 px-4 text-center">
                <h1 className="text-4xl md:text-5xl font-bold mb-4">Encuentra tu próximo vehículo</h1>
                <p className="text-xl text-gray-300 max-w-2xl mx-auto">
                    Explora nuestra selección de autos verificados o publica el tuyo en minutos.
                </p>
            </div>

            {/* Main Content */}
            <main className="container mx-auto p-6">
                {loading ? (
                    <div className="text-center py-10">Cargando anuncios...</div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {listings.length > 0 ? (
                            listings.map((car) => (
                                <div key={car.id} className="bg-gray-800 rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                                    <div className="h-56 bg-gray-700 relative overflow-hidden group">
                                        {car.image_url ? (
                                            <img src={car.image_url} alt={car.title} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center text-gray-500 bg-gray-800">
                                                <span className="text-4xl opacity-20">🚗</span>
                                            </div>
                                        )}
                                        <div className="absolute top-3 right-3 bg-black/70 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-white border border-white/10">
                                            {car.year}
                                        </div>
                                    </div>
                                    <div className="p-6">
                                        <div className="flex justify-between items-start mb-3">
                                            <div>
                                                <h3 className="text-lg font-bold text-white line-clamp-1">{car.brand} {car.model}</h3>
                                                <p className="text-gray-400 text-xs">{car.title}</p>
                                            </div>
                                            <span className="text-green-400 font-bold text-xl">${car.price.toLocaleString()}</span>
                                        </div>
                                        <p className="text-gray-400 text-sm mb-6 line-clamp-2 h-10">{car.description}</p>

                                        <div className="grid grid-cols-2 gap-2 mt-auto">
                                            <button className="w-full py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm font-medium transition-colors">
                                                Ver Detalles
                                            </button>
                                            <button className="w-full py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors">
                                                Contactar
                                            </button>
                                        </div>
                                        <div className="mt-4 pt-3 border-t border-gray-700 flex justify-between items-center text-xs text-gray-500">
                                            <span>Vendedor: {car.seller_name}</span>
                                            <span>Hace instantes</span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="col-span-full text-center py-20">
                                <p className="text-2xl text-gray-600 font-bold mb-2">No hay autos publicados aún</p>
                                <p className="text-gray-500">Sé el primero en vender tu auto hoy.</p>
                                {user && (
                                    <button onClick={() => setIsModalOpen(true)} className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg">
                                        Publicar Auto
                                    </button>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </main>

            {isModalOpen && user && (
                <MarketplaceModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onRefresh={fetchListings} />
            )}
        </div>
    );
};

export default Marketplace;
