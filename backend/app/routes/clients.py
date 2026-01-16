from flask import Blueprint, request, jsonify
from app.services.client_service import ClientService
from app.models import Client, User
from flask_jwt_extended import jwt_required, get_jwt_identity

# ==============================================================================
# Capa de RUTAS (Controlador) - Clients
# ==============================================================================
# Gestiona las peticiones HTTP relacionadas con clientes y sus vehículos.
# Delega la lógica de negocio a ClientService.
# ==============================================================================

clients_bp = Blueprint('clients', __name__, url_prefix='/api/clients')

# ==============================================================================
# Endpoint: Crear Cliente
# ==============================================================================
@clients_bp.route('', methods=['POST'])
@jwt_required()
def create_client():
    """
    Crea un nuevo cliente.

    Request Body:
        first_name (str): Nombre.
        last_name (str): Apellido.
        email (str, optional): Email.
        phone (str, optional): Teléfono.
        address (str, optional): Dirección.

    Returns:
        JSON: Cliente creado.
    """
    data = request.get_json()

    # Validamos campos obligatorios
    if not data or not data.get('first_name') or not data.get('last_name'):
        return jsonify({"msg": "Nombre y Apellido son obligatorios"}), 400

    try:
        new_client = ClientService.create_client(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        return jsonify({"msg": "Cliente creado exitosamente", "client": new_client.to_dict()}), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Listar Clientes
# ==============================================================================
@clients_bp.route('', methods=['GET'])
def get_clients():
    """
    Obtiene la lista de todos los clientes registrados.
    """
    try:
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)
        if page and per_page:
            query = Client.query.order_by(Client.created_at.desc())
            items = query.limit(per_page).offset((page - 1) * per_page).all()
            total = Client.query.count()
            return jsonify({
                "items": [c.to_dict() for c in items],
                "meta": {"page": page, "per_page": per_page, "total": total}
            }), 200
        clients = ClientService.get_all_clients()
        return jsonify([client.to_dict() for client in clients]), 200
    except Exception as e:
        return jsonify({"msg": f"Error al obtener clientes: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Obtener Cliente por ID
# ==============================================================================
@clients_bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    try:
        client = ClientService.get_client_by_id(client_id)
        if not client:
            return jsonify({"msg": "Cliente no encontrado"}), 404
        return jsonify(client.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Actualizar Cliente
# ==============================================================================
@clients_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    data = request.get_json() or {}
    try:
        updated = ClientService.update_client(client_id, data)
        return jsonify({"msg": "Cliente actualizado", "client": updated.to_dict()}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Eliminar Cliente
# ==============================================================================
@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({"msg": "Acceso denegado. Se requieren permisos de administrador"}), 403
        ClientService.delete_client(client_id)
        return jsonify({"msg": "Cliente eliminado exitosamente"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Agregar Vehículo a Cliente
# ==============================================================================
@clients_bp.route('/<int:client_id>/vehicles', methods=['POST'])
@jwt_required()
def add_vehicle(client_id):
    """
    Agrega un vehículo asociado a un cliente específico.
    
    Path Params:
        client_id (int): ID del cliente.

    Request Body:
        plate (str): Placa.
        brand (str): Marca.
        model (str): Modelo.
        year (int): Año.
        vin (str, optional): VIN.
    """
    data = request.get_json()

    # Validaciones de campos obligatorios del vehículo
    required_fields = ['plate', 'brand', 'model', 'year']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"msg": f"Faltan datos obligatorios: {', '.join(required_fields)}"}), 400

    try:
        new_vehicle = ClientService.add_vehicle(
            client_id=client_id,
            plate=data['plate'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            vin=data.get('vin')
        )
        return jsonify({"msg": "Vehículo agregado exitosamente", "vehicle": new_vehicle.to_dict()}), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500

# ==============================================================================
# Endpoint: Listar Vehículos de un Cliente
# ==============================================================================
@clients_bp.route('/<int:client_id>/vehicles', methods=['GET'])
def get_client_vehicles(client_id):
    """
    Obtiene todos los vehículos asociados a un cliente.
    """
    try:
        vehicles = ClientService.get_client_vehicles(client_id)
        return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": f"Error al obtener vehículos: {str(e)}"}), 500
