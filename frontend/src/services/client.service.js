import api from '../api/axios';

const ClientService = {
    getAllClients: async () => {
        try {
            const response = await api.get('/clients');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    createClient: async (clientData) => {
        try {
            const response = await api.post('/clients', clientData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Method to get client vehicles if needed elsewhere
    getClientVehicles: async (clientId) => {
        try {
            const response = await api.get(`/clients/${clientId}/vehicles`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};

export default ClientService;
