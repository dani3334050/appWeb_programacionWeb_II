from flask import Blueprint, request, jsonify
from app.services.client_service import ClientService
from app.models import Vehicle
from flask_jwt_extended import jwt_required

# ==============================================================================
# Capa de RUTAS (Controlador) - Vehicles
# ==============================================================================
# Gestiona las peticiones HTTP para operaciones CRUD directas sobre vehículos.
# ==============================================================================

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/api/vehicles')

# ==============================================================================
# Endpoint: Listar Todos los Vehículos
# ==============================================================================
@vehicles_bp.route('', methods=['GET'])
def get_all_vehicles():
    """
    Obtiene todos los vehículos registrados, incluyendo info básica del dueño.
    """
    try:
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)
        plate = request.args.get('plate', type=str)

        query = Vehicle.query
        if plate:
            query = query.filter(Vehicle.plate.ilike(f"%{plate}%"))

        if page and per_page:
            items = query.limit(per_page).offset((page - 1) * per_page).all()
            total = query.count()
        else:
            items = query.all()
            total = len(items)

        response = []
        for v in items:
            v_dict = v.to_dict()
            if v.owner:
                v_dict['client_name'] = f"{v.owner.first_name} {v.owner.last_name}"
            else:
                v_dict['client_name'] = "Desconocido"
            response.append(v_dict)

        if page and per_page:
            return jsonify({"items": response, "meta": {"page": page, "per_page": per_page, "total": total}}), 200
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"msg": f"Error al obtener vehículos: {str(e)}"}), 500

@vehicles_bp.route('', methods=['POST'])
@jwt_required()
def create_vehicle():
    data = request.get_json() or {}
    required = ['client_id', 'plate', 'brand', 'model', 'year']
    if not all(k in data for k in required):
        return jsonify({"msg": f"Faltan datos obligatorios: {', '.join(required)}"}), 400
    try:
        v = ClientService.add_vehicle(
            client_id=data['client_id'],
            plate=data['plate'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            vin=data.get('vin')
        )
        return jsonify({"msg": "Vehículo creado", "vehicle": v.to_dict()}), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

@vehicles_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    try:
        v = ClientService.get_vehicle_by_id(vehicle_id)
        if not v:
            return jsonify({"msg": "Vehículo no encontrado"}), 404
        d = v.to_dict()
        if v.owner:
            d['client_name'] = f"{v.owner.first_name} {v.owner.last_name}"
        return jsonify(d), 200
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Actualizar Vehículo
# ==============================================================================
@vehicles_bp.route('/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
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
