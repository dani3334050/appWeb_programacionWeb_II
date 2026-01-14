import { useState, useEffect } from 'react';
import { X, Save } from 'lucide-react';
import vehicleService from '../services/vehicle.service';
// Assuming client service exists, if not we might need to create it or fetch clients differently
import clientService from '../services/client.service';

const VehicleModal = ({ isOpen, onClose, vehicle = null, onSuccess }) => {
    const [formData, setFormData] = useState({
        plate: '',
        brand: '',
        model: '',
        year: '',
        vin: '',
        client_id: ''
    });
    const [clients, setClients] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (isOpen) {
            fetchClients();
            if (vehicle) {
                setFormData({
                    plate: vehicle.plate,
                    brand: vehicle.brand,
                    model: vehicle.model,
                    year: vehicle.year,
                    vin: vehicle.vin || '',
                    client_id: vehicle.client_id
                });
            } else {
                setFormData({
                    plate: '',
                    brand: '',
                    model: '',
                    year: new Date().getFullYear(),
                    vin: '',
                    client_id: ''
                });
            }
            setError('');
        }
    }, [isOpen, vehicle]);

    const fetchClients = async () => {
        try {
            const data = await clientService.getAllClients();
            setClients(data);
        } catch (err) {
            console.error("Error fetching clients:", err);
            setError("Error al cargar clientes");
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (vehicle) {
                await vehicleService.updateVehicle(vehicle.id, formData);
            } else {
                await vehicleService.createVehicle(formData);
            }
            onSuccess();
            onClose();
        } catch (err) {
            setError(err.response?.data?.msg || 'Error al guardar el vehículo');
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-xl w-full max-w-lg overflow-hidden">
                <div className="bg-gray-50 px-6 py-4 border-b border-gray-100 flex justify-between items-center">
                    <h2 className="text-xl font-bold text-gray-800">
                        {vehicle ? 'Editar Vehículo' : 'Nuevo Vehículo'}
                    </h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {error && (
                        <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    <div className="space-y-4">
                        {!vehicle && (
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Cliente</label>
                                <select
                                    name="client_id"
                                    value={formData.client_id}
                                    onChange={handleChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    required
                                >
                                    <option value="">Seleccionar Cliente</option>
                                    {clients.map(client => (
                                        <option key={client.id} value={client.id}>
                                            {client.first_name} {client.last_name}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        )}

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Patente</label>
                                <input
                                    type="text"
                                    name="plate"
                                    value={formData.plate}
                                    onChange={handleChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all uppercase"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Año</label>
                                <input
                                    type="number"
                                    name="year"
                                    value={formData.year}
                                    onChange={handleChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    required
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Marca</label>
                                <input
                                    type="text"
                                    name="brand"
                                    value={formData.brand}
                                    onChange={handleChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Modelo</label>
                                <input
                                    type="text"
                                    name="model"
                                    value={formData.model}
                                    onChange={handleChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">VIN (Opcional)</label>
                            <input
                                type="text"
                                name="vin"
                                value={formData.vin}
                                onChange={handleChange}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all uppercase"
                            />
                        </div>
                    </div>

                    <div className="pt-4 flex justify-end gap-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 font-medium transition-colors"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium flex items-center gap-2 shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
                        >
                            <Save size={18} />
                            {loading ? 'Guardando...' : 'Guardar Vehículo'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default VehicleModal;
