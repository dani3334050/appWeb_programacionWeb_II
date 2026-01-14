import { useState, useEffect } from 'react';
import { Search, Filter, Download, Plus, Eye, Edit2, Trash2 } from 'lucide-react';
import VehicleModal from '../components/VehicleModal';
import vehicleService from '../services/vehicle.service';

const StatusBadge = ({ status }) => {
    // Definir estados base o fallback
    const styles = {
        'En reparación': 'bg-orange-100 text-orange-700 border-orange-200',
        'Listo': 'bg-green-100 text-green-700 border-green-200',
        'En taller': 'bg-yellow-100 text-yellow-700 border-yellow-200',
        'Entregado': 'bg-gray-100 text-gray-700 border-gray-200',
    };
    // Mapeo simple de estados si vinieran diferente de API, o usar default
    const defaultStyle = 'bg-gray-100 text-gray-600';

    return (
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${styles[status] || defaultStyle}`}>
            {status || 'Sin Estado'}
        </span>
    );
};

const Dashboard = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [vehicles, setVehicles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedVehicle, setSelectedVehicle] = useState(null);

    const fetchVehicles = async () => {
        try {
            setLoading(true);
            const data = await vehicleService.getAllVehicles();
            setVehicles(data);
        } catch (error) {
            console.error("Error fetching vehicles:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchVehicles();
    }, []);

    const handleCreateClick = () => {
        setSelectedVehicle(null);
        setIsModalOpen(true);
    };

    const handleEditClick = (vehicle) => {
        setSelectedVehicle(vehicle);
        setIsModalOpen(true);
    };

    const handleDeleteClick = async (id) => {
        if (window.confirm('¿Está seguro de eliminar este vehículo?')) {
            try {
                await vehicleService.deleteVehicle(id);
                fetchVehicles(); // Recargar lista
            } catch (error) {
                console.error("Error deleting vehicle:", error);
                alert("Error al eliminar el vehículo");
            }
        }
    };

    const handleModalSuccess = () => {
        fetchVehicles();
    };

    // Filtro simple en cliente
    const filteredVehicles = vehicles.filter(v => {
        const searchLower = searchTerm.toLowerCase();
        return (
            v.plate?.toLowerCase().includes(searchLower) ||
            v.brand?.toLowerCase().includes(searchLower) ||
            v.model?.toLowerCase().includes(searchLower) ||
            v.client_name?.toLowerCase().includes(searchLower)
        );
    });

    return (
        <div className="space-y-6">
            {/* Header Area */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Gestión de Vehículos</h1>
                    <div className="flex items-center text-sm text-gray-500 mt-1">
                        <span>Inicio</span>
                        <span className="mx-2">/</span>
                        <span className="text-blue-600 font-medium">Autos</span>
                    </div>
                </div>
                <button
                    onClick={handleCreateClick}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 font-medium shadow-lg hover:shadow-xl transition-all"
                >
                    <Plus size={18} />
                    Nuevo Vehículo
                </button>
            </div>

            {/* Filters Bar */}
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col md:flex-row gap-4 justify-between items-center">
                <div className="relative flex-1 w-full md:max-w-lg">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <input
                        type="text"
                        placeholder="Buscar por patente, marca o modelo..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <div className="flex gap-3 w-full md:w-auto">
                    <select className="px-4 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option>Todos</option>
                        {/* Aquí se podrían agregar filtros de estado reales si el backend los soportara */}
                    </select>

                    <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-50 text-gray-700">
                        <Filter size={16} />
                        Más filtros
                    </button>

                    <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-50 text-gray-700">
                        <Download size={16} />
                        Exportar
                    </button>
                </div>
            </div>

            {/* Table */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 border-b border-gray-100">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider w-4">
                                    <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Patente</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Marca/Modelo</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">VIN</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Cliente</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Estado</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Año</th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {loading ? (
                                <tr>
                                    <td colSpan="8" className="px-6 py-8 text-center text-gray-500">
                                        Cargando vehículos...
                                    </td>
                                </tr>
                            ) : filteredVehicles.length === 0 ? (
                                <tr>
                                    <td colSpan="8" className="px-6 py-8 text-center text-gray-500">
                                        No se encontraron vehículos.
                                    </td>
                                </tr>
                            ) : (
                                filteredVehicles.map((vehicle) => (
                                    <tr key={vehicle.id} className="hover:bg-blue-50/50 transition-colors">
                                        <td className="px-6 py-4">
                                            <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="font-bold text-blue-600 hover:text-blue-800 cursor-pointer">{vehicle.plate}</span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="text-sm font-medium text-gray-900">{vehicle.brand}</div>
                                            <div className="text-xs text-gray-500">{vehicle.model}</div>
                                        </td>
                                        <td className="px-6 py-4 text-xs text-gray-500 font-mono">
                                            {vehicle.vin || 'N/A'}
                                        </td>
                                        <td className="px-6 py-4 text-sm text-blue-600 hover:underline cursor-pointer">
                                            {vehicle.client_name || 'Desconocido'}
                                        </td>
                                        <td className="px-6 py-4">
                                            <StatusBadge status="En taller" />
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-500">
                                            {vehicle.year}
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <div className="flex items-center justify-end gap-2">
                                                <button className="p-1.5 text-gray-400 hover:text-blue-600 transition-colors"><Eye size={18} /></button>
                                                <button
                                                    onClick={() => handleEditClick(vehicle)}
                                                    className="p-1.5 text-gray-400 hover:text-green-600 transition-colors"
                                                >
                                                    <Edit2 size={18} />
                                                </button>
                                                <button
                                                    onClick={() => handleDeleteClick(vehicle.id)}
                                                    className="p-1.5 text-gray-400 hover:text-red-600 transition-colors"
                                                >
                                                    <Trash2 size={18} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Pagination (Static for now) */}
                <div className="px-6 py-4 border-t border-gray-100 flex items-center justify-between">
                    <span className="text-sm text-gray-500">Mostrando {filteredVehicles.length} registros</span>
                    <div className="flex items-center gap-2">
                        <button className="px-3 py-1 border border-gray-200 rounded-md text-sm hover:bg-gray-50 disabled:opacity-50" disabled>Anterior</button>
                        <button className="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">1</button>
                        <button className="px-3 py-1 border border-gray-200 rounded-md text-sm hover:bg-gray-50">Siguiente</button>
                    </div>
                </div>
            </div>

            <VehicleModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                vehicle={selectedVehicle}
                onSuccess={handleModalSuccess}
            />
        </div>
    );
};

export default Dashboard;
