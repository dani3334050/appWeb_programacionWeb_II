import { Link } from 'react-router-dom';
import workshopBg from '../assets/workshop_bg.jpg';
import PublicNavbar from '../components/PublicNavbar';

const LandingPage = () => {
    return (
        <div className="bg-gray-900 min-h-screen text-white font-sans selection:bg-blue-500 selection:text-white">
            <PublicNavbar />

            {/* HERO SECTION */}
            <div className="relative h-screen flex items-center justify-center overflow-hidden">
                {/* Background Image with Gradient Overlay */}
                <div
                    className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat bg-fixed transform scale-105"
                    style={{ backgroundImage: `url(${workshopBg})` }}
                >
                    <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-gray-900"></div>
                </div>

                {/* Hero Content */}
                <div className="relative z-10 text-center px-4 max-w-5xl mx-auto mt-16">
                    <span className="inline-block py-1 px-3 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-bold tracking-widest uppercase mb-6 animate-fade-in-up">
                        Gestión Automotriz Premium
                    </span>
                    <h1 className="text-5xl md:text-7xl lg:text-8xl font-black mb-8 tracking-tighter leading-tight bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent drop-shadow-2xl animate-fade-in-up delay-100">
                        TALLER MECÁNICO <br /> <span className="text-blue-500">PRO</span>
                    </h1>
                    <p className="text-lg md:text-2xl text-gray-300 mb-10 font-light max-w-2xl mx-auto leading-relaxed animate-fade-in-up delay-200">
                        La solución integral para el cuidado de tu vehículo.
                        Desde mantenimiento experto hasta la compra-venta segura en nuestro marketplace exclusivo.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-5 justify-center w-full max-w-lg mx-auto animate-fade-in-up delay-300">
                        <Link
                            to="/marketplace"
                            className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white text-lg font-bold rounded-full transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-blue-500/50 flex items-center justify-center gap-2"
                        >
                            <span>Explorar Vehículos</span>
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                        </Link>
                        <a
                            href="#services"
                            className="px-8 py-4 bg-white/10 hover:bg-white/20 border border-white/20 text-white text-lg font-bold rounded-full transition-all duration-300 backdrop-blur-md flex items-center justify-center"
                        >
                            Nuestros Servicios
                        </a>
                    </div>
                </div>

                {/* Scroll Indicator */}
                <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce opacity-50">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>
                </div>
            </div>

            {/* INFO / FEATURES SECTION */}
            <section id="about" className="py-24 bg-gray-900 relative">
                <div className="container mx-auto px-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
                        <div className="p-8 rounded-3xl bg-gray-800/50 border border-gray-700/50 backdrop-blur-sm hover:bg-gray-800 transition-colors group">
                            <div className="w-16 h-16 bg-blue-600/20 text-blue-400 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                            </div>
                            <h3 className="text-xl font-bold mb-3">Servicio Certificado</h3>
                            <p className="text-gray-400 leading-relaxed">Mecánicos expertos y piezas originales garantizan el mejor cuidado para tu motor.</p>
                        </div>
                        <div className="p-8 rounded-3xl bg-gray-800/50 border border-gray-700/50 backdrop-blur-sm hover:bg-gray-800 transition-colors group">
                            <div className="w-16 h-16 bg-green-600/20 text-green-400 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            </div>
                            <h3 className="text-xl font-bold mb-3">Venta Directa</h3>
                            <p className="text-gray-400 leading-relaxed">Publica tu auto en nuestro Marketplace y conéctate con compradores al instante.</p>
                        </div>
                        <div className="p-8 rounded-3xl bg-gray-800/50 border border-gray-700/50 backdrop-blur-sm hover:bg-gray-800 transition-colors group">
                            <div className="w-16 h-16 bg-purple-600/20 text-purple-400 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            </div>
                            <h3 className="text-xl font-bold mb-3">Transparencia Total</h3>
                            <p className="text-gray-400 leading-relaxed">Sigue el estado de tu reparación en tiempo real desde tu propio panel de control.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* SERVICES PREVIEW */}
            <section id="services" className="py-24 bg-gray-800 text-center">
                <div className="container mx-auto px-6">
                    <span className="text-blue-400 font-bold tracking-wider uppercase text-sm mb-2 block">Lo que hacemos</span>
                    <h2 className="text-4xl md:text-5xl font-bold mb-16 text-white">Nuestros Servicios Principales</h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {['Diagnóstico Computarizado', 'Reparación de Motores', 'Frenos y Suspensión', 'Cambio de Aceite'].map((service, index) => (
                            <div key={index} className="p-6 bg-gray-700/50 rounded-2xl hover:bg-gray-700 transition-colors text-left border-l-4 border-blue-500">
                                <h4 className="text-xl font-bold text-white mb-2">{service}</h4>
                                <p className="text-gray-400 text-sm">Tecnología de punta para asegurar el máximo rendimiento.</p>
                            </div>
                        ))}
                    </div>

                    <div className="mt-16">
                        <Link to="/register" className="inline-flex items-center text-blue-400 font-bold hover:text-blue-300 hover:underline">
                            Ver todos los servicios <span className="ml-2">&rarr;</span>
                        </Link>
                    </div>
                </div>
            </section>

            {/* CTA SECTION */}
            <section className="py-24 relative overflow-hidden">
                <div className="absolute inset-0 bg-blue-600 opacity-10"></div>
                <div className="container mx-auto px-6 relative z-10 text-center">
                    <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">¿Listo para empezar?</h2>
                    <p className="text-xl text-blue-200 mb-10 max-w-2xl mx-auto">Regístrate hoy mismo para agendar citas o vender tu vehículo sin complicaciones.</p>
                    <Link
                        to="/register"
                        className="px-10 py-5 bg-white text-blue-900 text-xl font-bold rounded-full hover:bg-gray-100 transition-all shadow-xl hover:shadow-white/20 transform hover:-translate-y-1 inline-block"
                    >
                        Crear Cuenta Gratis
                    </Link>
                </div>
            </section>

            {/* FOOTER */}
            <footer className="bg-black py-12 border-t border-gray-800">
                <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center text-gray-500 text-sm">
                    <div className="mb-4 md:mb-0">
                        <span className="text-2xl font-bold text-white block mb-2">TallerPro</span>
                        &copy; {new Date().getFullYear()} Todos los derechos reservados.
                    </div>
                    <div className="flex gap-6">
                        <a href="#" className="hover:text-white transition-colors">Términos</a>
                        <a href="#" className="hover:text-white transition-colors">Privacidad</a>
                        <a href="#" className="hover:text-white transition-colors">Contacto</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
