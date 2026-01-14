import { useState } from 'react';

const MarketplaceModal = ({ isOpen, onClose, onRefresh }) => {
    const [formData, setFormData] = useState({
        title: '',
        brand: '',
        model: '',
        year: new Date().getFullYear(),
        price: '',
        description: '',
        image_url: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/marketplace/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Error al publicar el auto');
            }

            onRefresh();
            onClose();
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
            <div className="bg-gray-800 rounded-2xl w-full max-w-lg shadow-2xl border border-gray-700 overflow-hidden">
                <div className="p-6 border-b border-gray-700 flex justify-between items-center">
                    <h3 className="text-xl font-bold text-white">Vender mi Auto</h3>
                    <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl">&times;</button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {error && <div className="text-red-400 text-sm bg-red-400/10 p-2 rounded">{error}</div>}

                    <div>
                        <label className="block text-gray-400 text-xs mb-1">Título del Anuncio</label>
                        <input name="title" value={formData.title} onChange={handleChange} required className="w-full bg-gray-700 text-white rounded p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ej: Toyota Corolla 2018 Impecable" />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-gray-400 text-xs mb-1">Marca</label>
                            <input name="brand" value={formData.brand} onChange={handleChange} required className="w-full bg-gray-700 text-white rounded p-2 text-sm outline-none" placeholder="Toyota" />
                        </div>
                        <div>
                            <label className="block text-gray-400 text-xs mb-1">Modelo</label>
                            <input name="model" value={formData.model} onChange={handleChange} required className="w-full bg-gray-700 text-white rounded p-2 text-sm outline-none" placeholder="Corolla" />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-gray-400 text-xs mb-1">Año</label>
                            <input type="number" name="year" value={formData.year} onChange={handleChange} required className="w-full bg-gray-700 text-white rounded p-2 text-sm outline-none" />
                        </div>
                        <div>
                            <label className="block text-gray-400 text-xs mb-1">Precio ($)</label>
                            <input type="number" name="price" value={formData.price} onChange={handleChange} required className="w-full bg-gray-700 text-white rounded p-2 text-sm outline-none" placeholder="15000" />
                        </div>
                    </div>

                    <div>
                        <label className="block text-gray-400 text-xs mb-1">URL de Imagen (Opcional)</label>
                        <input name="image_url" value={formData.image_url} onChange={handleChange} className="w-full bg-gray-700 text-white rounded p-2 text-sm outline-none" placeholder="https://..." />
                    </div>

                    <div>
                        <label className="block text-gray-400 text-xs mb-1">Descripción</label>
                        <textarea name="description" value={formData.description} onChange={handleChange} rows="3" className="w-full bg-gray-700 text-white rounded p-2 text-sm outline-none" placeholder="Detalles adicionales..." />
                    </div>

                    <div className="pt-4 flex justify-end gap-3">
                        <button type="button" onClick={onClose} className="px-4 py-2 text-gray-300 hover:text-white transition-colors">Cancelar</button>
                        <button type="submit" disabled={loading} className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold shadow-lg transition-transform transform active:scale-95">
                            {loading ? 'Publicando...' : 'Publicar Auto'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default MarketplaceModal;
