from flask import Blueprint, request, jsonify
from app.services.client_service import ClientService
from app.models import Vehicle

# ==============================================================================
# Capa de RUTAS (Controlador) - Vehicles
# ==============================================================================
# Gestiona las peticiones HTTP para operaciones CRUD directas sobre vehículos.
# ==============================================================================

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/vehicles')

# ==============================================================================
# Endpoint: Listar Todos los Vehículos
# ==============================================================================
@vehicles_bp.route('', methods=['GET'])
def get_all_vehicles():
    """
    Obtiene todos los vehículos registrados, incluyendo info básica del dueño.
    """
    try:
        vehicles = ClientService.get_all_vehicles()
        # Enriquecer la respuesta con el nombre del dueño para mostrar en tabla
        response = []
        for v in vehicles:
            v_dict = v.to_dict()
            # Añadir nombre del cliente directamente al diccionario del vehículo
            # Usamos la relación backref 'owner' definida en Client.vehicles
            if v.owner:
                v_dict['client_name'] = f"{v.owner.first_name} {v.owner.last_name}"
            else:
                v_dict['client_name'] = "Desconocido"
            response.append(v_dict)
            
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"msg": f"Error al obtener vehículos: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Actualizar Vehículo
# ==============================================================================
@vehicles_bp.route('/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    """
    Actualiza los datos de un vehículo existente.
    """
    data = request.get_json()
    try:
        updated_vehicle = ClientService.update_vehicle(vehicle_id, data)
        return jsonify({"msg": "Vehículo actualizado", "vehicle": updated_vehicle.to_dict()}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Eliminar Vehículo
# ==============================================================================
@vehicles_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """
    Elimina un vehículo por su ID.
    """
    try:
        ClientService.delete_vehicle(vehicle_id)
        return jsonify({"msg": "Vehículo eliminado exitosamente"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500
