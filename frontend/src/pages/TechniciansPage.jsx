import { useState, useEffect } from 'react';
import api from '../api/axios';
import { Search, Filter, Plus, MoreVertical, Star, MapPin, Briefcase, Calendar } from 'lucide-react';

const TechniciansPage = () => {
    const [technicians, setTechnicians] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('Todos'); // Todos, Disponibles, Ocupados, Ausentes

    useEffect(() => {
        fetchTechnicians();
    }, []);

    const fetchTechnicians = async () => {
        try {
            const response = await api.get('/users/technicians');
            setTechnicians(response.data);
        } catch (error) {
            console.error("Error fetching technicians:", error);
            // Fallback mock data if backend has no technicians yet
            setTechnicians([
                { id: 1, first_name: "Carlos", last_name: "Ruiz", specialties: ["Mecánica General", "Transmisión"], status: "Disponible", certification: "ASE, Toyota Certified", jobs_month: 47, rating: 4.8 },
                { id: 2, first_name: "Roberto", last_name: "Silva", specialties: ["Electricidad", "Diagnóstico"], status: "Ocupado", certification: "ASE, Bosch Certified", jobs_month: 52, rating: 4.9 },
                { id: 3, first_name: "Luis", last_name: "Vargas", specialties: ["Chapistería", "Pintura"], status: "Disponible", certification: "I-CAR", jobs_month: 38, rating: 4.7 },
                { id: 4, first_name: "Miguel", last_name: "Torres", specialties: ["Frenos", "Suspensión"], status: "Ausente", certification: "ASE", jobs_month: 41, rating: 4.6 }
            ]);
        } finally {
            setLoading(false);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'Disponible': return 'bg-green-500';
            case 'Ocupado': return 'bg-red-500';
            case 'Ausente': return 'bg-gray-400';
            default: return 'bg-blue-500';
        }
    };

    const getStatusBadge = (status) => {
        switch (status) {
            case 'Disponible': return 'text-green-600 bg-green-50';
            case 'Ocupado': return 'text-red-600 bg-red-50';
            case 'Ausente': return 'text-gray-600 bg-gray-50';
            default: return 'text-blue-600 bg-blue-50';
        }
    };

    const filteredTechnicians = filter === 'Todos'
        ? technicians
        : technicians.filter(tech => tech.status === filter);

    return (
        <div className="p-8 w-full max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">Equipo Técnico</h1>
                    <div className="flex items-center text-sm text-gray-500 mt-1">
                        <span>Inicio</span>
                        <span className="mx-2">›</span>
                        <span>Técnicos</span>
                    </div>
                </div>
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 font-medium transition-colors shadow-sm">
                    <Plus size={20} />
                    Agregar Técnico
                </button>
            </div>

            {/* Controls */}
            <div className="flex flex-col sm:flex-row justify-between items-center bg-white p-2 rounded-xl mb-8 shadow-sm border border-gray-100">
                <div className="flex items-center gap-2 p-2">
                    <button className="p-2 hover:bg-gray-100 rounded-lg text-blue-600">
                        <div className="grid grid-cols-2 gap-0.5 w-5 h-5">
                            <div className="bg-current rounded-[1px]"></div>
                            <div className="bg-current rounded-[1px]"></div>
                            <div className="bg-current rounded-[1px]"></div>
                            <div className="bg-current rounded-[1px]"></div>
                        </div>
                    </button>
                    <button className="p-2 hover:bg-gray-100 rounded-lg text-gray-400">
                        <div className="flex flex-col gap-1 w-5">
                            <div className="h-0.5 bg-current w-full"></div>
                            <div className="h-0.5 bg-current w-full"></div>
                            <div className="h-0.5 bg-current w-full"></div>
                        </div>
                    </button>
                </div>

                <div className="flex bg-gray-100/80 p-1 rounded-lg">
                    {['Todos', 'Disponibles', 'Ocupados', 'Ausentes'].map((f) => (
                        <button
                            key={f}
                            onClick={() => setFilter(f)}
                            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${filter === f
                                    ? 'bg-blue-600 text-white shadow-sm'
                                    : 'text-gray-600 hover:bg-gray-200'
                                }`}
                        >
                            {f}
                        </button>
                    ))}
                </div>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredTechnicians.map((tech) => (
                    <div key={tech.id} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-4">
                            <div className={`w-14 h-14 rounded-full flex items-center justify-center text-white text-xl font-bold ${tech.id % 3 === 0 ? 'bg-indigo-500' : tech.id % 2 === 0 ? 'bg-blue-500' : 'bg-blue-600'
                                }`}>
                                {tech.first_name[0]}{tech.last_name ? tech.last_name[0] : ''}
                            </div>
                            <button className="text-gray-400 hover:text-gray-600">
                                <MoreVertical size={20} />
                            </button>
                        </div>

                        <h3 className="text-lg font-bold text-gray-800 mb-1">
                            {tech.first_name} {tech.last_name}
                        </h3>

                        <div className="flex flex-wrap gap-2 mb-3">
                            {tech.specialties?.map((spec, index) => (
                                <span key={index} className="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded-md font-medium border border-blue-100">
                                    {spec}
                                </span>
                            ))}
                        </div>

                        <div className="space-y-2 mb-6">
                            <div className="flex items-center gap-2 text-sm">
                                <span className={`w-2.5 h-2.5 rounded-full ${getStatusColor(tech.status)}`}></span>
                                <span className="font-medium text-gray-700">{tech.status}</span>
                            </div>

                            <div className="flex items-center gap-2 text-sm text-gray-500">
                                <Filter size={14} />
                                <span>{tech.certification}</span>
                            </div>

                            <div className="flex items-center gap-2 text-sm text-gray-500">
                                <Briefcase size={14} />
                                <span>{tech.jobs_month} trabajos este mes</span>
                            </div>

                            <div className="flex items-center gap-1 text-sm">
                                <div className="flex text-yellow-400">
                                    {[1, 2, 3, 4, 5].map((s) => (
                                        <Star key={s} size={14} fill={s <= Math.round(tech.rating) ? "currentColor" : "none"} />
                                    ))}
                                </div>
                                <span className="font-medium text-gray-700">({tech.rating})</span>
                            </div>
                        </div>

                        <button className="w-full py-2.5 border border-blue-200 text-blue-600 font-medium rounded-xl hover:bg-blue-50 transition-colors">
                            Ver perfil
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TechniciansPage;
