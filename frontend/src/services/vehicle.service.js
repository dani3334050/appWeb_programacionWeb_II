import api from '../api/axios';

const VehicleService = {
  getAllVehicles: async () => {
    try {
      const response = await api.get('/vehicles');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  createVehicle: async (vehicleData) => {
    try {
      // vehicleData expects: { client_id, plate, brand, model, year, vin }
      // The API endpoint for creation is under /clients/:client_id/vehicles
      // We need to extract client_id to construct the URL
      const { client_id, ...data } = vehicleData;
      const response = await api.post(`/clients/${client_id}/vehicles`, data);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  updateVehicle: async (id, vehicleData) => {
    try {
      const response = await api.put(`/vehicles/${id}`, vehicleData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  deleteVehicle: async (id) => {
    try {
      const response = await api.delete(`/vehicles/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default VehicleService;
